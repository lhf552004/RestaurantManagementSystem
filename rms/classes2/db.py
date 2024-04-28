import mysql.connector as mysql
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

class DB:
    # Constructor of Database Class
    def __init__(self):
        # instance of database object that connects us to the database
        self._db = mysql.connect(
               host=db_host,
               user=db_user,
               password=db_password,
               database=db_name
            )  # rms_final_project
        # Closing the database Connection
        self._db.close()

    # It is function that gets takes query and values and perform the query on database;
    # This function is only used for query that are related to getting the information from database;
    # It returns the result after getting from the database
    def fetch(self, query, values=None):
        try:
            self._db.reconnect()
            cursor = self._db.cursor()
            if values is None:
                cursor.execute(query)
            else:
                cursor.execute(query, values)
            result = cursor.fetchall()
            cursor.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            result = []
        finally:
            if self._db.is_connected():
                self._db.close()
        return result

    # It is a function that also takes the query and values to perform the query on database
    # This function is only used for query where there is only execution is need; no data to get from database
    # It returns the status of query executed on the database
    def execute(self, query, values):
        self._db.reconnect()
        cursor = self._db.cursor()
        cursor.execute(query, values)
        # row_count = cursor.rowcount
        self._db.commit()
        row_last_id = cursor.lastrowid
        cursor.close()
        self._db.close()
        return row_last_id
