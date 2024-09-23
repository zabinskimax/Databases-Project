from datetime import datetime

from sqlalchemy import text
from app.database.database import get_engine
from app.database.password_hashing import hash_password, verify_password
from app.database.session import session

engine = get_engine()


def log_in(email, password):
    global customer_id
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
    session.set_customer_id(user[0])
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


def get_customer_id():
    return session.get_customer_id()

