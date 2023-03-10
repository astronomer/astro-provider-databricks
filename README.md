<h1 align="center">
  Astro Databricks
</h1>
  <h3 align="center">
  Databricks Workflows in Apache Airflow made cheaper<br><br>
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
the need of running Jobs individually, which can result in **75% cost reduction**.

## Prerequisites

* Apache Airflow >= 2.2
* Python >= 2.7
* Databricks account
* Previously created Databricks Notebooks

## Install

```shell
pip install astro-providers-databricks
```

## Quickstart

1. Either use pre-existing or create two simple [Databricks Notebook](https://docs.databricks.com/notebooks/).

TODO: add screenshot

2. Ensure that your Airflow environment is set up correctly by running the following commands:

    ```shell
    export AIRFLOW_HOME=`pwd`
    export AIRFLOW__CORE__ALLOWED_DESERIALIZATION_CLASSES": "airflow\\.* astro_databricks\\.*"
   
    airflow db init
    ```
   
3. Create a Databricks connection

TODO

4. Run your workflow locally by using Airflow

TODO
   

## Available features

* `DatabricksWorkflowTaskGroup`: Airflow [task group](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#taskgroups) that allows users to create a [Databricks Workflow](https://www.databricks.com/product/workflows).
* `DatabricksNotebookOperator`: Airflow [operator](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/operators.html) which abstracts a pre-existing [Databricks Notebook](https://docs.databricks.com/notebooks/). Can be used independently to run the Notebook, or within a Databricks Workfow Task Group.
* `AstroDatabricksPlugin`: An Airflow [plugin](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/plugins.html) which is installed by the default. It allows users, by using the UI, to view a Databricks job and retry running it in case of failure.

## Documentation

The documentation is a work in progress--we aim to follow the [Diátaxis](https://diataxis.fr/) system:

* [Reference Guide](https://astronomer.github.io/astro-providers-databricks/)

## Changelog

Astro Databricks follows [semantic versioning](https://semver.org/) for releases. Read [changelog](CHANGELOG.rst) to understand more about the changes introduced to each version.

## Contribution guidelines

All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.

Read the [Contribution Guideline](docs/contributing.rst) for a detailed overview on how to contribute.

Contributors and maintainers should abide by the [Contributor Code of Conduct](CODE_OF_CONDUCT.md).

## License

[Apache Licence 2.0](LICENSE)