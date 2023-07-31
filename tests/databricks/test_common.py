from unittest import mock
from unittest.mock import MagicMock

import pytest
from airflow.exceptions import AirflowException
from astro_databricks.operators.common import DatabricksTaskOperator
from astro_databricks.operators.workflow import (
    DatabricksWorkflowTaskGroup,
)


@pytest.fixture
def mock_runs_api():
    return MagicMock()


@pytest.fixture
def databricks_task_operator():
    return DatabricksTaskOperator(
        task_id="test_task",
        databricks_conn_id="foo",
        job_cluster_key="foo",
        task_config={
            "notebook_task": {
                "notebook_path": "foo",
                "source": "WORKSPACE",
                "base_parameters": {
                    "foo": "bar",
                },
            },
        },
    )


@mock.patch("astro_databricks.operators.common.DatabricksTaskOperator.launch_task_job")
@mock.patch(
    "astro_databricks.operators.common.DatabricksTaskOperator.monitor_databricks_job"
)
def test_databricks_task_operator_without_taskgroup(mock_monitor, mock_launch, dag):
    with dag:
        task = DatabricksTaskOperator(
            task_id="test_task",
            databricks_conn_id="foo",
            job_cluster_key="foo",
            task_config={
                "notebook_task": {
                    "notebook_path": "foo",
                    "source": "WORKSPACE",
                    "base_parameters": {
                        "foo": "bar",
                    },
                },
            },
        )
        assert task.task_id == "test_task"
        assert task.databricks_conn_id == "foo"
        assert task.job_cluster_key == "foo"
        assert task.task_config == {
            "notebook_task": {
                "notebook_path": "foo",
                "source": "WORKSPACE",
                "base_parameters": {
                    "foo": "bar",
                },
            },
        }
    dag.test()
    mock_launch.assert_called_once()
    mock_monitor.assert_called_once()


@mock.patch("astro_databricks.operators.common.DatabricksTaskOperator.launch_task_job")
@mock.patch(
    "astro_databricks.operators.common.DatabricksTaskOperator.monitor_databricks_job"
)
@mock.patch(
    "astro_databricks.operators.workflow._CreateDatabricksWorkflowOperator.execute"
)
def test_databricks_task_operator_with_taskgroup(
    mock_create, mock_monitor, mock_launch, dag
):
    mock_create.return_value = {
        "databricks_job_id": "job_id",
        "databricks_run_id": "run_id",
        "databricks_conn_id": "conn_id",
    }
    with dag:
        task_group = DatabricksWorkflowTaskGroup(
            group_id="test_workflow",
            databricks_conn_id="foo",
            job_clusters=[{"job_cluster_key": "foo"}],
        )
        with task_group:
            task = DatabricksTaskOperator(
                task_id="test_task",
                databricks_conn_id="foo",
                job_cluster_key="foo",
                task_config={
                    "notebook_task": {
                        "notebook_path": "foo",
                        "source": "WORKSPACE",
                        "base_parameters": {
                            "foo": "bar",
                        },
                    },
                },
            )
            assert task.task_id == "test_workflow.test_task"
            assert task.databricks_conn_id == "foo"
            assert task.job_cluster_key == "foo"
            assert task.task_config == {
                "notebook_task": {
                    "notebook_path": "foo",
                    "source": "WORKSPACE",
                    "base_parameters": {
                        "foo": "bar",
                    },
                },
            }
        dag.test()
    mock_launch.assert_not_called()
    mock_monitor.assert_called_once()


@mock.patch(
    "astro_databricks.operators.common.DatabricksTaskOperator.monitor_databricks_job"
)
@mock.patch(
    "astro_databricks.operators.common.DatabricksTaskOperator._get_databricks_task_id"
)
@mock.patch("astro_databricks.operators.common.DatabricksTaskOperator._get_api_client")
@mock.patch("astro_databricks.operators.common.RunsApi")
def test_databricks_task_operator_without_taskgroup_new_cluster(
    mock_runs_api, mock_api_client, mock_get_databricks_task_id, mock_monitor, dag
):
    mock_get_databricks_task_id.return_value = "1234"
    mock_runs_api.return_value = mock.MagicMock()
    with dag:
        DatabricksTaskOperator(
            task_id="test_task",
            databricks_conn_id="foo",
            job_cluster_key="foo",
            new_cluster={"foo": "bar"},
            task_config={
                "notebook_task": {
                    "notebook_path": "foo",
                    "source": "WORKSPACE",
                    "base_parameters": {
                        "foo": "bar",
                    },
                },
            },
        )
    dag.test()
    mock_runs_api.return_value.submit_run.assert_called_once_with(
        {
            "run_name": "1234",
            "new_cluster": {"foo": "bar"},
            "notebook_task": {
                "notebook_path": "foo",
                "source": "WORKSPACE",
                "base_parameters": {
                    "foo": "bar",
                },
            },
        }
    )
    mock_monitor.assert_called_once()


