from dataclasses import dataclass

from shopfront.repositories.customers import CustomerRepository
from shopfront.repositories.orders import OrderRepository
from shopfront.services.customers import CustomerService
from shopfront.services.orders import OrderService


@dataclass
class Container:
    customers: CustomerService
    orders: OrderService


def build():
    customers, orders = CustomerRepository(), OrderRepository()
    return Container(CustomerService(customers), OrderService(orders, customers))
