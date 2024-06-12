import typing
from random import randint
from typing import Any, List, Union, Tuple, Dict

import pandas as pd
from temporalio import activity

from shared import Customer, Purchase, PurchaseDispute, RunPlaceholder
from first_temporal.activities.generator import create_transactions


@activity.defn
async def pull_csv(
    file_type: str
) -> Union[
    List[Purchase], 
    List[Customer],
    List[Purchase], 
    List[PurchaseDispute], 
    List[Any]
]:
    """
    Pull Data from CSV that contains prevous runs data.
    """
    if file_type == 'purchase':
        file_name = 'purchase.csv'
    elif file_type == 'customer':
        file_name = 'customer.csv'
    elif file_type == 'dispute':
        file_name = 'dispute.csv'
    elif file_type == 'placeholder':
        file_name = 'placeholder.csv'

    try:
        df = pd.read_csv(file_name)
    except:
        df = pd.DataFrame()

    if not df.empty:
        if file_type == 'purchase':
            return _past_purchases_to_dataclass(df.to_dict('records'))
        elif file_type == 'customer':
            return _past_customers_to_dataclass(df.to_dict('records'))
        elif file_type == 'dispute':
            return _past_disputes_to_dataclass(df.to_dict('records'))
        else:
            return _placeholder_to_dataclass(df.to_dict('records'))
    
    return []


def _past_purchases_to_dataclass(
        prepped_data: List[typing.Dict[str, Any]]
    ) -> List[Purchase]:
    """
    Formats the list of dictionaries into a list of `Purchase` dataclass 
    objects.
    """
    return [
        Purchase(
            customer_id=item['customer_id'],
            first_name=item['first_name'],
            last_name=item['last_name'],
            email_address=item['email_address'],
            checkout_type=item['checkout_type'],
            transaction_id=item['transaction_id'],
            product_id=item['product_id'],
            purchase_date=item['purchase_date'],
            delivery_date=item['delivery_date'],
            refund_till=item['refund_till'],
            delivered=item['delivered'],
        )
        for item in prepped_data
    ]


def _past_customers_to_dataclass(
        prepped_data: List[typing.Dict[str, Any]]
    ) -> List[Customer]:
    """
    Formats the list of dictionaries into a list of `Customer` dataclass 
    objects.
    """
    return [
        Customer(
            customer_id=item['customer_id'],
            first_name=item['first_name'],
            last_name=item['last_name'],
            email_address=item['email_address'],
        )
        for item in prepped_data
    ]


def _past_disputes_to_dataclass(
        prepped_data: List[typing.Dict[str, Any]]
    ) -> List[PurchaseDispute]:
    """
    Formats the list of dictionaries into a list of `PurchaseDispute` dataclass
    objects.
    """
    return [
        PurchaseDispute(
            customer_id=item['customer_id'],
            transaction_id=item['transaction_id'],
            product_id=item['product_id'],
            dispute_type=item['dispute_type'],
        )
        for item in prepped_data
    ]
     

def _placeholder_to_dataclass(
        prepped_data: typing.Dict[str, Any]
    ) -> List[RunPlaceholder]:
    """
    Formats the list of dictionaries into a list of `RunPlaceholder` dataclass
    objects.
    """
    return [
        RunPlaceholder(    
            previous_date=item['previous_date'],
            last_customer_id=item['last_customer_id'],
            last_transaction_id=item['last_transaction_id'],
        )
        for item in prepped_data
    ]


@activity.defn
async def pull_recent_purchases(
    purchase_arguments: Dict[str, List[Any]]
) -> Tuple[List[RunPlaceholder], List[Purchase]]:
    """
    Dummy function that replicates a pull from a storage layer for purchases.
    """
    run_checkpoint = purchase_arguments['run_checkpoint']
    previous_customers = None  #purchase_arguments['past_customers']
    total_purchases = randint(10,20)
    repeat_customers = (
        int(round((total_purchases / 3), 0)) 
        if previous_customers else 0
    )
    names_to_generate = total_purchases - repeat_customers        

    return create_transactions(
        run_checkpoint, names_to_generate
    )
