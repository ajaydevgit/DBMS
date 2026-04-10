import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists (for local development)
load_dotenv()

def get_database():
    """
    Connects to MongoDB using the MONGO_URI environment variable. 
    Defaults to localhost if the variable is not set.
    """
    # Cloud connection string or local fallback
    connection_string = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
    
    try:
        # Create a connection using MongoClient
        client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
        
        # Test the connection
        client.server_info() 
        
        # Return the database object. It will create 'library_system' if it doesn't exist
        return client['library_system']
        
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        print("Ensure MongoDB is running locally, or your MONGO_URI is correct.")
        sys.exit(1)
