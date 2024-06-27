"""Example DAG for using the DatabricksNotebookOperator."""
import os
from datetime import timedelta

from airflow.models.dag import DAG
from airflow.utils.timezone import datetime
from astro_databricks import DatabricksNotebookOperator

EXECUTION_TIMEOUT = int(os.getenv("EXECUTION_TIMEOUT", 6))
default_args = {
    "execution_timeout": timedelta(hours=EXECUTION_TIMEOUT),
    # Users are encouraged to use the repair feature, retries may fail:
    "retries": int(os.getenv("DEFAULT_TASK_RETRIES", 0)),
    "retry_delay": timedelta(seconds=int(os.getenv("DEFAULT_RETRY_DELAY_SECONDS", 60))),
}

DATABRICKS_CONN_ID = os.getenv("ASTRO_DATABRICKS_CONN_ID", "databricks_conn")
NEW_CLUSTER_SPEC = {
    "cluster_name": "",
    "spark_version": "11.3.x-scala2.12",
    "node_type_id": "Standard_DS3_v2",
    "spark_env_vars": {"PYSPARK_PYTHON": "/databricks/python3/bin/python3"},
    "enable_elastic_disk": False,
    "data_security_mode": "LEGACY_SINGLE_USER_STANDARD",
    "runtime_engine": "STANDARD",
    "num_workers": 8,
}
USER = os.environ.get("USER")

dag = DAG(
    dag_id=f"example_databricks_notebook_{USER}",
    start_date=datetime(2022, 1, 1),
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags=["example", "async", "databricks"],
)
with dag:
    notebook_1 = DatabricksNotebookOperator(
        task_id="notebook_1",
        databricks_conn_id=DATABRICKS_CONN_ID,
        notebook_path="/Shared/Notebook_1",
        notebook_packages=[
            {
                "pypi": {
                    "package": "simplejson==3.18.0",
                    "repo": "https://pypi.org/simple",
                }
            },
            {"pypi": {"package": "Faker"}},
        ],
        source="WORKSPACE",
        new_cluster=NEW_CLUSTER_SPEC,
    )