@mock.patch(
    "astro_databricks.operators.common.DatabricksTaskOperator.monitor_databricks_job"
)
@mock.patch(
    "astro_databricks.operators.common.DatabricksTaskOperator._get_databricks_task_id"
)
@mock.patch("astro_databricks.operators.common.DatabricksTaskOperator._get_api_client")
@mock.patch("astro_databricks.operators.common.RunsApi")
def test_databricks_task_operator_without_taskgroup_existing_cluster(
    mock_runs_api, mock_api_client, mock_get_databricks_task_id, mock_monitor, dag
):
    mock_get_databricks_task_id.return_value = "1234"
    mock_runs_api.return_value = mock.MagicMock()
    with dag:
        DatabricksTaskOperator(
            task_id="test_task",
            databricks_conn_id="foo",
            job_cluster_key="foo",
            task_config={
                "notebook_task": {
                    "notebook_path": "foo",
                    "source": "WORKSPACE",
                    "base_parameters": {
                        "foo": "bar",
                    },
                },
            },
            existing_cluster_id="123",
        )
    dag.test()
    mock_runs_api.return_value.submit_run.assert_called_once_with(
        {
            "run_name": "1234",
            "notebook_task": {
                "notebook_path": "foo",
                "source": "WORKSPACE",
                "base_parameters": {
                    "foo": "bar",
                },
            },
            "existing_cluster_id": "123",
        }
    )
    mock_monitor.assert_called_once()


@mock.patch(
    "astro_databricks.operators.common.DatabricksTaskOperator.monitor_databricks_job"
)
@mock.patch("astro_databricks.operators.common.DatabricksTaskOperator._get_api_client")
@mock.patch("astro_databricks.operators.common.RunsApi")
def test_databricks_task_operator_without_taskgroup_existing_cluster_and_new_cluster(
    mock_runs_api, mock_api_client, mock_monitor, dag
):
    with pytest.raises(ValueError):
        with dag:
            DatabricksTaskOperator(
                task_id="test_task",
                databricks_conn_id="foo",
                job_cluster_key="foo",
                task_config={
                    "notebook_task": {
                        "notebook_path": "foo",
                        "source": "WORKSPACE",
                        "base_parameters": {
                            "foo": "bar",
                        },
                    },
                },
                existing_cluster_id="123",
                new_cluster={"foo": "bar"},
            )
        dag.test()


@mock.patch(
    "astro_databricks.operators.common.DatabricksTaskOperator.monitor_databricks_job"
)
@mock.patch("astro_databricks.operators.common.DatabricksTaskOperator._get_api_client")
@mock.patch("astro_databricks.operators.common.RunsApi")
def test_databricks_task_operator_without_taskgroup_no_cluster(
    mock_runs_api, mock_api_client, mock_monitor, dag
):
    with pytest.raises(ValueError):
        with dag:
            DatabricksTaskOperator(
                task_id="test_task",
                databricks_conn_id="foo",
                job_cluster_key="foo",
                task_config={
                    "notebook_task": {
                        "notebook_path": "foo",
                        "source": "WORKSPACE",
                        "base_parameters": {
                            "foo": "bar",
                        },
                    },
                },
            )
        dag.test()


def test_handle_final_state_success(databricks_task_operator):
    final_state = {
        "life_cycle_state": "TERMINATED",
        "result_state": "SUCCESS",
        "state_message": "Job succeeded",
    }
    databricks_task_operator._handle_final_state(final_state)


def test_handle_final_state_failure(databricks_task_operator):
    final_state = {
        "life_cycle_state": "TERMINATED",
        "result_state": "FAILED",
        "state_message": "Job failed",
    }
    with pytest.raises(AirflowException):
        databricks_task_operator._handle_final_state(final_state)


def test_handle_final_state_exception(databricks_task_operator):
    final_state = {
        "life_cycle_state": "SKIPPED",
        "state_message": "Job skipped",
    }
    with pytest.raises(AirflowException):
        databricks_task_operator._handle_final_state(final_state)


@mock.patch("astro_databricks.operators.common.RunsApi")
@mock.patch("time.sleep")
def test_wait_for_pending_task(mock_sleep, mock_runs_api, databricks_task_operator):
    # create a mock current task with "PENDING" state
    current_task = {"run_id": "123", "state": {"life_cycle_state": "PENDING"}}
    mock_runs_api.get_run.side_effect = [
        {"state": {"life_cycle_state": "PENDING"}},
        {"state": {"life_cycle_state": "RUNNING"}},
    ]
    databricks_task_operator._wait_for_pending_task(current_task, mock_runs_api)
    mock_runs_api.get_run.assert_called_with("123", version="2.1")
    assert mock_runs_api.get_run.call_count == 2
    mock_runs_api.reset_mock()


