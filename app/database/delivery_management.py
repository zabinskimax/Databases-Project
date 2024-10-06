from app.database.database import get_engine
from sqlalchemy import text

from datetime import datetime, timedelta

engine = get_engine()


def assign_delivery_to_grouped_orders(order_id, postal_code):
    # Get the current time using Python's datetime module
    current_time = datetime.now()
    # Retrieve the order_time from the order with the given order_id
    fetch_order_time_query = text('''
            SELECT order_time FROM OrderDeliveries
            WHERE order_id = :order_id
        ''')

    with engine.connect() as connection:
        result = connection.execute(fetch_order_time_query, {'order_id': order_id})
        order = result.fetchone()

    if not order:
        print(f"Order with ID {order_id} not found.")
        return

    # Extract the order_time from the result
    order_time = order[0]  # Assuming `order_time` is at index 0
    print(f"Order time for order {order_id}: {order_time}")
    # Get a delivery person for the postal code using the `assign_delivery` method
    delivery_person = assign_delivery(postal_code)[0]
    print('assigning delivery person ID: ', delivery_person)

    if delivery_person:
        delivery_person_id = delivery_person  # Assuming ID is at index 0
        print("Parameters being passed to the query:")
        print(f"Postal Code: {postal_code}")
        print(f"Delivery Person ID: {delivery_person_id}")
        print(f"Order Time for Comparison: {order_time}")
        # Assign this delivery person to all unassigned orders with the same postal code
        assign_delivery_query = text('''
                    UPDATE OrderDeliveries
                    SET delivery_person_id = :delivery_person_id
                    WHERE delivery_postal_code = :postal_code
                    AND (delivery_person_id IS NULL OR delivery_person_id = 0)
                    AND TIMESTAMPDIFF(MINUTE, order_time, :order_time) <= 3
                    ORDER BY order_time ASC
                    LIMIT 3
                ''')

        with engine.connect() as connection:
            connection.execute(assign_delivery_query, {
                'delivery_person_id': delivery_person_id,
                'postal_code': postal_code,
                'order_time': order_time  # Pass the order_time as a parameter
            })
            connection.commit()
            # Check how many rows were updated
            print(f"Rows affected: {result.rowcount}")

        # Now update the delivery person's last_delivery_start_time
        update_delivery_person_time_query = text('''
                    UPDATE DeliveryPerson
                    SET last_delivery_start_time = :new_delivery_time
                    WHERE delivery_person_id = :delivery_person_id
                ''')

        # Calculate the new delivery start time (order_time + 3 minutes)
        new_delivery_time = order_time + timedelta(minutes=3)

        with engine.connect() as connection:
            # Execute the update to modify the last_delivery_start_time for the delivery person
            connection.execute(update_delivery_person_time_query, {
                'delivery_person_id': delivery_person_id,
                'new_delivery_time': new_delivery_time  # Use order_time + 3 minutes
            })
            connection.commit()


def assign_delivery(assigned_area):
    # Calculate 30 minutes ago (2.5 hours)
    half_hour_ago = datetime.now() - timedelta(minutes=30)

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
        if delivery_person is not None:
            update_query = text('''
                    UPDATE DeliveryPerson
                    SET last_delivery_start_time = DATE_ADD(NOW(), INTERVAL 2 HOUR)
                    WHERE delivery_person_id = :delivery_person_id
                ''')

            connection.execute(update_query, {'delivery_person_id': delivery_person[0]})
            connection.commit()
        return delivery_person
