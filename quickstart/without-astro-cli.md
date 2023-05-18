## Prerequisites

- Apache Airflow >= 2.2.4
- Python >= 3.7
- Databricks account
- Previously created Databricks Notebooks

## Install

```shell
pip install astro-provider-databricks
```

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
