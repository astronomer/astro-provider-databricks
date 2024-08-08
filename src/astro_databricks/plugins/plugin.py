"""
This module is deprecated and will be removed in future versions.
Please use `airflow.providers.databricks.plugins.databricks_workflow.DatabricksWorkflowPlugin` instead.
"""
from __future__ import annotations

from typing import Any

from airflow.providers.databricks.plugins.databricks_workflow import (
    DatabricksWorkflowPlugin,
    RepairDatabricksTasks as UpstreamRepairDatabricksTasks,
    WorkflowJobRepairAllFailedLink,
    WorkflowJobRepairSingleTaskLink,
    WorkflowJobRunLink,
)
from airflow.utils.log.logging_mixin import LoggingMixin


class DatabricksJobRunLink(WorkflowJobRunLink, LoggingMixin):
    """
    This class is deprecated and will be removed in future versions.
    Please use `airflow.providers.databricks.plugins.databricks_workflow.WorkflowJobRunLink` instead.
    """

    def __init__(self, *args: Any, **kwargs: Any):
        self.log.warning(
            "DatabricksJobRunLink is deprecated and will be removed in future versions. "
            "Please use `airflow.providers.databricks.plugins.databricks_workflow.WorkflowJobRunLink` instead."
        )
        super().__init__(*args, **kwargs)


class DatabricksJobRepairAllFailedLink(WorkflowJobRepairAllFailedLink, LoggingMixin):
    """
    This class is deprecated and will be removed in future versions.
    Please use `airflow.providers.databricks.plugins.databricks_workflow.WorkflowJobRepairAllFailedLink` instead.
    """

    def __init__(self, *args: Any, **kwargs: Any):
        self.log.warning(
            "DatabricksJobRepairAllFailedLink is deprecated and will be removed in future versions. "
            "Please use "
            "`airflow.providers.databricks.plugins.databricks_workflow.WorkflowJobRepairAllFailedLink` instead."
        )
        super().__init__(*args, **kwargs)


class DatabricksJobRepairSingleFailedLink(
    WorkflowJobRepairSingleTaskLink, LoggingMixin
):
    """
    This class is deprecated and will be removed in future versions.
    Please use `airflow.providers.databricks.plugins.databricks_workflow.WorkflowJobRepairSingleTaskLink` instead.
    """

    def __init__(self, *args: Any, **kwargs: Any):
        self.log.warning(
            "DatabricksJobRepairSingleFailedLink is deprecated and will be removed in future versions. "
            "Please use "
            "`airflow.providers.databricks.plugins.databricks_workflow.WorkflowJobRepairSingleTaskLink` instead."
        )
        super().__init__(*args, **kwargs)


class RepairDatabricksTasks(UpstreamRepairDatabricksTasks, LoggingMixin):
    def __init__(self, *args: Any, **kwargs: Any):
        self.log.warning(
            "RepairDatabricksTasks is deprecated and will be removed in future versions. "
            "Please use `airflow.providers.databricks.plugins.databricks_workflow.RepairDatabricksTasks` instead."
        )
        super().__init__(*args, **kwargs)


repair_databricks_view = RepairDatabricksTasks()

repair_databricks_package = {
    "name": "Repair Databricks View",
    "category": "Repair Databricks Plugin",
    "view": repair_databricks_view,
}


class AstroDatabricksPlugin(DatabricksWorkflowPlugin, LoggingMixin):
    def __init__(self, *args: Any, **kwargs: Any):
        self.log.warning(
            "AstroDatabricksPlugin is deprecated and will be removed in future versions. "
            "Please use `airflow.providers.databricks.plugins.databricks_workflow.DatabricksWorkflowPlugin` instead."
        )

        super().__init__(*args, **kwargs)
