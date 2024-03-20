"""DatabricksNotebookOperator for submitting notebook jobs to databricks."""
from __future__ import annotations

import time
from typing import Any

import airflow
from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.providers.databricks.hooks.databricks import DatabricksHook
from airflow.utils.context import Context
from databricks_cli.runs.api import RunsApi
from databricks_cli.sdk.api_client import ApiClient

from astro_databricks.operators.workflow import (
    DatabricksMetaData,
    DatabricksWorkflowTaskGroup,
)
from astro_databricks.plugins.plugin import (
    DatabricksJobRepairSingleFailedLink,
    DatabricksJobRunLink,
)
from astro_databricks.settings import DATABRICKS_JOBS_API_VERSION


class DatabricksTaskOperator(BaseOperator):
    """
    Launches a All Types Task to databricks using an Airflow operator.

    The DatabricksTaskOperator allows users to launch and monitor task
     deployments on Databricks as Aiflow tasks.
    It can be used as a part of a DatabricksWorkflowTaskGroup to take advantage of job clusters,
    which allows users to run their tasks on cheaper clusters that can be shared between tasks.

    Here is an example of running a notebook as a part of a workflow task group:

    .. code-block: python

        with dag:
            task_group = DatabricksWorkflowTaskGroup(
                group_id="test_workflow",
                databricks_conn_id="databricks_conn",
                job_clusters=job_cluster_spec,
            )
            with task_group:
                task_1 = DatabricksTaskOperator(
                    task_id="task_1",
                    databricks_conn_id="databricks_conn",
                    job_cluster_key="Shared_job_cluster",
                    task_config={
                        "notebook_task": {
                            "notebook_path": "/Users/daniel@astronomer.io/Test workflow",
                            "source": "WORKSPACE",
                            "base_parameters": {
                                "end_time": "{{ ts }}",
                                "start_time": "{{ ts }}",
                            },
                        },
                        "libraries": [
                            {"pypi": {"package": "scikit-learn"}},
                            {"pypi": {"package": "pandas"}},
                        ],
                    },
                )
                task_2 = DatabricksTaskOperator(
                    task_id="task_2",
                    databricks_conn_id="databricks_conn",
                    job_cluster_key="Shared_job_cluster",
                    task_config={
                        "spark_jar_task": {
                            "main_class_name": "jar.main.class.here",
                            "parameters": [
                                "--key",
                                "value",
                            ],
                            "run_as_repl": "true",
                        },
                        "libraries": [
                            {
                                "jar": "your.jar.path/file.jar"
                            }
                        ],
                    },
                )
                task_1 >> task_2

        :param task_id: the task name displayed in Databricks and Airflow.
        :param databricks_conn_id: the connection id to use to connect to Databricks
        :param job_cluster_key: the connection id to use to connect to Databricks
        :param task_config: Please write appropriate configuration values for various tasks provided by Databricks
                            such as notebook_task, spark_jar_task, spark_python_task, spark_submit_task, etc.
                            For more information please visit
                                https://docs.databricks.com/dev-tools/api/latest/jobs.html#operation/JobsCreate
    """

    operator_extra_links = (
        DatabricksJobRunLink(),
        DatabricksJobRepairSingleFailedLink(),
    )
    template_fields = ("databricks_metadata",)

    def __init__(
        self,
        databricks_conn_id: str,
        task_config: dict | None = None,
        job_cluster_key: str | None = None,
        new_cluster: dict | None = None,
        existing_cluster_id: str | None = None,
        **kwargs,
    ):
        if new_cluster and existing_cluster_id:
            raise ValueError(
                "Both new_cluster and existing_cluster_id are set. Only one can be set."
            )

        self.task_config = task_config or {}
        self.databricks_conn_id = databricks_conn_id
        self.databricks_run_id = ""
        self.databricks_metadata: dict | None = None
        self.job_cluster_key = job_cluster_key
        self.new_cluster = new_cluster
        self.existing_cluster_id = existing_cluster_id or ""
        super().__init__(**kwargs)

        # For Airflow versions <2.3, the `task_group` attribute is unassociated, and hence we need to add that.
        if not hasattr(self, "task_group"):
            from airflow.utils.task_group import TaskGroupContext

            self.task_group = TaskGroupContext.get_current_task_group(self.dag)

    def _get_task_base_json(self) -> dict[str, Any]:
        """Get task base json to be used for task group tasks and single task submissions."""
        return self.task_config

    def find_parent_databricks_workflow_task_group(self):
        """
        Find the closest parent_group which is an instance of DatabricksWorkflowTaskGroup.

        In the case of Airflow 2.2.x, inner Task Groups do not inherit properties from Parent Task Groups like more
        recent versions of Airflow. This lead to the issue:
        https://github.com/astronomer/astro-provider-databricks/pull/47
        """
        parent_group = self.task_group
        while parent_group:
            if parent_group.__class__.__name__ == "DatabricksWorkflowTaskGroup":
                return parent_group
            parent_group = parent_group._parent_group

    def convert_to_databricks_workflow_task(
        self, relevant_upstreams: list[BaseOperator], context: Context | None = None
    ):
        """
        Convert the operator to a Databricks workflow task that can be a task in a workflow
        """
        if airflow.__version__ in ("2.2.4", "2.2.5"):
            self.find_parent_databricks_workflow_task_group()
        else:
            pass

        if context:
            # The following exception currently only happens on Airflow 2.3, with the following error:
            # airflow.exceptions.AirflowException: XComArg result from test_workflow.launch at example_databricks_workflow with key="return_value" is not found!
            try:
                self.render_template_fields(context)
            except AirflowException:
                self.log.exception("Unable to process template fields")

        base_task_json = self._get_task_base_json()
        result = {
            "task_key": self._get_databricks_task_id(self.task_id),
            "depends_on": [
                {"task_key": self._get_databricks_task_id(t)}
                for t in self.upstream_task_ids
                if t in relevant_upstreams
            ],
            **base_task_json,
        }

        if self.job_cluster_key:
            result["job_cluster_key"] = self.job_cluster_key

        return result

    def _get_databricks_task_id(self, task_id: str):
        """Get the databricks task ID using dag_id and task_id. removes illegal characters."""
        return self.dag_id + "__" + task_id.replace(".", "__")

    def monitor_databricks_job(self):
        """Monitor the Databricks job until it completes. Raises Airflow exception if the job fails."""
        api_client = self._get_api_client()
        runs_api = RunsApi(api_client)
        current_task = self._get_current_databricks_task(runs_api)
        url = runs_api.get_run(
            self.databricks_run_id, version=DATABRICKS_JOBS_API_VERSION
        )["run_page_url"]
        self.log.info(f"Check the job run in Databricks: {url}")
        self._wait_for_pending_task(current_task, runs_api)
        self._wait_for_running_task(current_task, runs_api)
        self._wait_for_terminating_task(current_task, runs_api)
        final_state = runs_api.get_run(
            current_task["run_id"], version=DATABRICKS_JOBS_API_VERSION
        )["state"]
        self._handle_final_state(final_state)

    def _get_current_databricks_task(self, runs_api):
        return {
            x["task_key"]: x
            for x in runs_api.get_run(
                self.databricks_run_id, version=DATABRICKS_JOBS_API_VERSION
            )["tasks"]
        }[self._get_databricks_task_id(self.task_id)]

    def _handle_final_state(self, final_state):
        if final_state.get("life_cycle_state", None) != "TERMINATED":
            raise AirflowException(
                f"Databricks job failed with state {final_state}. Message: {final_state['state_message']}"
            )
        if final_state["result_state"] != "SUCCESS":
            raise AirflowException(
                "Task failed. Final State %s. Reason: %s",
                final_state["result_state"],
                final_state["state_message"],
            )

    def _get_lifestyle_state(self, current_task, runs_api):
        return runs_api.get_run(
            current_task["run_id"], version=DATABRICKS_JOBS_API_VERSION
        )["state"]["life_cycle_state"]

    def _wait_on_state(self, current_task, runs_api, state):
        while self._get_lifestyle_state(current_task, runs_api) == state:
            print(f"task {self.task_id.replace('.', '__')} {state.lower()}...")
            time.sleep(5)

    def _wait_for_terminating_task(self, current_task, runs_api):
        self._wait_on_state(current_task, runs_api, "TERMINATING")

    def _wait_for_running_task(self, current_task, runs_api):
        self._wait_on_state(current_task, runs_api, "RUNNING")

    def _wait_for_pending_task(self, current_task, runs_api):
        self._wait_on_state(current_task, runs_api, "PENDING")

    def _get_api_client(self):
        hook = DatabricksHook(self.databricks_conn_id)
        databricks_conn = hook.get_conn()
        return ApiClient(
            user=databricks_conn.login,
            token=databricks_conn.password,
            host=databricks_conn.host,
        )

    def launch_task_job(self):
        """Launch the notebook as a one-time job to Databricks."""
        api_client = self._get_api_client()
        base_task_json = self._get_task_base_json()
        run_json = {
            "run_name": self._get_databricks_task_id(self.task_id),
            **base_task_json,
        }
        if self.new_cluster and self.existing_cluster_id:
            raise ValueError(
                "Both new_cluster and existing_cluster_id are set. Only one can be set."
            )
        if self.existing_cluster_id:
            run_json["existing_cluster_id"] = self.existing_cluster_id
        elif self.new_cluster:
            run_json["new_cluster"] = self.new_cluster
        else:
            raise ValueError("Must specify either existing_cluster_id or new_cluster")
        runs_api = RunsApi(api_client)
        run = runs_api.submit_run(run_json)
        self.databricks_run_id = run["run_id"]
        return run

    def execute(self, context: Context) -> Any:
        """
        Execute the DataBricksNotebookOperator.

        Executes the DataBricksNotebookOperator. If the task is inside of a
        DatabricksWorkflowTaskGroup, it assumes the notebook is already launched
        and proceeds to monitor the running notebook.

        :param context:
        :return:
        """
        if self.databricks_task_group:
            # if we are in a workflow, we assume there is an upstream launch task
            if not self.databricks_metadata:
                launch_task_id = [
                    task for task in self.upstream_task_ids if task.endswith(".launch")
                ][0]
                self.databricks_metadata = context["ti"].xcom_pull(
                    task_ids=launch_task_id
                )
            databricks_metadata = DatabricksMetaData(**self.databricks_metadata)
            self.databricks_run_id = databricks_metadata.databricks_run_id
            self.databricks_conn_id = databricks_metadata.databricks_conn_id
        else:
            self.launch_task_job()

        self.monitor_databricks_job()

    @property
    def databricks_task_group(self) -> DatabricksWorkflowTaskGroup | None:
        """
        Traverses up parent TaskGroups until the `is_databricks` flag is found.
        If found, returns the task group. Otherwise, returns None.
        """
        parent_tg = self.task_group

        while parent_tg:
            if hasattr(parent_tg, "is_databricks") and getattr(
                parent_tg, "is_databricks"
            ):
                return parent_tg

            # here, we rely on the fact that Airflow sets the task_group property on tasks/task groups
            # if that ever changes, we will need to update this
            if hasattr(parent_tg, "task_group") and getattr(parent_tg, "task_group"):
                parent_tg = parent_tg.task_group
            else:
                return None

        return None
