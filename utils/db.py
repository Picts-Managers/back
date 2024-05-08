import os

from pymongo import MongoClient
from pymongo.database import Database

db: MongoClient = None
client: Database = None


def init_db_client():
    global client, db
    db = MongoClient(os.getenv("DB_URI"))
    client = db[os.getenv("DB_NAME")]
