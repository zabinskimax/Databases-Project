from sqlalchemy import create_engine, text
import re
from datetime import datetime

from app.password_hashing import hash_password, verify_password

from datetime import datetime, timedelta

# Define your MySQL database credentials
username = 'admin'
password = 'ktGl4r&<,bNY'
host = 'databases-project.ctsm8y2g4qex.eu-north-1.rds.amazonaws.com'
port = '3306'
database = 'boneless_pizza'

# Create the database engine
db_url = f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}'
engine = create_engine(db_url)

customer_id = None

def log_in(email, password):
    # Construct the SQL query to check for the user
    query = text('''
            SELECT * FROM Customer WHERE email = :email
        ''')

    with engine.connect() as connection:
        result = connection.execute(query, {'email': email})
        user = result.fetchone()

    if not user:
        # User not found, login failed
        print("Invalid email or password.")
        return

    # Verify password using bcrypt
    if not verify_password(user.Password, password):
        print("Invalid email or password.")
        return
        # Login successful
    print(f"User {user} logged in successfully!")
    customer_id = user[0]
    return True

def create_account(name, gender, birthdate, phone, address, email, password, number_of_orders):
    # Basic validation
    if not name or not gender or not birthdate or not email or not password:
        print("All required fields must be filled.")
        return

    if gender not in ['male', 'female', 'other']:
        print("Invalid gender.")
        return

    try:
        datetime.strptime(birthdate, '%Y-%m-%d')  # Validate birthdate format
    except ValueError:
        print("Invalid birthdate format. Use YYYY-MM-DD.")
        return

    try:
        number_of_orders = int(number_of_orders)
    except ValueError:
        print("Number of orders must be an integer.")
        return

    check_email_query = text('''
            SELECT 1 FROM Customer WHERE email = :email
        ''')
    with engine.connect() as connection:
        result = connection.execute(check_email_query, {'email': email})
        exists = result.fetchone()

    if exists:
        print("Email address already exists. Please choose a different email.")
        return

    hashed_password = hash_password(password)
    print(hashed_password)

    insert_statement = text('''
        INSERT INTO Customer (Name, Gender, Birthdate, PhoneNumber, Address, Email, Password, NumberOfOrders) VALUES (
            :name, :gender, :birthdate, :phone, :address, :email, :hashed_password, :number_of_orders
        )
    ''')

    params = {
        'name': name,
        'gender': gender,
        'birthdate': birthdate,
        'phone': phone,
        'address': address,
        'email': email,
        'hashed_password': hashed_password,
        'number_of_orders': number_of_orders
    }

    with engine.connect() as connection:
        result = connection.execute(insert_statement, params)
        connection.commit()
        print(f'Customer {name} added successfully.')



def take_order(take_away, total_amount, order_status, discount, payed):
    query = text('''
        INSERT INTO orders (CustomerID, TakeAway, TotalAmount, OrderStatus, Discount, Payed)
        VALUES (:customer_id, :take_away, :total_amount, :order_status, :discount, :payed)
    ''')

    with engine.connect() as connection:
        connection.execute(query, customer_id=customer_id, take_away=take_away, total_amount=total_amount, order_status=order_status, discount=discount, payed=payed)


def assign_delivery(designated_area):
    # Calculate half an hour ago
    half_hour_ago = datetime.now() - timedelta(minutes=30)

    query = text('''
            SELECT * FROM DeliveryPerson
            WHERE designated_area = :designated_area
            AND last_delivery_start_time < :half_hour_ago
            ORDER BY last_delivery_start_time ASC
            LIMIT 1
        ''')

    with engine.connect() as connection:
        result = connection.execute(query, designated_area=designated_area, half_hour_ago=half_hour_ago)
        delivery_person = result.fetchone()

        if delivery_person:
            update_query = text('''
                    UPDATE DeliveryPerson
                    SET last_delivery_start_time = :now
                    WHERE id = :delivery_person_id
                ''')

            connection.execute(update_query, now=datetime.now(), delivery_person_id=delivery_person.id)

        return delivery_person


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

def take_order():
    print('take order')

def get_engine():
    return engine
