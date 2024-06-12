from datetime import timedelta
from typing import List, Union, Tuple

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    import pandas as pd

    from first_temporal.activities import extractor, transformer
    from shared import (
        Customer,
        Purchase,
        PurchaseDispute,
        RunPlaceholder
    )


@workflow.defn
class VehicleTransactionsWorkflow:

    @workflow.run
    async def run(self) -> Tuple[
        List[RunPlaceholder], List[Purchase], List[Customer]
    ]:
        """
        Workflow that simulates the batch process of consolidating a
        performance vehicle dealerships purchase data.
        """
        run_checkpoint, past_purchases, past_customers, past_disputes = (
            await self._pull_past_historic_data()
        )
        pull_args = {
            'run_checkpoint': run_checkpoint,
            'past_customers': past_customers
        }
        updated_checkpoint, new_purchases = await workflow.execute_activity(
            extractor.pull_recent_purchases,
            pull_args,
            start_to_close_timeout=timedelta(seconds=15)
        )

        workflow.logger.info(
            f"Today had {len(new_purchases)} new Purchases."
        )

        new_customers = await workflow.execute_activity(
            transformer.define_customers_from_purchases,
            new_purchases,
            start_to_close_timeout=timedelta(seconds=15)
        )
        
        full_purchases = past_purchases + new_purchases
        full_customers = past_customers + new_customers

        return updated_checkpoint, full_purchases, full_customers


    async def _pull_past_historic_data(self) -> Union[
            List[RunPlaceholder], 
            List[Purchase],
            List[Customer],
            List[PurchaseDispute]
        ]:
        """
        Helper workflow function that pulls historic data.
        """
        checkpoint_holder = await workflow.execute_activity(
            extractor.pull_csv,
            'placeholder',
            start_to_close_timeout=timedelta(seconds=10)
        )
        past_purchases = await workflow.execute_activity(
            extractor.pull_csv,
            'purchase',
            start_to_close_timeout=timedelta(seconds=10)
        )
        workflow.logger.info(
            f"Pulled {len(past_purchases)} Past Purchases."
        )

        past_customers = await workflow.execute_activity(
            extractor.pull_csv,
            'customer',
            start_to_close_timeout=timedelta(seconds=10)
        )
        workflow.logger.info(
            f"Pulled {len(past_customers)} Past Customers."
        )

        past_disputes = await workflow.execute_activity(
            extractor.pull_csv,
            'dispute',
            start_to_close_timeout=timedelta(seconds=10)
        )
        workflow.logger.info(
            f"Pulled {len(past_disputes)} Past Disputes."
        )
        

        return checkpoint_holder, past_purchases, past_customers, past_disputes
        