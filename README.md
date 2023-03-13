<h1 align="center">
  Astro Databricks
</h1>
  <h3 align="center">
  Orchestrate your Databricks notebooks in Airflow and execute them as Databricks Workflows<br><br>
</h3>

[![Python versions](https://img.shields.io/pypi/pyversions/astro-provider-databricks.svg)](https://pypi.org/pypi/astro-provider-databricks)
[![License](https://img.shields.io/pypi/l/astro-provider-databricks.svg)](https://pypi.org/pypi/astro-provider-databricks)
[![Development Status](https://img.shields.io/pypi/status/astro-provider-databricks.svg)](https://pypi.org/pypi/astro-provider-databricks)
[![PyPI downloads](https://img.shields.io/pypi/dm/astro-provider-databricks.svg)](https://pypistats.org/packages/astro-provider-databricks)
[![Contributors](https://img.shields.io/github/contributors/astronomer/astro-provider-databricks)](https://github.com/astronomer/astro-provider-databricks)
[![Commit activity](https://img.shields.io/github/commit-activity/m/astronomer/astro-provider-databricks)](https://github.com/astronomer/astro-provider-databricks)
[![CI](https://github.com/astronomer/astro-provider-databricks/actions/workflows/ci.yml/badge.svg)](https://github.com/astronomer/astro-provider-databricks)
[![codecov](https://codecov.io/gh/astronomer/astro-provider-databricks/branch/main/graph/badge.svg?token=MI4SSE50Q6)](https://codecov.io/gh/astronomer/astro-provider-databricks)

The **Astro Databricks Provider** is an [Apache Airflow](https://github.com/apache/airflow) provider created by [Astronomer](https://www.astronomer.io/) to run your Databricks notebooks as Databricks Workflows while maintaining Airflow as the authoring interface. When using the `DatabricksTaskGroup` and `DatabricksNotebookOperator`, notebooks run as a Databricks Workflow which can result in a [75% cost reduction](https://www.databricks.com/product/aws-pricing) ($0.40/DBU for all-purpose compute, $0.10/DBU for Jobs compute).

## Prerequisites

- Apache Airflow >= 2.2.4
- Python >= 3.7
- Databricks account
- Previously created Databricks Notebooks

## Install

```shell
pip install astro-provider-databricks
```

## Quickstart (with Astro CLI)

1. Use pre-existing or create two simple [Databricks Notebooks](https://docs.databricks.com/notebooks/). Their identifiers will be used in step (6). The original example DAG uses:

   - `Shared/Notebook_1`
   - `Shared/Notebook_2`

2. Generate a [Databricks Personal Token](https://docs.databricks.com/dev-tools/auth.html#databricks-personal-access-tokens). This will be used in step (5).

3. Create a new Astro CLI project (if you don't have one already):

   ```shell
   mdkir my_project && cd my_project
   astro dev init
   ```

4. Add the following to your `requirements.txt` file:

   ```shell
   astro-provider-databricks
   ```

5. [Create a Databricks connection in Airflow](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html). You can do this via the Airflow UI or the `airflow_settings.yaml` file by specifying the following fields:

   ```yaml
   connections:
     - conn_id: databricks_conn
       conn_type: databricks
       conn_login: <your email, e.g. julian@astronomer.io>
       conn_password: <your personal access token, e.g. dapi1234567890abcdef>
       conn_host: <your databricks host, e.g. https://dbc-9c390870-65ef.cloud.databricks.com>
   ```

6. Copy the following workflow into a file named `example_databricks.py` in your `dags` directory:

   https://github.com/astronomer/astro-provider-databricks/blob/45897543a5e34d446c84b3fbc4f6f7a3ed16cdf7/example_dags/example_databricks_workflow.py#L48-L101

7. Run the following command to start your Airflow environment:

   ```shell
   astro dev start
   ```

8. Open the Airflow UI at http://localhost:8080 and trigger the DAG. You can click on a task, and under the Details tab select "See Databricks Job Run" to open the job in the Databricks UI.

## Quickstart (without Astro CLI)

1. Use pre-existing or create two simple [Databricks Notebooks](https://docs.databricks.com/notebooks/). Their identifiers will be used in step (5). The original example DAG uses:

   - `Shared/Notebook_1`
   - `Shared/Notebook_2`

2. Generate a [Databricks Personal Token](https://docs.databricks.com/dev-tools/auth.html#databricks-personal-access-tokens). This will be used in step (6).

3. Ensure that your Airflow environment is set up correctly by running the following commands:

   ```shell
   export AIRFLOW_HOME=`pwd`

   airflow db init
   ```

4. [Create a Databricks connection in Airflow](https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html). This can be done by running the following command, replacing the login and password (with your access token):

   ```shell
   # If using Airflow 2.3 or higher:
   airflow connections add 'databricks_conn' \
       --conn-json '{
           "conn_type": "databricks",
           "login": "some.email@yourcompany.com",
           "host": "https://dbc-c9390870-65ef.cloud.databricks.com/",
           "password": "personal-access-token"
       }'

   # If using Airflow between 2.2.4 and less than 2.3:
   airflow connections add 'databricks_conn' --conn-type 'databricks' --conn-login 'some.email@yourcompany.com' --conn-host 'https://dbc-9c390870-65ef.cloud.databricks.com/' --conn-password 'personal-access-token'
   ```

5. Copy the following workflow into a file named `example_databricks_workflow.py` and add it to the `dags` directory of your Airflow project:

   https://github.com/astronomer/astro-provider-databricks/blob/45897543a5e34d446c84b3fbc4f6f7a3ed16cdf7/example_dags/example_databricks_workflow.py#L48-L101

   Alternatively, you can download `example_databricks_workflow.py`

   ```shell
   curl -O https://raw.githubusercontent.com/astronomer/astro-provider-databricks/main/example_dags/example_databricks_workflow.py
   ```

6. Run the example DAG:

   ```shell
   airflow dags test example_databricks_workflow `date -Iseconds`
   ```

   Which will log, among other lines, the link to the Databricks Job Run URL:

   ```shell
   [2023-03-13 15:27:09,934] {notebook.py:158} INFO - Check the job run in Databricks: https://dbc-c9390870-65ef.cloud.databricks.com/?o=4256138892007661#job/950578808520081/run/14940832
   ```

   This will create a Databricks Workflow with two Notebook jobs. This workflow may take two minutes to complete if the cluster is already up & running or approximately five minutes depending on your cluster initialisation time.

## Available features

- `DatabricksWorkflowTaskGroup`: Airflow [task group](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#taskgroups) that allows users to create a [Databricks Workflow](https://www.databricks.com/product/workflows).
- `DatabricksNotebookOperator`: Airflow [operator](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/operators.html) which abstracts a pre-existing [Databricks Notebook](https://docs.databricks.com/notebooks/). Can be used independently to run the Notebook, or within a Databricks Workflow Task Group.
- `AstroDatabricksPlugin`: An Airflow [plugin](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/plugins.html) which is installed by the default. It allows users, by using the UI, to view a Databricks job and retry running it in case of failure.

## Documentation

The documentation is a work in progress--we aim to follow the [Diátaxis](https://diataxis.fr/) system:

- [Reference Guide](https://astronomer.github.io/astro-provider-databricks/)

## Changelog

Astro Databricks follows [semantic versioning](https://semver.org/) for releases. Read [changelog](CHANGELOG.rst) to understand more about the changes introduced to each version.

## Contribution guidelines

All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.

Read the [Contribution Guidelines](docs/contributing.rst) for a detailed overview on how to contribute.

Contributors and maintainers should abide by the [Contributor Code of Conduct](CODE_OF_CONDUCT.md).

## License

[Apache Licence 2.0](LICENSE)
