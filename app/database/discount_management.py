from sqlalchemy import text
from datetime import datetime, timedelta
from app.database.account_management import get_customer_id
from app.database.database import get_engine
from app.database.queries import get_pizza_id, get_drink_id, get_dessert_id

engine = get_engine()

def check_if_discount():
    customer_id = get_customer_id()
    query = text('''
        SELECT NumberOfOrders
        FROM Customer
        WHERE CustomerID = :customer_id
    ''')

    with engine.connect() as connection:
        result = connection.execute(query, {'customer_id': customer_id})
        number = result.fetchone()

    if number is not None:
        number_of_orders = number[0]  # Extract the value from the tuple
        return number_of_orders % 10
    else:
        return False  # In case the customer is not found or NumberOfOrders is NULL

def add_an_order_to_order_sum():
    customer_id = get_customer_id()

    # Define the SQL query to increment the NumberOfOrders by 1 for the given customer
    update_query = text('''
            UPDATE Customer
            SET NumberOfOrders = NumberOfOrders + 1
            WHERE CustomerID = :customer_id
        ''')

    # Execute the query to update the database
    with engine.connect() as connection:
        connection.execute(update_query, {'customer_id': customer_id})
        connection.commit()