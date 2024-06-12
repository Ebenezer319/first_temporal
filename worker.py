import asyncio
import logging

from temporalio.client import Client
from temporalio.worker import Worker

from first_temporal.activities import extractor, transformer
from first_temporal.workflow import VehicleTransactionsWorkflow
from shared import TASK_QUEUE_NAME


async def main():
    """
    Worker function where logging and the client is set up to work the queue.
    """
    logging.basicConfig(level=logging.INFO)
    client = await Client.connect("localhost:7233")
    worker = Worker(
        client,
        task_queue=TASK_QUEUE_NAME,
        workflows=[VehicleTransactionsWorkflow],
        activities=[
            extractor.pull_csv, 
            extractor.pull_recent_purchases,
            transformer.define_customers_from_purchases
        ],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())