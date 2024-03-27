import os

if os.getenv("ENV") == "TEST":
    import mongomock

    client = mongomock.MongoClient()

else:
    from pymongo import MongoClient

    client = MongoClient(os.getenv("DB_URI"))
