Changelog
=========

0.2.0 (20-03-24)
----------------

Feature

* Allow users to specify Databricks API version via an environment variable (PR `#66 <https://github.com/astronomer/astro-provider-databricks/pull/66>`_ by @pankajkoti)


0.1.6 (23-02-24)
----------------

Bug fixes

* Bump ``pydantic`` to ``>=1.10.0`` to be compatible with Airflow 2.7.0+ (PR `#61 <https://github.com/astronomer/astro-provider-databricks/pull/61>`_ by @w0ut0)


0.1.5 (31-07-23)
----------------

Feature

* Add operator that supports all task types (PR `#55 <https://github.com/astronomer/astro-provider-databricks/pull/55>`_ by @crong-k)

Bug fixes

* Limit Pydantic < 2.0.0 until Airflow resolves incompatibilities (PR `#52 <https://github.com/astronomer/astro-provider-databricks/pull/42>`_ by @tatiana)

Enhancements

* Update query ID to hello world query (PR `#56 <https://github.com/astronomer/astro-provider-databricks/pull/56>`_ by @jlaneve)

0.1.4 (23-06-16)
----------------

Bug fixes

* Fix repairing tasks declared in inner task groups (PR `#49 <https://github.com/astronomer/astro-provider-databricks/pull/49>`_ by @tatiana)
* Fix copying dependencies from task groups to tasks inside intermediate task groups (PR `#47 <https://github.com/astronomer/astro-provider-databricks/pull/47>`_ by @tatiana)


Enhancements

* Documentation improvements (PRs `#43 <https://github.com/astronomer/astro-provider-databricks/pull/43>`_ and `#44 <https://github.com/astronomer/astro-provider-databricks/pull/44>`_ by @jlaneve)


0.1.3 (23-04-27)
----------------

Enhancements

* Associate a **DatabricksNotebookOperator** to a **DatabricksWorkflowTaskGroup** even if there are up to three levels **TaskGroups** in between (issue `#29 <https://github.com/astronomer/astro-provider-databricks/issues/29>`_)
* Support templating the field **notebook_params** of the **DatabricksNotebookOperator**  (issue `#33 <https://github.com/astronomer/astro-provider-databricks/issues/33>`_)
* Extend **notebook_params** of the **DatabricksNotebookOperator** with the values defined in **DatabricksWorkflowTaskGroup** (issue `#33 <https://github.com/astronomer/astro-provider-databricks/issues/33>`_)
* Improve example DAGs  (issue `#29 <https://github.com/astronomer/astro-provider-databricks/issues/29>`_)
* Overall README improvements (pull requests `#23 <https://github.com/astronomer/astro-provider-databricks/pull/23>`_ and `#24 <https://github.com/astronomer/astro-provider-databricks/pulls/24>`_)


0.1.1 (23-03-13)
----------------

Enhancements

* **DatabricksWorkflowTaskGroup** and **DatabricksNotebookOperator** log the Databricks Job URL  (issue `#20 <https://github.com/astronomer/astro-provider-databricks/issues/20>`_)
* README improvement  (issue `#21 <https://github.com/astronomer/astro-provider-databricks/issues/21>`_)


0.1.0 (2023-03-10)
-------------------

Features

* **DatabricksWorkflowTaskGroup**: Airflow `Task Group <https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#taskgroups>`_ that allows users to create a `Databricks Workflow <https://www.databricks.com/product/workflows>`_.
* **DatabricksNotebookOperator**: Airflow `Operator <https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/operators.html>`_ which abstracts a pre-existing `Databricks Notebook <https://docs.databricks.com/notebooks/>`_. Can be used independently to run the Notebook, or within a Databricks Workflow Task Group.
* **AstroDatabricksPlugin**: An Airflow `Plugin <https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/plugins.html>`_ which is installed by the default. It allows users, by using the UI, to view a Databricks job and retry running it in case of failure.

Known limitations

* Cancelling the Airflow task does not stop its execution in Databricks (issue `#1 <https://github.com/astronomer/astro-provider-databricks/issues/1>`_).
* Users should not click the buttons "repair all" or "repair single task" while the DAG/task is running (issue `#2 <https://github.com/astronomer/astro-provider-databricks/issues/2>`_).
