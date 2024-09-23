import re
from datetime import datetime, timedelta

from sqlalchemy import text

from app.database.account_management import get_customer_id
from app.database.database import get_engine

engine = get_engine()


def get_pizza_id(pizza_type, size):
    query = text('''
        SELECT PizzaID FROM Pizza
        WHERE Type = :pizza_type AND Size = :size
    ''')
    with engine.connect() as connection:
        result = connection.execute(query, {'pizza_type': pizza_type, 'size': size})
        pizza = result.fetchone()
        return pizza.PizzaID if pizza else None

def get_drink_id(drink_name, size):
    query = text('''
        SELECT DrinkID FROM Drink
        WHERE Name = :drink_name AND Size = :size
    ''')
    with engine.connect() as connection:
        result = connection.execute(query, {'drink_name': drink_name, 'size': size})
        drink = result.fetchone()
        return drink.DrinkID if drink else None

def get_dessert_id(dessert_type):
    query = text('''
        SELECT DessertID FROM Dessert
        WHERE Type = :dessert_type
    ''')
    with engine.connect() as connection:
        result = connection.execute(query, {'dessert_type': dessert_type})
        dessert = result.fetchone()
        return dessert.DessertID if dessert else None






def get_account_information():
    customer_id = get_customer_id()
    query = text('''
        SELECT Name, Gender, Birthdate, PhoneNumber, Address, Email, NumberOfOrders
        FROM Customer
        WHERE CustomerID = :customer_id
    ''')

    with engine.connect() as connection:
        result = connection.execute(query, {'customer_id': customer_id})
        account_info = result.fetchone()

    if account_info:
        return {
            'Name': account_info.Name,
            'Gender': account_info.Gender,
            'Birthdate': account_info.Birthdate,
            'PhoneNumber': account_info.PhoneNumber,
            'Address': account_info.Address,
            'Email': account_info.Email,
            'NumberOfOrders': account_info.NumberOfOrders,
        }

    return None

def get_pizza_info():
    query = text('''
                SELECT * FROM Pizza
            ''')
    with engine.connect() as connection:
        result = connection.execute(query)
        return result.fetchall()

def get_pizza_types():
    pizzas= get_pizza_info()
    pizza_types = {pizza[1] for pizza in pizzas}
    return list(pizza_types)

def get_pizza_ingredients():
    ingredients = get_pizza_info()
    ingredient_types = {pizza[6] for pizza in ingredients}
    return ingredient_types

def get_drinks_info():
    query = text('''
                SELECT * FROM Drink
            ''')
    with engine.connect() as connection:
        result = connection.execute(query)
        return result.fetchall()
def get_drink_types():
    drinks = get_drinks_info()
    drink_types = {drinks[1] for drinks in drinks}
    return list(drink_types)

def get_desserts_info():
    query = text('''
                SELECT * FROM Dessert
            ''')
    with engine.connect() as connection:
        result = connection.execute(query)
        return result.fetchall()

def get_desserts_types():
    desserts = get_desserts_info()
    dessert_types = {desserts[1] for desserts in desserts}
    return list(dessert_types)


def get_ingredients_info():
    query = text('''SELECT * FROM Ingredient''')
    with engine.connect() as connection:
        result = connection.execute(query)
        return result.fetchall()

def get_ingredients_types():
    ingredients = get_ingredients_info()
    ingredient_types = {ingredients[3] for ingredients in ingredients}
    return list(ingredient_types)

def get_ingredient_details(food_type, category):
    if category == "Pizza":
        # For pizzas, we need to join the Pizza and Ingredient tables
        pizza_query = text('''
            SELECT * FROM Pizza
            WHERE Type = :food_type
        ''')
        with engine.connect() as connection:
            with connection.begin() as transaction:
                result = connection.execute(pizza_query, {'food_type': food_type})
                pizza_ingredients = result.fetchone()

                if pizza_ingredients:
                    return pizza_ingredients[6]
                else:
                    return "No information available."


def get_ingredient_from_ids(ids):
    # If ids are passed as a string like "[1,2,3,34]", clean it up
    if isinstance(ids, str):
        # Use regex to extract all numbers from the string
        ids = re.findall(r'\d+', ids)
        ids = [int(i) for i in ids]  # Convert extracted numbers to integers

    ingredients = []
    for id1 in ids:
        query = text('''
                        SELECT * FROM Ingredient
                        WHERE IngredientID = :id
                        ''')
        with engine.connect() as connection:
            result = connection.execute(query, {'id': id1})
            ingredient = result.fetchone()
            if ingredient:
                ingredients.append(ingredient[3])  # Assuming the name is at index 3
    return ingredients

def check_price(category, item_name, item_size):
    if category == "Pizza":
        query = text('''
            SELECT * FROM Pizza
            WHERE Type = :item_name
            AND Size = :item_size
        ''')
    elif category == "Drink":
        query = text('''
            SELECT * FROM Drink
            WHERE Name = :item_name
            AND Size = :item_size
        ''')
    elif category == "Dessert":
        query = text('''
            SELECT * FROM Dessert
            WHERE Type = :item_name
        ''')
    else:
        return 0

    with engine.connect() as connection:
        with connection.begin() as transaction:
            result = connection.execute(query, {"item_name": item_name, "item_size": item_size})
            price = result.fetchone()
            print(price)
            print(query)
            if price:
                return price[2]

    return 0

