from __future__ import annotations

import logging
from unittest import mock

import pytest
from airflow.exceptions import AirflowException
from airflow.utils.task_group import TaskGroup
from astro_databricks.operators.notebook import DatabricksNotebookOperator
from astro_databricks.operators.workflow import DatabricksWorkflowTaskGroup
from astro_databricks.settings import DATABRICKS_JOBS_API_VERSION

expected_workflow_json = {
    "name": "unit_test_dag.test_workflow",
    "email_notifications": {"no_alert_for_skipped_runs": False},
    "format": "MULTI_TASK",
    "job_clusters": [{"job_cluster_key": "foo"}],
    "max_concurrent_runs": 1,
    "tasks": [
        {
            "depends_on": [],
            "email_notifications": {},
            "job_cluster_key": "foo",
            "libraries": [
                {"nb_index": {"package": "nb_package"}},
                {"tg_index": {"package": "tg_package"}},
            ],
            "notebook_task": {
                "base_parameters": {"notebook_path": "/foo/bar"},
                "notebook_path": "/foo/bar",
                "source": "WORKSPACE",
            },
            "task_key": "unit_test_dag__test_workflow__notebook_1",
            "timeout_seconds": 0,
        },
        {
            "depends_on": [{"task_key": "unit_test_dag__test_workflow__notebook_1"}],
            "email_notifications": {},
            "job_cluster_key": "foo",
            "libraries": [{"tg_index": {"package": "tg_package"}}],
            "notebook_task": {
                "base_parameters": {"foo": "bar", "notebook_path": "/foo/bar"},
                "notebook_path": "/foo/bar",
                "source": "WORKSPACE",
            },
            "task_key": "unit_test_dag__test_workflow__notebook_2",
            "timeout_seconds": 0,
        },
    ],
    "timeout_seconds": 0,
}


@mock.patch("astro_databricks.operators.workflow.DatabricksHook")
@mock.patch("astro_databricks.operators.workflow.ApiClient")
@mock.patch("astro_databricks.operators.workflow.JobsApi")
@mock.patch(
    "astro_databricks.operators.workflow.RunsApi.get_run",
    return_value={"state": {"life_cycle_state": "SKIPPED"}},
)
def test_create_workflow_from_notebooks_raises_exception_due_to_job_being_skipped(
    mock_run_api, mock_jobs_api, mock_api, mock_hook, dag
):
    mock_jobs_api.return_value.create_job.return_value = {"job_id": 1}
    with dag:
        task_group = DatabricksWorkflowTaskGroup(
            group_id="test_workflow",
            databricks_conn_id="foo",
            job_clusters=[{"job_cluster_key": "foo"}],
            notebook_params={"notebook_path": "/foo/bar"},
            notebook_packages=[{"tg_index": {"package": "tg_package"}}],
        )
        with task_group:
            notebook_1 = DatabricksNotebookOperator(
                task_id="notebook_1",
                databricks_conn_id="foo",
                notebook_path="/foo/bar",
                notebook_packages=[{"nb_index": {"package": "nb_package"}}],
                source="WORKSPACE",
                job_cluster_key="foo",
            )
            notebook_2 = DatabricksNotebookOperator(
                task_id="notebook_2",
                databricks_conn_id="foo",
                notebook_path="/foo/bar",
                source="WORKSPACE",
                job_cluster_key="foo",
                notebook_params={
                    "foo": "bar",
                },
            )
            notebook_1 >> notebook_2

    assert len(task_group.children) == 3
    with pytest.raises(AirflowException) as exc_info:
        task_group.children["test_workflow.launch"].execute(context={})
    assert (
        str(exc_info.value) == "Could not start the workflow job, it had state SKIPPED"
    )


@mock.patch("astro_databricks.operators.workflow.DatabricksHook")
@mock.patch("astro_databricks.operators.workflow.ApiClient")
@mock.patch("astro_databricks.operators.workflow.JobsApi")
@mock.patch(
    "astro_databricks.operators.workflow.RunsApi.get_run",
    return_value={"state": {"life_cycle_state": "RUNNING"}},
)
def test_create_workflow_from_notebooks_with_create(
    mock_run_api, mock_jobs_api, mock_api, mock_hook, dag
):
    mock_jobs_api.return_value.create_job.return_value = {"job_id": 1}
    with dag:
        task_group = DatabricksWorkflowTaskGroup(
            group_id="test_workflow",
            databricks_conn_id="foo",
            job_clusters=[{"job_cluster_key": "foo"}],
            notebook_params={"notebook_path": "/foo/bar"},
            notebook_packages=[{"tg_index": {"package": "tg_package"}}],
        )
        with task_group:
            notebook_1 = DatabricksNotebookOperator(
                task_id="notebook_1",
                databricks_conn_id="foo",
                notebook_path="/foo/bar",
                notebook_packages=[{"nb_index": {"package": "nb_package"}}],
                source="WORKSPACE",
                job_cluster_key="foo",
            )
            notebook_2 = DatabricksNotebookOperator(
                task_id="notebook_2",
                databricks_conn_id="foo",
                notebook_path="/foo/bar",
                source="WORKSPACE",
                job_cluster_key="foo",
                notebook_params={
                    "foo": "bar",
                },
            )
            notebook_1 >> notebook_2

    assert len(task_group.children) == 3
    task_group.children["test_workflow.launch"].execute(context={})
    mock_jobs_api.return_value.create_job.assert_called_once_with(
        json=expected_workflow_json,
        version=DATABRICKS_JOBS_API_VERSION,
    )
    mock_jobs_api.return_value.run_now.assert_called_once_with(
        job_id=1,
        jar_params=[],
        notebook_params={"notebook_path": "/foo/bar"},
        python_params=[],
        spark_submit_params=[],
        version=DATABRICKS_JOBS_API_VERSION,
    )


