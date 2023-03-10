<h1 align="center">
  Astro Databricks
</h1>
  <h3 align="center">
  Affordable Databricks Workflows in Apache Airflow<br><br>
</h3>

[![Python versions](https://img.shields.io/pypi/pyversions/astro-providers-databricks.svg)](https://pypi.org/pypi/astro-providers-databricks)
[![License](https://img.shields.io/pypi/l/astro-providers-databricks.svg)](https://pypi.org/pypi/astro-providers-databricks)
[![Development Status](https://img.shields.io/pypi/status/astro-providers-databricks.svg)](https://pypi.org/pypi/astro-providers-databricks)
[![PyPI downloads](https://img.shields.io/pypi/dm/astro-providers-databricks.svg)](https://pypistats.org/packages/astro-providers-databricks)
[![Contributors](https://img.shields.io/github/contributors/astronomer/astro-providers-databricks)](https://github.com/astronomer/astro-providers-databricks)
[![Commit activity](https://img.shields.io/github/commit-activity/m/astronomer/astro-providers-databricks)](https://github.com/astronomer/astro-providers-databricks)
[![CI](https://github.com/astronomer/astro-providers-databricks/actions/workflows/ci.yml/badge.svg)](https://github.com/astronomer/astro-providers-databricks)
[![codecov](https://codecov.io/gh/astronomer/astro-providers-databricks/branch/main/graph/badge.svg?token=MI4SSE50Q6)](https://codecov.io/gh/astronomer/astro-providers-databricks)


**Astro Databricks** is an [Apache Airflow](https://github.com/apache/airflow) provider created by [Astronomer](https://www.astronomer.io/) for an **optimal Databricks experience**.  With the `DatabricksTaskGroup`, Astro Datatricks allows you to run from Databricks workflows without
the need of running Jobs individually, which can result in [75% cost reduction](https://www.databricks.com/product/aws-pricing).

## Prerequisites

* Apache Airflow >= 2.2.4
* Python >= 2.7
* Databricks account
* Previously created Databricks Notebooks

## Install

```shell
pip install astro-providers-databricks
```

## Quickstart

1. Use pre-existing or create two simple [Databricks Notebooks](https://docs.databricks.com/notebooks/). Their identifiers will be used in step (5). The original example DAG uses: 
   * `Shared/Notebook_1`
   * `Shared/Notebook_2`

2. Generate a [Databricks Personal Token](https://docs.databricks.com/dev-tools/auth.html#databricks-personal-access-tokens). This will be used in step (6). 

3. Ensure that your Airflow environment is set up correctly by running the following commands:

    ```shell
    export AIRFLOW_HOME=`pwd`
   
    airflow db init
    ```
   
4. [Create using your preferred way](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html) a Databricks Airflow connection (so Airflow can access Databricks using your credentials). This can be done by running the following command, replacing the login and password (with your access token):

```shell
airflow connections add 'databricks_conn' \
    --conn-json '{
        "conn_type": "databricks",
        "login": "some.email@yourcompany.com",
        "host": "https://dbc-c9390870-65ef.cloud.databricks.com/",
        "password": "personal-access-token"
    }'
```

5. Copy the following workflow into a file named `example_databricks_workflow.py` and add it to the `dags` directory of your Airflow project:
   
   https://github.com/astronomer/astro-providers-databricks/blob/45897543a5e34d446c84b3fbc4f6f7a3ed16cdf7/example_dags/example_databricks_workflow.py#L48-L101

   Alternatively, you can download `example_databricks_workflow.py`
   ```shell
    curl -O https://raw.githubusercontent.com/astronomer/astro-providers-databricks/main/example_dags/example_databricks_workflow.py
   ```

6. Run the example DAG:

    ```sh
    airflow dags test example_databricks_workflow `date -Iseconds`
    ```
   
This will create a Databricks Workflow with two Notebook jobs.

## Available features

* `DatabricksWorkflowTaskGroup`: Airflow [task group](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#taskgroups) that allows users to create a [Databricks Workflow](https://www.databricks.com/product/workflows).
* `DatabricksNotebookOperator`: Airflow [operator](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/operators.html) which abstracts a pre-existing [Databricks Notebook](https://docs.databricks.com/notebooks/). Can be used independently to run the Notebook, or within a Databricks Workflow Task Group.
* `AstroDatabricksPlugin`: An Airflow [plugin](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/plugins.html) which is installed by the default. It allows users, by using the UI, to view a Databricks job and retry running it in case of failure.

## Documentation

The documentation is a work in progress--we aim to follow the [Diátaxis](https://diataxis.fr/) system:

* [Reference Guide](https://astronomer.github.io/astro-providers-databricks/)

## Changelog

Astro Databricks follows [semantic versioning](https://semver.org/) for releases. Read [changelog](CHANGELOG.rst) to understand more about the changes introduced to each version.

## Contribution guidelines

All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.

Read the [Contribution Guidelines](docs/contributing.rst) for a detailed overview on how to contribute.

Contributors and maintainers should abide by the [Contributor Code of Conduct](CODE_OF_CONDUCT.md).

## License

[Apache Licence 2.0](LICENSE)