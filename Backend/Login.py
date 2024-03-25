import bcrypt
import hashlib
import uuid 
from pymongo import MongoClient

def loginAndRegisterDataBase():
    client = MongoClient("mongo")
    db = client["login"]
    collection = db["login"]
    return collection
class LoginAndRegistration:
    
    def __init__(self, collection):
        self.collection = collection    
        self.errorMessage = ''
    
    def same_password(self, password, confPassword):
        if password == confPassword:
            return True
        return False
                
    def existingAccount(self,username):
        
        for i in self.collection.find():
            
            if i['username'] == username:
                
                return [True, i]
        
        return [False, '']
    
    def strongPassword(self, password):
        if len(password) >= 8:
            return True
        return False
        
    def create_account(self, username, password, confirmPassword):
        
        if not self.same_password(password, confirmPassword):
            self.errorMessage = 'Password and Confirm Password don\'t match'
            return False
        if self.existingAccount(username)[0]:
            self.errorMessage = 'Username already taken'
            return False
        if not self.strongPassword(password):
            self.errorMessage = 'Password must be at least 8 characters'
            return False
        hashedPassword = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self.collection.insert_one({'username': username, 'password': hashedPassword, 'token':"N/A", 'xref':'N/A'})
        return True
    
    def login(self, username, password):
        
        info = self.existingAccount(username)
        
        if info[0]: 
            if bcrypt.checkpw(password.encode(), info[1]['password']):
                id = str(uuid.uuid1())
                hashedToken = hashlib.sha512(id.encode()).digest()
                self.collection.update_one({'username': username}, {'$set': {'token': hashedToken}}, upsert=True)
                
                return [True, id]
        
        
        self.errorMessage = 'Incorrect Username or Password'    
            
        return [False, 'Incorrect Username or Password']

                
            
    
    
    