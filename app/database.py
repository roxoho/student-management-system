from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# MongoDB Connection
MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.client = MongoClient(MONGODB_URI)
            cls._instance.db = cls._instance.client[DATABASE_NAME]
        return cls._instance

    def get_database(self):
        return self.db

    def get_students_collection(self):
        return self.db['students']

# Create a singleton database connection
database = DatabaseConnection()