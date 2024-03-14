from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
# print("DATABASE_URL:", DATABASE_URL)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# from sqlalchemy.inspection import inspect

# # Function to print all table names and their schemas
# def print_table_names_and_schemas(engine):
#     inspector = inspect(engine)
#     # Retrieve all schemas in the database
#     schemas = inspector.get_schema_names()
#     for schema in schemas:
#         print(f"Schema: {schema}")
#         # For each schema, print the table names it contains
#         for table_name in inspector.get_table_names(schema=schema):
#             print(f"Table: {table_name}")

# # Call the function to print all table names and their schemas
# print_table_names_and_schemas(engine)