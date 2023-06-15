import os
from datetime import datetime

from airflow.decorators import dag, task_group
from airflow.utils.task_group import TaskGroup

from astro_databricks.operators.notebook import DatabricksNotebookOperator
from astro_databricks.operators.workflow import DatabricksWorkflowTaskGroup


DATABRICKS_CONN = "databricks_conn"
USER = os.environ.get("USER")
GROUP_ID = os.getenv("DATABRICKS_GROUP_ID", "1234").replace(".", "_")
USER = os.environ.get("USER")
job_clusters = [
    {
        "job_cluster_key": "Shared_job_cluster",
        "new_cluster": {
            "cluster_name": "",
            "spark_version": "11.3.x-scala2.12",
            "aws_attributes": {
                "first_on_demand": 1,
                "availability": "SPOT_WITH_FALLBACK",
                "zone_id": "us-east-2b",
                "spot_bid_price_percent": 100,
                "ebs_volume_count": 0,
            },
            "node_type_id": "i3.xlarge",
            "spark_env_vars": {"PYSPARK_PYTHON": "/databricks/python3/bin/python3"},
            "enable_elastic_disk": False,
            "data_security_mode": "LEGACY_SINGLE_USER_STANDARD",
            "runtime_engine": "STANDARD",
            "num_workers": 8,
        },
    }
]


@dag(
    schedule_interval="@daily",
    start_date=datetime(2021, 1, 1),
    catchup=False,
    default_args={'retries': 0},  # Users are encouraged to use the repair feature, retries may fail
    tags=["astro-provider-databricks"],
)
def example_task_group():
    databricks_task_group = DatabricksWorkflowTaskGroup(
        group_id=f"example_task_group_{USER}_{GROUP_ID}",
        databricks_conn_id=DATABRICKS_CONN,
        job_clusters=job_clusters,
        notebook_packages=[{"pypi": {"package": "simplejson"}}],
    )
    with databricks_task_group:
        nb_1 = DatabricksNotebookOperator(
            task_id="nb_1",
            databricks_conn_id=DATABRICKS_CONN,
            notebook_path="/Shared/Notebook_1",
            source="WORKSPACE",
            job_cluster_key="Shared_job_cluster",
            notebook_packages=[{"pypi": {"package": "Faker"}}],
        )

        with TaskGroup("my_task_group") as my_task_group:
            DatabricksNotebookOperator(
                task_id="nb_2",
                databricks_conn_id=DATABRICKS_CONN,
                notebook_path="/Shared/Notebook_2",
                source="WORKSPACE",
                job_cluster_key="Shared_job_cluster",
            )

            DatabricksNotebookOperator(
                task_id="nb_3",
                databricks_conn_id=DATABRICKS_CONN,
                notebook_path="/Shared/Notebook_3",
                source="WORKSPACE",
                job_cluster_key="Shared_job_cluster",
            )

        nb_4 = DatabricksNotebookOperator(
            task_id="nb_4",
            databricks_conn_id=DATABRICKS_CONN,
            notebook_path="/Shared/Notebook_4",
            source="WORKSPACE",
            job_cluster_key="Shared_job_cluster",
        )

        nb_1 >> my_task_group >> nb_4


example_task_group()
