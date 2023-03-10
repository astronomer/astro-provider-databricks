Changelog
=========

0.1.0 (2023-03-10)
-------------------

Features

* **DatabricksWorkflowTaskGroup**: Airflow `Task Group <https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#taskgroups>`_ that allows users to create a `Databricks Workflow <https://www.databricks.com/product/workflows>`_.
* **DatabricksNotebookOperator**: Airflow `Operator <https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/operators.html>`_ which abstracts a pre-existing `Databricks Notebook <https://docs.databricks.com/notebooks/>`_. Can be used independently to run the Notebook, or within a Databricks Workflow Task Group.
* **AstroDatabricksPlugin**: An Airflow `Plugin <https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/plugins.html>`_ which is installed by the default. It allows users, by using the UI, to view a Databricks job and retry running it in case of failure.

Known limitations

* Cancelling the Airflow task does not stop its execution in Databricks (issue `#1 <https://github.com/astronomer/astro-providers-databricks/issues/1>`_).
* Users should not click the buttons "repair all" or "repair single task" while the DAG/task is running (issue `#2 <https://github.com/astronomer/astro-providers-databricks/issues/2>`_).
* Users need to enable XCom pickling for Airflow versions older than 2.5. This happens because the **DatabricksNotebookOperator** uses **DatabricksMetaData** to store information about the Databricks Job, so that the plugin **AstroDatabricksPlugin** can use it for retrying failed tasks. One of the ways of achieving this is:

.. code-block::
    AIRFLOW__CORE__ENABLE_XCOM_PICKLING="True"

.. note::
    Starting with Airflow 2.0.0, the pickle type for XCom messages has been replaced to JSON by default to prevent
    RCE attacks and the default value for **[core] enable_xom_pickling** has been set to False.
    Read more `here <http://apache-airflow-docs.s3-website.eu-central-1.amazonaws.com/docs/apache-airflow/latest/release_notes.html#the-default-value-for-core-enable-xcom-pickling-has-been-changed-to-false>`_.
    However, serialization of objects that contain attr, dataclass or custom serializer into JSON are supported
    starting in `Airflow 2.5.0 <https://github.com/apache/airflow/pull/27540>`_. Hence, users should enable XCom Pickling if
    using an older versions of Airflow, .
