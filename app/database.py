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


def assign_delivery(assigned_area):
    # Calculate 150 minutes ago (2.5 hours)
    half_hour_ago = datetime.now() - timedelta(minutes=150)

    query = text('''
                SELECT * FROM DeliveryPerson
                WHERE assigned_area = :assigned_area
                AND (last_delivery_start_time < :half_hour_ago OR last_delivery_start_time IS NULL)
                ORDER BY last_delivery_start_time ASC
                LIMIT 1
            ''')

    with engine.connect() as connection:
        result = connection.execute(query, {'assigned_area': assigned_area, 'half_hour_ago': half_hour_ago})
        delivery_person = result.fetchone()

        if delivery_person:
            update_query = text('''
                    UPDATE DeliveryPerson
                    SET last_delivery_start_time = :now
                    WHERE delivery_person_id = :delivery_person_id
                ''')

            connection.execute(update_query, {'now': datetime.now(), 'delivery_person_id': delivery_person.delivery_person_id})

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


def insert_order(takeaway, total_amount, order_status, discount, payed, order_details, delivery_address, payment_method):
    global customer_id

    # Insert into Orders table
    order_query = text('''
        INSERT INTO Orders (CustomerID, TakeAway, TotalAmount, OrderStatus, Discount, Payed)
        VALUES (:customer_id, :takeaway, :total_amount, :order_status, :discount, :payed)
    ''')

    # Insert into OrderItems table
    order_item_query = text('''
        INSERT INTO OrderItems (OrderID, ItemType, ItemID, Quantity)
        VALUES (:order_id, :item_type, :item_id, :quantity)
    ''')

    # Insert into OrderDeliveries table, excluding cancellable_until
    delivery_query = text('''
        INSERT INTO OrderDeliveries (order_id, delivery_address, payment_method, delivery_status, customer_id)
        VALUES (:order_id, :delivery_address, :payment_method, 'Being Prepared', :customer_id)
    ''')
    # Get the current time using datetime.now()
    with engine.connect() as connection:
        with connection.begin():
            # Step 1: Insert the main order into Orders table
            result = connection.execute(order_query, {
                'customer_id': customer_id,
                'takeaway': takeaway,
                'total_amount': total_amount,
                'order_status': order_status,
                'discount': discount,
                'payed': payed
            })

            # Retrieve the last inserted OrderID
            order_id = connection.execute(text("SELECT LAST_INSERT_ID()")).scalar()

            # Step 2: Insert each item into the OrderItems table
            for item in order_details:
                if item['category'] == 'Pizza':
                    item_id = get_pizza_id(item['item'], item['size'])
                    item_type = 'Pizza'
                elif item['category'] == 'Drink':
                    item_id = get_drink_id(item['item'], item['size'])
                    item_type = 'Drink'
                elif item['category'] == 'Dessert':
                    item_id = get_dessert_id(item['item'])
                    item_type = 'Dessert'
                else:
                    continue

                if item_id:
                    connection.execute(order_item_query, {
                        'order_id': order_id,
                        'item_type': item_type,
                        'item_id': item_id,
                        'quantity': 1  # Assuming quantity is 1 for now, adjust as needed
                    })

            # Step 3: Insert into the OrderDeliveries table without specifying cancellable_until
            connection.execute(delivery_query, {
                'order_id': order_id,
                'delivery_address': delivery_address,
                'payment_method': payment_method,
                'customer_id': customer_id
            })

    return order_id


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


def check_latest_order_status():
    global customer_id
    query = text('''
        SELECT order_id, delivery_status, order_time, cancellable_until
        FROM OrderDeliveries
        WHERE customer_id = :customer_id
        ORDER BY order_time DESC
        LIMIT 1
    ''')

    with engine.connect() as connection:
        result = connection.execute(query, {'customer_id': customer_id})
        order = result.fetchone()

        if not order:
            return "No orders found for this customer."

        order_id = order.order_id
        status = order.delivery_status
        order_time = order.order_time
        cancellable_until = order.cancellable_until

        return (f"Order ID: {order_id}\n"
                f"Order Status: {status}\n"
                f"Order Time: {order_time}\n"
                f"Cancelable Until: {cancellable_until}")


def cancel_latest_order():
    global customer_id
    query = text('''
        SELECT order_id, cancellable_until, delivery_status
        FROM OrderDeliveries
        WHERE customer_id = :customer_id
        ORDER BY order_time DESC
        LIMIT 1
    ''')

    with engine.connect() as connection:
        result = connection.execute(query, {'customer_id': customer_id})
        order = result.fetchone()

        if not order:
            return "No orders found for this customer."

        order_id = order.order_id
        cancellable_until = order.cancellable_until + timedelta(hours=2)
        delivery_status = order.delivery_status

        current_time = datetime.now()
        if current_time > cancellable_until:
            print(current_time)
            print(cancellable_until)
            return "Cancellation period has expired."

        if delivery_status not in ['Being Prepared', 'Ready for Pickup']:
            return "Order cannot be canceled as it is already being delivered or completed."

        # Cancel the order
        cancel_query = text('''
            UPDATE OrderDeliveries
            SET cancellation_status = 1, delivery_status = 'Cancelled'
            WHERE order_id = :order_id
        ''')

        connection.execute(cancel_query, {'order_id': order_id})
        return "Your order has been successfully canceled."

def get_account_information():
    global customer_id
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
def get_food_ids(order):
    print('yes')

def get_engine():
    return engine
