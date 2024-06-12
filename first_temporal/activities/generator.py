from datetime import datetime, timedelta, date
from random import randint
from typing import List, Tuple

from mimesis import Person
from mimesis.enums import Gender
from mimesis.locales import Locale

from shared import Purchase, EMAIL_DOMAINS, RunPlaceholder, BASE_DATE


def create_transactions(
    run_checkpoint: List[RunPlaceholder], 
    names_to_generate: int
) -> Tuple[List[RunPlaceholder], List[Purchase]]:
    """
    Generator function used to generate new vehicle purchases.
    """
    person = Person(Locale.EN)
    current_date = _get_current_date(run_checkpoint)
    purchases = []

    customer_id, transaction_id = _get_id_vals(run_checkpoint)
    for _ in range(names_to_generate):
        selector = randint(0,1)
        email_selector = randint(0, 5)
        product_selector = randint(1,5)

        delivery_date = current_date + timedelta(days=product_selector)
        refund_end_date = current_date + timedelta(days=30)
        new_customer = (
            person.full_name(gender=Gender.MALE).split(' ')
            if selector == 0
            else person.full_name(gender=Gender.FEMALE).split(' ')
        )
        email = (
            f'{new_customer[0]}.'
            f'{new_customer[1]}@{EMAIL_DOMAINS[email_selector]}'
        )
        new_purchase = Purchase(
            customer_id=customer_id,
            first_name=new_customer[0],
            last_name=new_customer[1],
            email_address=email,
            checkout_type='First Time Customer',
            transaction_id=transaction_id,
            product_id=product_selector,
            purchase_date=f'{current_date}',
            delivery_date=f'{delivery_date}',
            refund_till=f'{refund_end_date}',
            delivered=False,
        )

        purchases.append(new_purchase)
        customer_id += 1
        transaction_id += 1

    return (
        _run_holder_update(purchases), purchases
    )


def _get_current_date(run_placeholder: List[RunPlaceholder]) -> date:
    """
    Get current date for purchases.
    """
    day_delta = randint(1, 3)
    if run_placeholder:
        checkpoint = run_placeholder[0]
        previous_date = (
            datetime.strptime(checkpoint['previous_date'], '%Y-%m-%d').date()
        )
        return previous_date + timedelta(days=day_delta)
   
    return BASE_DATE


def _get_id_vals(run_placeholder: List[RunPlaceholder]) -> Tuple[int, int]:
    """
    Get id values for customers and transactions.
    """
    if run_placeholder:
        checkpoint = run_placeholder[0]        
        return (
            checkpoint['last_customer_id'], checkpoint['last_transaction_id']
        ) 
    
    return 100000, 1
    

def _run_holder_update(
    purchases: List[Purchase]
) -> List[RunPlaceholder]:
    """
    Update current placeholder to be able to keep track of what has been
    generated.
    """
    max_customer_id = max([
        purchase.customer_id 
        for purchase in purchases
    ])
    max_transaction_id = max([
        purchase.transaction_id 
        for purchase in purchases
    ])
    purchase_date = purchases[0].purchase_date 
  
    return [RunPlaceholder(
        previous_date=purchase_date,
        last_customer_id=max_customer_id,
        last_transaction_id=max_transaction_id
    )]        
