from __future__ import annotations

from airflow.providers.databricks.plugins.databricks_workflow import (
    DatabricksWorkflowPlugin as UpstreamDatabricksWorkflowPlugin,
    RepairDatabricksTasks as UpstreamRepairDatabricksTasks,
    WorkflowJobRepairAllFailedLink,
    WorkflowJobRepairSingleTaskLink,
    WorkflowJobRunLink,
)
from astro_databricks.plugins.plugin import (
    DatabricksJobRepairAllFailedLink,
    DatabricksJobRepairSingleFailedLink,
    DatabricksJobRunLink,
    DatabricksWorkflowPlugin,
    RepairDatabricksTasks,
)


def test_databricks_job_run_link_init():
    link = DatabricksJobRunLink()

    assert isinstance(link, WorkflowJobRunLink)


def test_repair_all_get_link_init():
    link = DatabricksJobRepairAllFailedLink()

    assert isinstance(link, WorkflowJobRepairAllFailedLink)


def test_databricks_job_repair_single_failed_link_init():
    link = DatabricksJobRepairSingleFailedLink()

    assert isinstance(link, WorkflowJobRepairSingleTaskLink)


def test_repair_databricks_task_init():
    repair_databricks_task = RepairDatabricksTasks()

    assert isinstance(repair_databricks_task, UpstreamRepairDatabricksTasks)


def test_plugin_init():
    plugin = DatabricksWorkflowPlugin()

    assert isinstance(plugin, UpstreamDatabricksWorkflowPlugin)
