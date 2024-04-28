import mysql.connector
import json
import os
# Database Class
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Accessing variables
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
db_host = os.getenv('DB_HOST')

# Function to connect to the MySQL database
def connect_to_db():
    return mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

# Function to read JSON data from a file
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to insert categories and menu items into the database
def insert_data_into_db(data):
    db = connect_to_db()
    cursor = db.cursor()

    # Insert categories first
    categories = set(item['type'] for item in data)
    for category in categories:
        cursor.execute("INSERT INTO category (category_name) VALUES (%s) ON DUPLICATE KEY UPDATE category_name=category_name;", (category,))

    # Insert menu items
    for item in data:
        cursor.execute("""
        INSERT INTO menu (food_name, price, category_id) 
        VALUES (%s, %s, (SELECT id FROM category WHERE category_name = %s))
        ON DUPLICATE KEY UPDATE price=VALUES(price);
        """, (item['name'], item['price'], item['type']))

    db.commit()
    cursor.close()
    db.close()

# Main function to control the workflow
def main():
    file_path = 'products.json'  # Path to your JSON file
    menu_data = read_json_file(file_path)
    insert_data_into_db(menu_data)

if __name__ == '__main__':
    main()
