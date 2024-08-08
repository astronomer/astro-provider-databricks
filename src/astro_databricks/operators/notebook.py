"""
This module is deprecated and will be removed in future versions.
Please use `airflow.providers.databricks.operators.databricks.DatabricksNotebookOperator` instead.
"""
from __future__ import annotations

from typing import Any

from airflow.providers.databricks.operators.databricks import (
    DatabricksNotebookOperator as UpstreamDatabricksNotebookOperator,
)


class DatabricksNotebookOperator(UpstreamDatabricksNotebookOperator):
    """
    This class is deprecated and will be removed in future versions.
    Please use `airflow.providers.databricks.operators.databricks.DatabricksNotebookOperator` instead.
    """

    def __init__(self, *args: Any, **kwargs: Any):
        self.log.warning(
            "DatabricksNotebookOperator is deprecated and will be removed in future versions."
            "Please use `airflow.providers.databricks.operators.databricks.DatabricksNotebookOperator` instead."
        )
        super().__init__(*args, **kwargs)
