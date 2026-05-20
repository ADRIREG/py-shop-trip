import os
import json
import datetime
from app.car import Car
from app.customer import Customer
from app.shop import Shop


def shop_trip() -> None:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, "..", "config.json")

    with open(config_path, "r") as file:
        data = json.load(file)

    fuel_price = data["FUEL_PRICE"]

    shops = []
    for shop_data in data["shops"]:
        shops.append(Shop(shop_data["name"],
                          shop_data["location"],
                          shop_data["products"]))

    customers = []
    for customer_data in data["customers"]:
        car = Car(customer_data["car"]["brand"],
                  customer_data["car"]["fuel_consumption"])
        cust = Customer(customer_data["name"],
                        customer_data["product_cart"],
                        customer_data["location"],
                        customer_data["money"],
                        car)
        customers.append(cust)

    for customer in customers:
        trip_costs = {}
        for shop in shops:
            cost = customer.calculate_trip_cost(shop, fuel_price)
            trip_costs[shop] = cost

        best_shop = min(trip_costs, key=trip_costs.get)
        total_cost = trip_costs[best_shop]

        if total_cost <= customer.money:
            customer.location = best_shop.location
            customer.money -= total_cost

            now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"# Date: {now}")
            print(f"Thanks, {customer.name}, for your purchase!")
            print("You have bought:")

            for item, quantity in customer.product_cart.items():
                price = best_shop.products[item]
                print(f"{quantity} {item}s for {quantity * price} dollars")

            print(f"Total cost is {total_cost} dollars")
            print(f"{customer.name} rides home")
            print(f"{customer.name} "
                  f"now has {round(customer.money, 2)} dollars")
        else:
            print(f"{customer.name} doesn't have enough money "
                  f"to make a purchase in any shop")


if __name__ == "__main__":
    shop_trip()
