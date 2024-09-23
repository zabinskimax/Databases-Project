from sqlalchemy import create_engine

# Define your MySQL database credentials
username = 'admin'
password = 'ktGl4r&<,bNY'
host = 'databases-project.ctsm8y2g4qex.eu-north-1.rds.amazonaws.com'
port = '3306'
database = 'boneless_pizza'

# Create the database engine
db_url = f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}'
engine = create_engine(db_url)

def get_engine():
    return engine
