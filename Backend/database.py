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
    
    
def findLongestMessage():
    collection = postContent()
    messages = collection.find({})
    longest_message = ""
    for message in messages:
        if 'content' in message and len(message['content']) > len(longest_message):
            longest_message = message['content']
    return longest_message