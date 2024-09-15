from sqlalchemy import create_engine, text

from app.GUI.gui import execute_gui

# Define your MySQL database credentials
username = 'admin'
password = 'ktGl4r&<,bNY'
host = 'databases-project.ctsm8y2g4qex.eu-north-1.rds.amazonaws.com'
port = '3306'
database = 'boneless_pizza'

db_url = f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}'

engine = create_engine(db_url)

# Connect to the database
with engine.connect() as connection:

    result = connection.execute(text('SELECT * FROM Customer'))

    # Fetch and print the result
    for row in result:
        print(row)

    execute_gui()