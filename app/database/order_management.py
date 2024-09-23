

from sqlalchemy import text
from datetime import datetime, timedelta
from app.database.account_management import get_customer_id
from app.database.database import get_engine
from app.database.queries import get_pizza_id, get_drink_id, get_dessert_id

engine = get_engine()


def insert_order(takeaway, total_amount, order_status, discount, payed, order_details, delivery_address, payment_method):
    customer_id = get_customer_id()

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

def take_order(take_away, total_amount, order_status, discount, payed):
    customer_id = get_customer_id()
    query = text('''
        INSERT INTO orders (CustomerID, TakeAway, TotalAmount, OrderStatus, Discount, Payed)
        VALUES (:customer_id, :take_away, :total_amount, :order_status, :discount, :payed)
    ''')

    with engine.connect() as connection:
        connection.execute(query, customer_id=customer_id, take_away=take_away, total_amount=total_amount, order_status=order_status, discount=discount, payed=payed)

def cancel_latest_order():
    customer_id = get_customer_id()
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

def check_latest_order_status():
    customer_id = get_customer_id()
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
