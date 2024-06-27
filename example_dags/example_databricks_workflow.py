"""Example DAG for using the DatabricksWorkflowTaskGroup and DatabricksNotebookOperator."""
import os
from datetime import timedelta

from airflow.models.dag import DAG
from airflow.utils.timezone import datetime
from astro_databricks import DatabricksNotebookOperator, DatabricksWorkflowTaskGroup

EXECUTION_TIMEOUT = int(os.getenv("EXECUTION_TIMEOUT", 6))
default_args = {
    "execution_timeout": timedelta(hours=EXECUTION_TIMEOUT),
    # Users are encouraged to use the repair feature, retries may fail:
    "retries": int(os.getenv("DEFAULT_TASK_RETRIES", 0)),
    "retry_delay": timedelta(seconds=int(os.getenv("DEFAULT_RETRY_DELAY_SECONDS", 60))),
}

DATABRICKS_CONN_ID = os.getenv("ASTRO_DATABRICKS_CONN_ID", "databricks_conn")

# DATABRICKS_NOTIFICATION_EMAIL = os.getenv(
#     "ASTRO_DATABRICKS_NOTIFICATION_EMAIL", "tatiana.alchueyr@astronomer.io"
# )
DATABRICKS_DESTINATION_ID = os.getenv(
    "ASTRO_DATABRICKS_DESTINATION_ID", "48c7315c-1d65-4ee3-b7d3-1692e8e8012d"
)

USER = os.environ.get("USER")
GROUP_ID = os.getenv("DATABRICKS_GROUP_ID", "1234").replace(".", "_")
USER = os.environ.get("USER")

job_cluster_spec = [
    {
        "job_cluster_key": "Shared_job_cluster",
        "new_cluster": {
            "cluster_name": "",
            "spark_version": "11.3.x-scala2.12",
            "node_type_id": "Standard_DS3_v2",
            "spark_env_vars": {"PYSPARK_PYTHON": "/databricks/python3/bin/python3"},
            "enable_elastic_disk": False,
            "data_security_mode": "LEGACY_SINGLE_USER_STANDARD",
            "runtime_engine": "STANDARD",
            "num_workers": 8,
        },
    }
]
dag = DAG(
    dag_id="example_databricks_workflow",
    start_date=datetime(2022, 1, 1),
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags=["example", "async", "databricks"],
)
with dag:
    # [START howto_databricks_workflow_notebook]
    task_group = DatabricksWorkflowTaskGroup(
        group_id=f"test_workflow_{USER}_{GROUP_ID}",
        databricks_conn_id=DATABRICKS_CONN_ID,
        job_clusters=job_cluster_spec,
        notebook_params={"ts": "{{ ts }}"},
        notebook_packages=[
            {
                "pypi": {
                    "package": "simplejson==3.18.0",  # Pin specification version of a package like this.
                    "repo": "https://pypi.org/simple",  # You can specify your required Pypi index here.
                }
            },
        ],
        extra_job_params={
            ## Commented below to avoid spam; keeping this for example purposes.
            # "email_notifications": {
            #     "on_start": [DATABRICKS_NOTIFICATION_EMAIL],
            # },
            "webhook_notifications": {
                "on_start": [{"id": DATABRICKS_DESTINATION_ID}],
            },
        },
    )
    with task_group:
        notebook_1 = DatabricksNotebookOperator(
            task_id="notebook_1",
            databricks_conn_id=DATABRICKS_CONN_ID,
            notebook_path="/Shared/Notebook_1",
            notebook_packages=[{"pypi": {"package": "Faker"}}],
            source="WORKSPACE",
            job_cluster_key="Shared_job_cluster",
            execution_timeout=timedelta(seconds=600),
        )
        notebook_2 = DatabricksNotebookOperator(
            task_id="notebook_2",
            databricks_conn_id=DATABRICKS_CONN_ID,
            notebook_path="/Shared/Notebook_2",
            source="WORKSPACE",
            job_cluster_key="Shared_job_cluster",
            notebook_params={"foo": "bar", "ds": "{{ ds }}"},
        )
        notebook_1 >> notebook_2
    # [END howto_databricks_workflow_notebook]