@mock.patch("astro_databricks.operators.common.RunsApi")
@mock.patch("time.sleep")
def test_wait_for_terminating_task(mock_sleep, mock_runs_api, databricks_task_operator):
    current_task = {"run_id": "123", "state": {"life_cycle_state": "PENDING"}}
    mock_runs_api.get_run.side_effect = [
        {"state": {"life_cycle_state": "TERMINATING"}},
        {"state": {"life_cycle_state": "TERMINATING"}},
        {"state": {"life_cycle_state": "TERMINATED"}},
    ]
    databricks_task_operator._wait_for_terminating_task(current_task, mock_runs_api)
    mock_runs_api.get_run.assert_called_with("123", version="2.1")
    assert mock_runs_api.get_run.call_count == 3
    mock_runs_api.reset_mock()


@mock.patch("astro_databricks.operators.common.RunsApi")
@mock.patch("time.sleep")
def test_wait_for_running_task(mock_sleep, mock_runs_api, databricks_task_operator):
    current_task = {"run_id": "123", "state": {"life_cycle_state": "PENDING"}}
    mock_runs_api.get_run.side_effect = [
        {"state": {"life_cycle_state": "RUNNING"}},
        {"state": {"life_cycle_state": "RUNNING"}},
        {"state": {"life_cycle_state": "TERMINATED"}},
    ]
    databricks_task_operator._wait_for_running_task(current_task, mock_runs_api)
    mock_runs_api.get_run.assert_called_with("123", version="2.1")
    assert mock_runs_api.get_run.call_count == 3
    mock_runs_api.reset_mock()


def test_get_lifestyle_state(databricks_task_operator):
    runs_api_mock = MagicMock()
    runs_api_mock.get_run.return_value = {"state": {"life_cycle_state": "TERMINATING"}}

    task_info = {"run_id": "test_run_id"}

    assert (
        databricks_task_operator._get_lifestyle_state(task_info, runs_api_mock)
        == "TERMINATING"
    )


@mock.patch("astro_databricks.operators.common.DatabricksHook")
@mock.patch("astro_databricks.operators.common.RunsApi")
@mock.patch("astro_databricks.operators.common.DatabricksTaskOperator._get_api_client")
@mock.patch(
    "astro_databricks.operators.common.DatabricksTaskOperator._get_databricks_task_id"
)
def test_monitor_databricks_job_success(
    mock_get_databricks_task_id,
    mock_get_api_client,
    mock_runs_api,
    mock_databricks_hook,
    databricks_task_operator,
    caplog,
):
    mock_get_databricks_task_id.return_value = "1"
    # Define the expected response
    response = {
        "run_page_url": "https://databricks-instance-xyz.cloud.databricks.com/#job/1234/run/1",
        "state": {
            "life_cycle_state": "TERMINATED",
            "result_state": "SUCCESS",
            "state_message": "Ran successfully",
        },
        "tasks": [
            {
                "run_id": "1",
                "task_key": "1",
            }
        ],
    }
    mock_runs_api.return_value.get_run.return_value = response

    databricks_task_operator.databricks_run_id = "1"
    databricks_task_operator.monitor_databricks_job()
    mock_runs_api.return_value.get_run.assert_called_with(
        databricks_task_operator.databricks_run_id, version="2.1"
    )
    assert (
        "Check the job run in Databricks: https://databricks-instance-xyz.cloud.databricks.com/#job/1234/run/1"
        in caplog.messages
    )


@mock.patch("astro_databricks.operators.common.DatabricksHook")
@mock.patch("astro_databricks.operators.common.RunsApi")
@mock.patch("astro_databricks.operators.common.DatabricksTaskOperator._get_api_client")
@mock.patch(
    "astro_databricks.operators.common.DatabricksTaskOperator._get_databricks_task_id"
)
def test_monitor_databricks_job_fail(
    mock_get_databricks_task_id,
    mock_get_api_client,
    mock_runs_api,
    mock_databricks_hook,
    databricks_task_operator,
):
    mock_get_databricks_task_id.return_value = "1"
    # Define the expected response
    response = {
        "run_page_url": "https://databricks-instance-xyz.cloud.databricks.com/#job/1234/run/1",
        "state": {
            "life_cycle_state": "TERMINATED",
            "result_state": "FAILED",
            "state_message": "job failed",
        },
        "tasks": [
            {
                "run_id": "1",
                "task_key": "1",
            }
        ],
    }
    mock_runs_api.return_value.get_run.return_value = response

    databricks_task_operator.databricks_run_id = "1"
    with pytest.raises(AirflowException):
        databricks_task_operator.monitor_databricks_job()