@mock.patch("astro_databricks.operators.workflow.DatabricksHook")
@mock.patch("astro_databricks.operators.workflow.ApiClient")
@mock.patch("astro_databricks.operators.workflow._get_job_by_name")
@mock.patch(
    "astro_databricks.operators.workflow.RunsApi.get_run",
    side_effect=[
        {"state": {"life_cycle_state": "BLOCKED"}},
        {"state": {"life_cycle_state": "BLOCKED"}},
        {"state": {"life_cycle_state": "RUNNING"}},
    ],
)
@mock.patch("astro_databricks.operators.workflow.JobsApi.run_now")
@mock.patch("astro_databricks.operators.workflow.JobsApi.create_job")
def test_create_workflow_from_notebooks_job_templates_notebook_jobs(
    mock_create_job,
    mock_run_now,
    mock_get_run,
    mock_get_jobs,
    mock_api,
    mock_hook,
    dag,
    caplog,
):
    mock_get_jobs.return_value = {"job_id": None}
    caplog.set_level(logging.INFO)
    with dag:
        task_group = DatabricksWorkflowTaskGroup(
            group_id="test_workflow",
            databricks_conn_id="foo",
            job_clusters=[{"job_cluster_key": "foo"}],
            notebook_params={"notebook_path": "/foo/bar", "ts": "{{ ts }}"},
            notebook_packages=[{"tg_index": {"package": "tg_package"}}],
        )
        with task_group:
            notebook_1 = DatabricksNotebookOperator(
                task_id="notebook_1",
                databricks_conn_id="foo",
                notebook_path="/foo/bar",
                notebook_packages=[{"nb_index": {"package": "nb_package"}}],
                notebook_params={"ds": "{{ ds }}"},
                source="WORKSPACE",
                job_cluster_key="foo",
            )

            notebook_1

    assert len(task_group.children) == 2
    context = {
        "ds": "yyyy-mm-dd",
        "ts": "hh:mm",
        "ti": mock.MagicMock(),
        "expanded_ti_count": 0,
    }
    task_group.children["test_workflow.launch"].execute(context=context)
    assert mock_get_run.call_count == 3
    assert "Job state: BLOCKED" in caplog.messages

    notebook_job_parameters = mock_create_job.call_args.kwargs["json"]["tasks"][0][
        "notebook_task"
    ]["base_parameters"]
    assert notebook_job_parameters["ds"] == "yyyy-mm-dd"
    assert notebook_job_parameters["ts"] == "hh:mm"


