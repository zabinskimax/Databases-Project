from app.database.database import get_engine
from sqlalchemy import text

from datetime import datetime, timedelta

engine = get_engine()

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
        print(delivery_person)
        if delivery_person is not None:
            print(delivery_person[0])
            update_query = text('''
                    UPDATE DeliveryPerson
                    SET last_delivery_start_time = DATE_ADD(NOW(), INTERVAL 2 HOUR)
                    WHERE delivery_person_id = :delivery_person_id
                ''')

            connection.execute(update_query, {'delivery_person_id': delivery_person[0]})
            connection.commit()
        return delivery_person
