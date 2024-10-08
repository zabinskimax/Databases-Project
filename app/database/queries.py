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


def get_pizza_types():
    query = text('''
        SELECT DISTINCT Type
        FROM PizzaType
    ''')

    with engine.connect() as connection:
        result = connection.execute(query)
        pizza_types = {row[0] for row in result.fetchall()}

    return list(pizza_types)


def get_pizza_ingredients(pizza_type):
    query = text('''
        SELECT i.Name, i.IsVegetarian, i.IsVegan
        FROM Ingredient i
        JOIN PizzaIngredients pi ON i.IngredientID = pi.IngredientID
        JOIN PizzaType pt ON pi.PizzaTypeID = pt.PizzaTypeID
        WHERE pt.Type = :pizza_type
    ''')

    with engine.connect() as connection:
        result = connection.execute(query, {'pizza_type': pizza_type})
        ingredients = result.fetchall()

    is_vegetarian = all(row[1] for row in ingredients)  # True if all ingredients are vegetarian
    is_vegan = all(row[2] for row in ingredients)  # True if all ingredients are vegan

    # Return the list of ingredients and whether they are vegetarian/vegan
    return [row[0] for row in ingredients], is_vegetarian, is_vegan

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



def check_price_with_details(category, item_name, item_size, detailed=False):
    """
    This function calculates the price of an item (e.g., pizza, drink, dessert).
    If `detailed=True`, it returns the price breakdown including ingredients, base price, profit margin, and VAT.
    Otherwise, it returns only the final price.
    """
    if category == "Pizza":
        # Query to get the price of each ingredient for a specific pizza type
        query = text('''
            SELECT i.Name, i.PricePerUnit
            FROM PizzaType pt
            JOIN PizzaIngredients pi ON pt.PizzaTypeID = pi.PizzaTypeID
            JOIN Ingredient i ON pi.IngredientID = i.IngredientID
            WHERE pt.Type = :item_name
        ''')

        # Size multiplier for different pizza sizes
        size_multiplier = {
            "Small": 1.0,
            "Medium": 1.3,
            "Large": 1.6
        }

        base_price = 3.2  # The base price for all pizzas
        profit_margin_rate = 0.40  # 40% profit margin
        vat_rate = 0.09  # 9% VAT

        detailed_price_info = ""  # To store the breakdown of ingredients and their prices

        multiplier = size_multiplier.get(item_size, 1.0)  # Get the appropriate size multiplier

        with engine.connect() as connection:
            with connection.begin() as transaction:
                result = connection.execute(query, {"item_name": item_name})
                ingredients = result.fetchall()

                total_ingredient_price = 0.0

                # Build the detailed price info string and calculate the total ingredient price
                for ingredient in ingredients:
                    ingredient_name = ingredient[0]
                    ingredient_price = float(ingredient[1]) * multiplier  # Apply size multiplier
                    total_ingredient_price += ingredient_price
                    if detailed:
                        detailed_price_info += f"{ingredient_name}: ${ingredient_price:.2f} (x{multiplier})\n"

                # Multiply the base price by the size multiplier
                total_base_price = base_price * multiplier

                # Calculate the total cost price (ingredients + base)
                total_cost_price = total_base_price + total_ingredient_price

                # Apply the 40% profit margin
                total_price_with_profit = total_cost_price * (1 + profit_margin_rate)

                # Apply the 9% VAT
                final_price_with_vat = total_price_with_profit * (1 + vat_rate)

        # If detailed breakdown is requested
        if detailed:
            detailed_price_info += f"Base Price: ${total_base_price:.2f} (x{multiplier})\n"
            detailed_price_info += f"Ingredient Total: ${total_ingredient_price:.2f}\n"
            detailed_price_info += f"Cost Price: ${total_cost_price:.2f}\n"
            detailed_price_info += f"Profit Margin (40%): ${total_price_with_profit - total_cost_price:.2f}\n"
            detailed_price_info += f"Price with Profit: ${total_price_with_profit:.2f}\n"
            detailed_price_info += f"VAT (9%): ${final_price_with_vat - total_price_with_profit:.2f}\n"
            detailed_price_info += f"Final Price: ${final_price_with_vat:.2f}\n"

            return final_price_with_vat, detailed_price_info

        # Return only the final price if no detailed breakdown is requested
        return final_price_with_vat

    # For other categories like "Drink" and "Dessert", no changes needed, return price directly
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
                return price[0] if not detailed else (price[0], f"Drink Price: ${price[0]:.2f}")

    elif category == "Dessert":
        query = text('''
            SELECT Price FROM Dessert
            WHERE Type = :item_name
        ''')
        with engine.connect() as connection:
            result = connection.execute(query, {"item_name": item_name})
            price = result.fetchone()
            if price:
                return price[0] if not detailed else (price[0], f"Dessert Price: ${price[0]:.2f}")

    return 0 if not detailed else (0, "No price available")




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


def check_if_admin():
    customer_id = get_customer_id()  # Assuming this function retrieves the current customer's ID

    # SQL query to check if the customer is an admin
    query = text('''
        SELECT isAdmin
        FROM Customer
        WHERE CustomerID = :customer_id
    ''')

    with engine.connect() as connection:
        # Execute the query to get the isAdmin value for the customer
        result = connection.execute(query, {'customer_id': customer_id})
        admin_status = result.scalar()

        # Check if the admin status is True (1)
        return bool(admin_status)  # Returns True if isAdmin is 1, otherwise False

