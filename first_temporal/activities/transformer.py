from typing import List

from temporalio import activity

from shared import Customer, Purchase


@activity.defn
async def define_customers_from_purchases(
    current_purchases: List[Purchase]
) -> List[Customer]:
    """
    From new purchases made, generate the necessary list of 
    `Customer`.

    :param current_purchases:
        List of the `Purchase` dataclass used to pull customer data.
    "return:
        List of the `Customer` dataclass that is created from 4 fields within
        the `Purchase` dataclass object.
    """
    return [
        Customer(
            customer_id=vehicle_purchase.customer_id,
            first_name=vehicle_purchase.first_name,
            last_name=vehicle_purchase.last_name,
            email_address=vehicle_purchase.email_address,
        )
        for vehicle_purchase in current_purchases
    ]
