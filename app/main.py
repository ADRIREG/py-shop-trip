import json
import datetime
from app.car import Car
from app.customer import Customer
from app.shop import Shop
from app.utils import calculate_distance


def shop_trip() -> None:
    with open("config.json", "r") as file:
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
        print(f"{customer.name} has {customer.money} dollars")

        trip_costs = {}
        for shop in shops:
            cost = customer.calculate_trip_cost(shop, fuel_price)
            trip_costs[shop] = cost
            print(
                f"{customer.name} "
                f"shop_data trip to the {shop.name} costs {cost}")

        best_shop = min(trip_costs, key=trip_costs.get)

        if trip_costs[best_shop] <= customer.money:
            print(f"{customer.name} rides to {best_shop.name}")

            customer.location = best_shop.location

            now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"# Date: {now}")
            print(f"Thanks, {customer.name}, for your purchase!")
            print("You have bought:")

            shopping_cost = best_shop.calculate_cost(customer.product_cart)
            for item, quantity in customer.product_cart.items():
                price = best_shop.products[item]
                print(f"{quantity} {item}shop_data "
                      f"for {quantity * price} dollars")

            print(f"Total cost is {shopping_cost} dollars")
            print("See you again!")

            customer.money -= trip_costs[best_shop]
            print(f"{customer.name} rides home")
            print(f"{customer.name} "
                  f"now has {round(customer.money, 2)} dollars")
        else:
            print(
                f"{customer.name} "
                f"doesn't have enough money to make a purchase in any shop")


if __name__ == "__main__":
    shop_trip()
