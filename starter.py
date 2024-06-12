import asyncio

import pandas as pd
from temporalio.client import Client

from shared import TASK_QUEUE_NAME
from first_temporal.workflow import VehicleTransactionsWorkflow


async def main():
    """
    Starter that is used to trigger the run of the workflow. Writing data to
    local storage, in this case it's a csv file.
    """
    client = await Client.connect("localhost:7233")
    checkpoint_holder, all_purchases, all_customers = (
        await client.execute_workflow(
            VehicleTransactionsWorkflow.run,
            id="Vehicle-transaction-workflow",
            task_queue=TASK_QUEUE_NAME,
        )
    )
    checkpoint_df = pd.DataFrame(checkpoint_holder)
    customers_df = pd.DataFrame(all_customers)
    purchases_df = pd.DataFrame(all_purchases)

    checkpoint_df.to_csv('placeholder.csv', index=False)
    customers_df.to_csv('customer.csv', index=False)
    purchases_df.to_csv('purchase.csv', index=False)


if __name__ == "__main__":
    asyncio.run(main())