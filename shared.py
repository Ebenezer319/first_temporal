from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum


TASK_QUEUE_NAME = 'temporal-project'
EMAIL_DOMAINS = [
    'gmail.com', 
    'yahoo.com', 
    'hotmail.com', 
    'outlook.com',
    'verizon.net', 
    'aol.com'
]
BASE_DATE = datetime(2020, 7, 3).date()

class CheckoutTypes(Enum):
    """
    Represents checkout types.
    """
    INITIAL = 'First Time Customer'
    REPEAT = 'Repeat Customer'


class DisputeTypes(Enum):
    """
    Represents dispute types.
    """
    CANCELLATION = 'cancellation'
    REFUND = 'return_for_refund'
    RETURN = 'return_for_no_refund'


@dataclass
class Purchase:
    """
    Represents a Purchase and the pertinent information associated with making
    one.
    """
    customer_id: int
    first_name: str
    last_name: str
    email_address: str
    checkout_type: str
    transaction_id: int
    product_id: int
    purchase_date: str
    delivery_date: str
    refund_till: str
    delivered: bool


@dataclass
class Customer:
    """
    Represents customers that have made a purchase prior.
    """
    customer_id: int
    first_name: str
    last_name: str
    email_address: str


@dataclass
class PurchaseDispute:
    """
    Represents a dispute that took place prior.
    """
    customer_id: int
    transaction_id: int
    product_id: int
    dispute_type: DisputeTypes


@dataclass
class RunPlaceholder:
    """
    Represents a dispute that took place prior.
    """
    previous_date: str
    last_customer_id: int  
    last_transaction_id: int     


@dataclass
class Product:
    """
    Represents a product that is being sold by the dealer.
    """
    product_id: int
    year: int
    make: str
    model: str
    exterior_color: str
    interior_color: str
    cost: float


class Products(Enum):
    """
    Enum containing mutiple Products.
    """
    RAM_TRX_2024 = Product(
        product_id=1,
        year=2024,
        make='Ram',
        model='1500 TRX',
        exterior_color='Black',
        interior_color='Black',
        cost=125_215.00
    )

    ALFA_ROMEO_2024 = Product(
        product_id=2,
        year=2024,
        make='Alfa Romeo',
        model='Stelvio Quadrifoglio',
        exterior_color='Black',
        interior_color='Black',
        cost=92_237.00
    )

    PORSCHE_GTS_2024 = Product(
        product_id=3,
        year=2024,
        make='Porsche',
        model='Cayenne Turbo GT',
        exterior_color='Black',
        interior_color='Red & Black',
        cost=215_617.00
    )

    ASTON_DBX_2024 = Product(
        product_id=4,
        year=2024,
        make='Aston Martin',
        model='DBX 707',
        exterior_color='Black',
        interior_color='Red',
        cost=265_617.00
    )

    AUDI_Q8_2024 = Product(
        product_id=5,
        year=2024,
        make='Audi',
        model='RS Q8',
        exterior_color='Black',
        interior_color='Red & Black',
        cost=132_327.00
    )


_product_make_lookup = {product.value.make: product.value for product in Products}


def get_product_by_make(product_make: str) -> Product:
    """Get Product object based on the make supplied."""
    return _product_make_lookup[product_make]