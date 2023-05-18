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
