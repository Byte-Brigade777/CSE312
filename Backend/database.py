from pymongo import MongoClient

def loginAndRegisterDataBase():
    client = MongoClient("mongo")
    db = client["login"]
    collection = db["login"]
    return collection
    
    
    