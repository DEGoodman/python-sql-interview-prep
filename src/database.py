import os
import psycopg2
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class Database:
    def __init__(self):
        self.connection: Optional[psycopg2.extensions.connection] = None
        
    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                port=os.getenv('DB_PORT', '5432'),
                database=os.getenv('DB_NAME', 'interview_practice'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD')
            )
            return self.connection
        except psycopg2.Error as e:
            print(f"Error connecting to database: {e}")
            return None
    
    def close(self):
        if self.connection:
            self.connection.close()
            
    def execute_query(self, query: str, params=None):
        if not self.connection:
            self.connect()
            
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                if cursor.description:
                    return cursor.fetchall()
                self.connection.commit()
                return cursor.rowcount
        except psycopg2.Error as e:
            self.connection.rollback()
            print(f"Error executing query: {e}")
            return None