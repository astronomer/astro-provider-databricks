from __future__ import annotations

from airflow.providers.databricks.operators.databricks_workflow import (
    DatabricksWorkflowTaskGroup as UpstreamDatabricksWorkflowTaskGroup,
)
from astro_databricks.operators.workflow import DatabricksWorkflowTaskGroup


def test_workflow_init(dag):
    with dag:
        task_group = DatabricksWorkflowTaskGroup(
            group_id="test_workflow",
            databricks_conn_id="foo",
            job_clusters=[{"job_cluster_key": "foo"}],
            notebook_params={"notebook_path": "/foo/bar"},
            notebook_packages=[{"tg_index": {"package": "tg_package"}}],
        )

    assert isinstance(task_group, UpstreamDatabricksWorkflowTaskGroup)
