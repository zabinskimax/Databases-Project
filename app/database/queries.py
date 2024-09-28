import re
from datetime import datetime, timedelta

from sqlalchemy import text

from app.database.account_management import get_customer_id
from app.database.database import get_engine

engine = get_engine()


def get_pizza_id(pizza_type):
    query = text('''
        SELECT pt.PizzaTypeID
        FROM PizzaType pt
        WHERE pt.Type = :pizza_type
    ''')

    with engine.connect() as connection:
        result = connection.execute(query, {'pizza_type': pizza_type})
        pizza_type_id = result.scalar()

    if pizza_type_id:
        return pizza_type_id
    else:
        return None

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
    query = text('''
        SELECT DISTINCT Type
        FROM PizzaType
    ''')

    with engine.connect() as connection:
        result = connection.execute(query)
        pizza_types = {row[0] for row in result.fetchall()}

    return list(pizza_types)


def get_pizza_ingredients():
    query = text('''
        SELECT DISTINCT i.Name
        FROM Ingredient i
        JOIN PizzaIngredients pi ON i.IngredientID = pi.IngredientID
        JOIN PizzaType pt ON pi.PizzaTypeID = pt.PizzaTypeID
    ''')

    with engine.connect() as connection:
        result = connection.execute(query)
        ingredient_types = {row[0] for row in result.fetchall()}

    return list(ingredient_types)

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
        # For pizzas, we need to join the PizzaType, PizzaIngredients, and Ingredient tables
        ingredient_query = text('''
            SELECT i.Name
            FROM PizzaType pt
            JOIN PizzaIngredients pi ON pt.PizzaTypeID = pi.PizzaTypeID
            JOIN Ingredient i ON pi.IngredientID = i.IngredientID
            WHERE pt.Type = :food_type
        ''')
        with engine.connect() as connection:
            with connection.begin() as transaction:
                result = connection.execute(ingredient_query, {'food_type': food_type})
                pizza_ingredients = result.fetchall()

                if pizza_ingredients:
                    # Extract just the ingredient names
                    ingredient_names = [ingredient[0] for ingredient in pizza_ingredients]
                    return ingredient_names
                else:
                    return "No information available."

    return "Category not supported."


def check_price(category, item_name, item_size):
    if category == "Pizza":
        # Query to sum the price of ingredients for a specific pizza type
        query = text('''
            SELECT SUM(i.PricePerUnit) AS total_ingredient_price
            FROM PizzaType pt
            JOIN PizzaIngredients pi ON pt.PizzaTypeID = pi.PizzaTypeID
            JOIN Ingredient i ON pi.IngredientID = i.IngredientID
            WHERE pt.Type = :item_name
        ''')

        size_multiplier = {
            "Small": 1.0,
            "Medium": 1.5,
            "Large": 2.0
        }

        base_price = 7.0  # The base price for all pizzas

        with engine.connect() as connection:
            with connection.begin() as transaction:
                result = connection.execute(query, {"item_name": item_name})
                total_ingredient_price = result.scalar()

                if total_ingredient_price is not None:
                    # Add the base price to the total ingredient price
                    total_price = base_price + float(total_ingredient_price)

                    # Apply the size multiplier to the base ingredient price
                    pizza_price = total_price * size_multiplier.get(item_size, 1.0)
                    return pizza_price

    elif category == "Drink":
        query = text('''
            SELECT Price FROM Drink
            WHERE Name = :item_name
            AND Size = :item_size
        ''')
        with engine.connect() as connection:
            result = connection.execute(query, {"item_name": item_name, "item_size": item_size})
            price = result.fetchone()
            if price:
                return price[0]

    elif category == "Dessert":
        query = text('''
            SELECT Price FROM Dessert
            WHERE Type = :item_name
        ''')
        with engine.connect() as connection:
            result = connection.execute(query, {"item_name": item_name})
            price = result.fetchone()
            if price:
                return price[0]

    return 0


def check_if_birthday():
    customer_id = get_customer_id()  # Assuming this function retrieves the current customer's ID
    today = datetime.today()

    # SQL query to check if today is the customer's birthday
    birthday_query = text('''
        SELECT COUNT(*)
        FROM Customer
        WHERE CustomerID = :customer_id
        AND MONTH(Birthdate) = :current_month
        AND DAY(Birthdate) = :current_day
    ''')

    # SQL query to check if the customer has already ordered today
    order_query = text('''
        SELECT COUNT(*)
        FROM OrderDeliveries
        WHERE customer_id = :customer_id
        AND DATE(order_time) = :today_date
    ''')

    with engine.connect() as connection:
        # Execute the birthday query
        birthday_result = connection.execute(birthday_query, {
            'customer_id': customer_id,
            'current_month': today.month,
            'current_day': today.day
        })

        # Check if today is the customer's birthday
        birthday_count = birthday_result.scalar()

        if birthday_count == 0:
            return False

        # Execute the order query to check if the customer has already ordered today
        order_result = connection.execute(order_query, {
            'customer_id': customer_id,
            'today_date': today.date()
        })

        # Check if the customer has ordered today
        order_count = order_result.scalar()
        print(order_count)
        # If the customer has already placed an order today, return False
        return order_count == 0
