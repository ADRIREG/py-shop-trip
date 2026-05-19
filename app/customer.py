from car import Car
from shop import Shop


class Customer:
    def __init__(self,
                 name: str,
                 product_cart: dict,
                 location: tuple,
                 money: int,
                 car: Car) \
            -> None:
        self.name = name
        self.product_cart = product_cart
        self.location = location
        self.money = money
        self.car = car

    def calculate_trip_cost(self, shop: Shop, fuel_price: float) -> int:
        pass
