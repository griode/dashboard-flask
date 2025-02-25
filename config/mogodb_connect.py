from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi

# Load environment variables
load_dotenv()

def get_database():
    # Get MongoDB connection string from environment variable
    MONGODB_URI = os.getenv('MONGODB_URI')
    
    # Create MongoDB client with SSL certificate verification
    client = MongoClient(MONGODB_URI, tlsCAFile=certifi.where())
    
    # Return database instance
    return client.get_database('task_dashboard')

def init_mongodb():
    try:
        db = get_database()
        # Test the connection
        db.command('ping')
        print("Successfully connected to MongoDB Atlas")
        return db
    except Exception as e:
        print(f"Error connecting to MongoDB Atlas: {e}")
        return None