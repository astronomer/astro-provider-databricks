"""
This module is deprecated and will be removed in future versions.
Please use `airflow.providers.databricks.operators.databricks.DatabricksTaskOperator` instead.
"""
from __future__ import annotations

from typing import Any

from airflow.providers.databricks.operators.databricks import (
    DatabricksTaskOperator as UpstreamDatabricksTaskOperator,
)


class DatabricksTaskOperator(UpstreamDatabricksTaskOperator):
    """
    This class is deprecated and will be removed in future versions.
    Please use `airflow.providers.databricks.operators.databricks.DatabricksTaskOperator` instead.
    """

    def __init__(self, *args: Any, **kwargs: Any):
        self.log.warning(
            "DatabricksTaskOperator is deprecated and will be removed in future versions. "
            "Please use `airflow.providers.databricks.operators.databricks.DatabricksTaskOperator` instead."
        )
        super().__init__(*args, **kwargs)
