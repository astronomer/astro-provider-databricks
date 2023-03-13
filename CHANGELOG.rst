Changelog
=========

0.1.0 (2023-03-10)
-------------------

Features

* **DatabricksWorkflowTaskGroup**: Airflow `Task Group <https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#taskgroups>`_ that allows users to create a `Databricks Workflow <https://www.databricks.com/product/workflows>`_.
* **DatabricksNotebookOperator**: Airflow `Operator <https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/operators.html>`_ which abstracts a pre-existing `Databricks Notebook <https://docs.databricks.com/notebooks/>`_. Can be used independently to run the Notebook, or within a Databricks Workflow Task Group.
* **AstroDatabricksPlugin**: An Airflow `Plugin <https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/plugins.html>`_ which is installed by the default. It allows users, by using the UI, to view a Databricks job and retry running it in case of failure.

Known limitations

* Cancelling the Airflow task does not stop its execution in Databricks (issue `#1 <https://github.com/astronomer/astro-provider-databricks/issues/1>`_).
* Users should not click the buttons "repair all" or "repair single task" while the DAG/task is running (issue `#2 <https://github.com/astronomer/astro-provider-databricks/issues/2>`_).

