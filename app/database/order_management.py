

from sqlalchemy import text
from datetime import datetime, timedelta
from app.database.account_management import get_customer_id
from app.database.database import get_engine
from app.database.discount_management import add_an_order_to_order_sum
from app.database.queries import get_pizza_id, get_drink_id, get_dessert_id

engine = get_engine()


def insert_order(takeaway, total_amount, order_status, discount, payed, order_details, delivery_postal_code, delivery_address, payment_method):
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
        INSERT INTO OrderDeliveries (order_id, order_time, delivery_postal_code, delivery_address, payment_method, customer_id)
        VALUES (:order_id, :order_time, :delivery_postal_code, :delivery_address, :payment_method, :customer_id)
        
    ''')
    # Get the current time using datetime.now()
    current_time = datetime.now()

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
                    item_id = get_pizza_id(item['item'])
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
                'delivery_postal_code': delivery_postal_code,
                'order_time': current_time,  # Pass the current time as order_time
                'delivery_address': delivery_address,
                'payment_method': payment_method,
                'customer_id': customer_id
            })

    add_an_order_to_order_sum()
    return order_id


def cancel_latest_order():
    customer_id = get_customer_id()
    query = text('''
        SELECT od.order_id, od.cancellable_until, o.OrderStatus
        FROM OrderDeliveries od
        JOIN Orders o ON od.order_id = o.OrderID
        WHERE od.customer_id = :customer_id
        ORDER BY od.order_time DESC
        LIMIT 1
    ''')

    with engine.connect() as connection:
        result = connection.execute(query, {'customer_id': customer_id})
        order = result.fetchone()

        if not order:
            return "No orders found for this customer."

        order_id = order.order_id
        cancellable_until = order.cancellable_until + timedelta(hours=2)
        order_status = order.OrderStatus

        current_time = datetime.now()
        if current_time > cancellable_until:
            return "Cancellation period has expired."

        if order_status not in ['Being Prepared', 'Ready for Pickup']:
            return "Order cannot be canceled as it is already being delivered or completed."

        # Cancel the order
        cancel_query = text('''
            UPDATE OrderDeliveries
            SET cancellation_status = 1
            WHERE order_id = :order_id
        ''')

        order_status_update_query = text('''
            UPDATE Orders
            SET OrderStatus = 'Cancelled'
            WHERE OrderID = :order_id
        ''')

        # No need to start a new transaction if already in one
        connection.execute(cancel_query, {'order_id': order_id})
        connection.execute(order_status_update_query, {'order_id': order_id})

        return "Your order has been successfully canceled."


def check_latest_order_status():
    customer_id = get_customer_id()
    query = text('''
        SELECT od.order_id, od.order_time, od.cancellable_until, o.OrderStatus
        FROM OrderDeliveries od
        JOIN Orders o ON od.order_id = o.OrderID
        WHERE od.customer_id = :customer_id
        ORDER BY od.order_time DESC
        LIMIT 1
    ''')

    with engine.connect() as connection:
        result = connection.execute(query, {'customer_id': customer_id})
        order = result.fetchone()

        if not order:
            return "No orders found for this customer."

        order_id = order.order_id
        order_time = order.order_time
        cancellable_until = order.cancellable_until
        order_status = order.OrderStatus

        # Calculate the elapsed time since order_time
        current_time = datetime.now()
        elapsed_time = current_time - order_time

        # Determine if order_status needs to be updated
        if elapsed_time >= timedelta(minutes=30) and order_status != 'Done':
            # Update order_status to 'Done'
            update_query = text('''
                UPDATE Orders
                SET OrderStatus = 'Done'
                WHERE OrderID = :order_id
            ''')
            connection.execute(update_query, {'order_id': order_id})
            order_status = 'Done'

        elif elapsed_time >= timedelta(minutes=7) and order_status != 'Out For Delivery':
            # Update order_status to 'Out For Delivery'
            update_query = text('''
                UPDATE Orders
                SET OrderStatus = 'Out For Delivery'
                WHERE OrderID = :order_id
            ''')
            connection.execute(update_query, {'order_id': order_id})
            order_status = 'Out For Delivery'

        return (f"Order ID: {order_id}\n"
                f"Order Status: {order_status}\n"  # Corrected variable name
                f"Order Time: {order_time}\n"
                f"Cancelable Until: {cancellable_until}")
