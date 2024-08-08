from airflow.providers.databricks.operators.databricks import (
    DatabricksTaskOperator as UpstreamDatabricksTaskOperator,
)
from astro_databricks.operators.common import DatabricksTaskOperator


def test_init():
    operator = DatabricksTaskOperator(
        task_id="test_task",
        databricks_conn_id="foo",
        job_cluster_key="foo",
        task_config={
            "notebook_task": {
                "notebook_path": "foo",
                "source": "WORKSPACE",
                "base_parameters": {
                    "foo": "bar",
                },
            },
        },
    )

    assert isinstance(operator, UpstreamDatabricksTaskOperator)
