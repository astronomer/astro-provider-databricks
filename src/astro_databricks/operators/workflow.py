"""
This module is deprecated and will be removed in future versions.
Please use `airflow.providers.databricks.operators.databricks.DatabricksWorkflowTaskGroup` instead.
"""
from __future__ import annotations

from typing import Any

from airflow.providers.databricks.operators.databricks_workflow import (
    DatabricksWorkflowTaskGroup as UpstreamDatabricksWorkflowTaskGroup,
)


class DatabricksWorkflowTaskGroup(UpstreamDatabricksWorkflowTaskGroup):
    """
    This class is deprecated and will be removed in future versions.
    Please use `airflow.providers.databricks.operators.databricks.DatabricksWorkflowTaskGroup` instead.
    """

    def __init__(self, *args: Any, **kwargs: Any):
        """
        This class is deprecated and will be removed in future versions.
        Please use `airflow.providers.databricks.operators.databricks.DatabricksWorkflowTaskGroup` instead.
        """
        super().__init__(*args, **kwargs)
