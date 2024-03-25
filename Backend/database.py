from pymongo import MongoClient

def loginAndRegisterDataBase():
    client = MongoClient("mongo")
    db = client["login"]
    collection = db["login"]
    return collection
    
def postContent():
    client = MongoClient("mongo")
    db = client["content"]
    collection = db["enginner"]
    return collection
    
    
    