<h1 align="center">
  Databricks Workflows in Airflow
</h1>

The Astro Databricks Provider is an Apache Airflow provider to run your Databricks notebooks as Databricks Workflows while maintaining Airflow as the authoring interface. Running your Databricks notebooks as Databricks Workflows can result in a [75% cost reduction](https://www.databricks.com/product/aws-pricing) ($0.40/DBU for all-purpose compute, $0.10/DBU for Jobs compute).

There are a few advantages to defining your Databricks Workflows in Airflow:

|                                      |        via Databricks         |      via Airflow       |
| :----------------------------------- | :---------------------------: | :--------------------: |
| Authoring interface                  | _Web-based via Databricks UI_ | _Code via Airflow DAG_ |
| Workflow compute pricing             |              ✅               |           ✅           |
| Notebook code in source control      |              ✅               |           ✅           |
| Workflow structure in source control |                               |           ✅           |
| Retry from beginning                 |              ✅               |           ✅           |
| Retry single task                    |                               |           ✅           |
| Task groups within Workflows         |                               |           ✅           |
| Trigger workflows from other DAGs    |                               |           ✅           |
| Workflow-level parameters            |                               |           ✅           |

## Example

The following Airflow DAG illustrates how to use the `DatabricksTaskGroup` and `DatabricksNotebookOperator` to define a Databricks Workflow in Airflow:

```python
from pendulum import datetime

from airflow.decorators import dag, task_group
from astro_databricks import DatabricksNotebookOperator, DatabricksWorkflowTaskGroup

# define your cluster spec - can have from 1 to many clusters
job_cluster_spec = [
   {
      "job_cluster_key": "astro_databricks",
      "new_cluster": {
         "cluster_name": "",
         "spark_version": "11.3.x-scala2.12",
         "aws_attributes": {
               "first_on_demand": 1,
               "availability": "SPOT_WITH_FALLBACK",
               "zone_id": "us-east-2b",
               "spot_bid_price_percent": 100,
               "ebs_volume_count": 0,
         },
         "node_type_id": "i3.xlarge",
         "spark_env_vars": {"PYSPARK_PYTHON": "/databricks/python3/bin/python3"},
         "enable_elastic_disk": False,
         "data_security_mode": "LEGACY_SINGLE_USER_STANDARD",
         "runtime_engine": "STANDARD",
         "num_workers": 8,
      },
   }
]

@dag(start_date=datetime(2023, 1, 1), schedule_interval="@daily", catchup=False)
def databricks_workflow_example():
   # the task group is a context manager that will create a Databricks Workflow
   with DatabricksWorkflowTaskGroup(
      group_id="example_databricks_workflow",
      databricks_conn_id="databricks_default",
      job_clusters=job_cluster_spec,
      # you can specify common fields here that get shared to all notebooks
      notebook_packages=[
         { "pypi": { "package": "pandas" } },
         { "pypi": { "package": "numpy" } },
      ],
      # notebook_params supports templating
      notebook_params={
         "start_time": "{{ ds }}",
      }
   ):
      notebook_1 = DatabricksNotebookOperator(
         task_id="notebook_1",
         notebook_path="/Shared/notebook_1",
         source="WORKSPACE",
         # job_cluster_key corresponds to the job_cluster_key in the job_cluster_spec
         job_cluster_key="astro_databricks",
         # you can add to packages & params at the task level
         notebook_packages=[
            { "pypi": { "package": "scikit-learn" } },
         ],
         notebook_params={
            "end_time": "{{ macros.ds_add(ds, 1) }}",
         }
      )

      # you can embed task groups for easier dependency management
      @task_group(group_id="inner_task_group")
      def inner_task_group():
         notebook_2 = DatabricksNotebookOperator(
            task_id="notebook_2",
            notebook_path="/Shared/notebook_2",
            source="WORKSPACE",
            job_cluster_key="astro_databricks",
         )

         notebook_3 = DatabricksNotebookOperator(
            task_id="notebook_3",
            notebook_path="/Shared/notebook_3",
            source="WORKSPACE",
            job_cluster_key="astro_databricks",
         )

      notebook_4 = DatabricksNotebookOperator(
         task_id="notebook_4",
         notebook_path="/Shared/notebook_4",
         source="WORKSPACE",
         job_cluster_key="astro_databricks",
      )

      notebook_1 >> inner_task_group() >> notebook_4

databricks_workflow_example_dag = databricks_workflow_example()
```

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
