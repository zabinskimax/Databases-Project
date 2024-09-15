from sqlalchemy import create_engine, text
import re
from datetime import datetime

# Define your MySQL database credentials
username = 'admin'
password = 'ktGl4r&<,bNY'
host = 'databases-project.ctsm8y2g4qex.eu-north-1.rds.amazonaws.com'
port = '3306'
database = 'boneless_pizza'

# Create the database engine
db_url = f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}'
engine = create_engine(db_url)


def log_in(email, password):
    # Construct the SQL query to check for the user
    query = text('''
            SELECT * FROM Customer WHERE email = :email AND password = :password
        ''')

    # Execute the query with the provided email and password
    with engine.connect() as connection:
        result = connection.execute(query, {'email': email, 'password': password})
        user = result.fetchone()


    if user:
            print(f"User {user[0]} logged in successfully!")
    else:
        # User not found, login failed
        print("Invalid email or password.")


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
    insert_statement = text('''
        INSERT INTO Customer (Name, Gender, Birthdate, PhoneNumber, Address, Email, Password, NumberOfOrders) VALUES (
            :name, :gender, :birthdate, :phone, :address, :email, :password, :number_of_orders
        )
    ''')

    params = {
        'name': name,
        'gender': gender,
        'birthdate': birthdate,
        'phone': phone,
        'address': address,
        'email': email,
        'password': password,
        'number_of_orders': number_of_orders
    }

    with engine.connect() as connection:
        result = connection.execute(insert_statement, params)
        connection.commit()
        print(f'Customer {name} added successfully.')


def take_order():
    print('take order')

def get_engine():
    return engine
