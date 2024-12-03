from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("URI")
client = MongoClient(MONGO_URI)

db = client["Students"]

students_collection = db["students"]
