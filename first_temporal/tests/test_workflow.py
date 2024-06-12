import pytest
from unittest.mock import patch, MagicMock

from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

from shared import TASK_QUEUE_NAME
from first_temporal.workflow import VehicleTransactionsWorkflow
from first_temporal.activities import extractor, transformer


@pytest.mark.asyncio
async def test_vehicle_transactions_none():
    async with await WorkflowEnvironment.start_time_skipping() as env:
        async with Worker (
            env.client,
            task_queue="test-transactions",
            workflows=[VehicleTransactionsWorkflow],
            activities=[
                extractor.pull_csv, 
                extractor.pull_recent_purchases,
                transformer.define_customers_from_purchases
            ],
        ):
            await env.client.execute_workflow(
                VehicleTransactionsWorkflow.run,
                id="test-vehicle-transactions",
                task_queue="test-transactions"
            )
