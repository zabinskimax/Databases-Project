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


def has_used_discount(discount_code):
    customer_id = get_customer_id()
    query = text('''
        SELECT cd.used
        FROM CustomerDiscounts cd
        JOIN Discounts d ON cd.discount_id = d.discount_id
        WHERE cd.customer_id = :customer_id AND d.discount_code = :discount_code
    ''')

    with engine.connect() as connection:
        result = connection.execute(query, {'customer_id': customer_id, 'discount_code': discount_code}).fetchone()
        return result is not None and result[0]


# Function to apply a discount code and mark it as used for the customer
def apply_discount_code(discount_code):
    customer_id = get_customer_id()

    # Get the discount details
    query = text('''
        SELECT discount_id, discount_percentage
        FROM Discounts
        WHERE discount_code = :discount_code
    ''')

    with engine.connect() as connection:
        discount = connection.execute(query, {'discount_code': discount_code}).fetchone()

        if discount is None:
            return None  # Discount code doesn't exist

        discount_id, discount_percentage = discount

        # Convert discount_percentage to float before multiplying
        discount_percentage = float(discount_percentage) * 0.01

        return discount_percentage, discount_id  # Return both percentage and discount_id


def update_discount_usage(discount_id):
    customer_id = get_customer_id()
    # Mark this discount as used by the customer
    insert_query = text('''
        INSERT INTO CustomerDiscounts (customer_id, discount_id, used)
        VALUES (:customer_id, :discount_id, TRUE)
    ''')

    with engine.connect() as connection:
        connection.execute(insert_query, {'customer_id': customer_id, 'discount_id': discount_id})
        connection.commit()
