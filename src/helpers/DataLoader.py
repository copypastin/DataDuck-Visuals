from pymongo import MongoClient 
from dotenv import load_dotenv
import pandas as pd
import os


class DataLooder():
    
    def __init__(self, DBname, CollName) -> None:

        load_dotenv("secrets.env")
        MONGO_URI = os.getenv("MONGODB_URI")


        if not MONGO_URI:
            raise ValueError("MONGODB_URI could not be found. Please set your key in the secrets.env file")


        client = MongoClient(MONGO_URI)
        db = client.get_database(DBname)
        collection = db.get_collection(CollName)

        self.data = pd.DataFrame(list(collection.find()))

    def get_data(self) -> pd.DataFrame:
        return self.data