@mock.patch("astro_databricks.operators.workflow.DatabricksHook")
@mock.patch("astro_databricks.operators.workflow.ApiClient")
@mock.patch("astro_databricks.operators.workflow.JobsApi")
@mock.patch("astro_databricks.operators.workflow._get_job_by_name")
@mock.patch(
    "astro_databricks.operators.workflow.RunsApi.get_run",
    return_value={"state": {"life_cycle_state": "RUNNING"}},
)
def test_create_workflow_with_arbitrary_extra_job_params(
    mock_run_api, mock_get_jobs, mock_jobs_api, mock_api, mock_hook, dag
):
    mock_get_jobs.return_value = {"job_id": 862519602273592}

    extra_job_params = {
        "timeout_seconds": 10,  # default: 0
        "webhook_notifications": {
            "on_failure": [{"id": "b0aea8ab-ea8c-4a45-a2e9-9a26753fd702"}],
        },
        "email_notifications": {
            "no_alert_for_skipped_runs": True,  # default: False
            "on_start": ["user.name@databricks.com"],
        },
        "git_source": {  # no default value
            "git_url": "https://github.com/astronomer/astro-provider-databricks",
            "git_provider": "gitHub",
            "git_branch": "main",
        },
    }
    with dag:
        task_group = DatabricksWorkflowTaskGroup(
            group_id="test_workflow",
            databricks_conn_id="foo",
            job_clusters=[{"job_cluster_key": "foo"}],
            notebook_params={"notebook_path": "/foo/bar"},
            extra_job_params=extra_job_params,
        )
        with task_group:
            notebook_with_extra = DatabricksNotebookOperator(
                task_id="notebook_with_extra",
                databricks_conn_id="foo",
                notebook_path="/foo/bar",
                source="WORKSPACE",
                job_cluster_key="foo",
            )
            notebook_with_extra

    assert len(task_group.children) == 2

    task_group.children["test_workflow.launch"].create_workflow_json()
    task_group.children["test_workflow.launch"].execute(context={})

    mock_jobs_api.return_value.reset_job.assert_called_once()
    kwargs = mock_jobs_api.return_value.reset_job.call_args_list[0].kwargs["json"]

    assert kwargs["job_id"] == 862519602273592
    assert (
        kwargs["new_settings"]["email_notifications"]
        == extra_job_params["email_notifications"]
    )
    assert (
        kwargs["new_settings"]["timeout_seconds"] == extra_job_params["timeout_seconds"]
    )
    assert kwargs["new_settings"]["git_source"] == extra_job_params["git_source"]
    assert (
        kwargs["new_settings"]["webhook_notifications"]
        == extra_job_params["webhook_notifications"]
    )
    assert (
        kwargs["new_settings"]["email_notifications"]
        == extra_job_params["email_notifications"]
    )


@mock.patch("astro_databricks.operators.workflow.DatabricksHook")
@mock.patch("astro_databricks.operators.workflow.ApiClient")
@mock.patch("astro_databricks.operators.workflow.JobsApi")
@mock.patch("astro_databricks.operators.workflow._get_job_by_name")
@mock.patch(
    "astro_databricks.operators.workflow.RunsApi.get_run",
    return_value={"state": {"life_cycle_state": "RUNNING"}},
)
def test_create_workflow_with_nested_task_groups(
    mock_run_api, mock_get_jobs, mock_jobs_api, mock_api, mock_hook, dag
):
    mock_get_jobs.return_value = {"job_id": 862519602273592}

    extra_job_params = {
        "timeout_seconds": 10,  # default: 0
        "webhook_notifications": {
            "on_failure": [{"id": "b0aea8ab-ea8c-4a45-a2e9-9a26753fd702"}],
        },
        "email_notifications": {
            "no_alert_for_skipped_runs": True,  # default: False
            "on_start": ["user.name@databricks.com"],
        },
        "git_source": {  # no default value
            "git_url": "https://github.com/astronomer/astro-provider-databricks",
            "git_provider": "gitHub",
            "git_branch": "main",
        },
    }
    with dag:
        outer_task_group = DatabricksWorkflowTaskGroup(
            group_id="test_workflow",
            databricks_conn_id="foo",
            job_clusters=[{"job_cluster_key": "foo"}],
            notebook_params={"notebook_path": "/foo/bar"},
            extra_job_params=extra_job_params,
            notebook_packages=[
                {"pypi": {"package": "mlflow==2.4.0"}},
            ],
        )
        with outer_task_group:
            direct_notebook = DatabricksNotebookOperator(
                task_id="direct_notebook",
                databricks_conn_id="foo",
                notebook_path="/foo/bar",
                source="WORKSPACE",
                job_cluster_key="foo",
            )

            with TaskGroup("middle_task_group") as middle_task_group:
                with TaskGroup("inner_task_group") as inner_task_group:
                    inner_notebook = DatabricksNotebookOperator(
                        task_id="inner_notebook",
                        databricks_conn_id="foo",
                        notebook_path="/foo/bar",
                        source="WORKSPACE",
                        job_cluster_key="foo",
                    )
                    inner_notebook
                inner_task_group
            direct_notebook >> middle_task_group

    assert len(outer_task_group.children) == 3

    outer_task_group.children["test_workflow.launch"].create_workflow_json()
    outer_task_group.children["test_workflow.launch"].execute(context={})

    kwargs = mock_jobs_api.return_value.reset_job.call_args_list[0].kwargs["json"]

    inner_notebook_json = kwargs["new_settings"]["tasks"][0]
    outer_notebook_json = kwargs["new_settings"]["tasks"][1]

    assert (
        inner_notebook_json["task_key"]
        == "unit_test_dag__test_workflow__direct_notebook"
    )
    assert inner_notebook_json["libraries"] == [{"pypi": {"package": "mlflow==2.4.0"}}]

    assert (
        outer_notebook_json["task_key"]
        == "unit_test_dag__test_workflow__middle_task_group__inner_task_group__inner_notebook"
    )
    assert outer_notebook_json["libraries"] == [{"pypi": {"package": "mlflow==2.4.0"}}]
