from airflow.providers.databricks.operators.databricks import (
    DatabricksNotebookOperator as UpstreamDatabricksNotebookOperator,
)
from astro_databricks.operators.notebook import DatabricksNotebookOperator


def test_init():
    operator = DatabricksNotebookOperator(
        task_id="notebook",
        databricks_conn_id="foo",
        notebook_path="/foo/bar",
        source="WORKSPACE",
        job_cluster_key="foo",
        notebook_params={
            "foo": "bar",
        },
        notebook_packages=[{"nb_index": {"package": "nb_package"}}],
        existing_cluster_id="123",
    )

    assert isinstance(operator, UpstreamDatabricksNotebookOperator)
