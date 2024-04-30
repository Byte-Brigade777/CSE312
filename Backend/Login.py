import bcrypt
import hashlib
import uuid
from pymongo import MongoClient


# def loginAndRegisterDataBase():
#     client = MongoClient("mongo")
#     db = client["login"]
#     collection = db["login"]
#     return collection


class LoginAndRegistration:

    def __init__(self, collection):
        self.collection = collection
        self.errorMessage = ''
        self.info = ['', '']
        self.messageId = ''
        self.name = ''
        self.count = 0

    def same_password(self, password, confPassword):
        if password == confPassword:
            return True
        return False

    def existing_account(self, username):

        for i in self.collection.find():

            if i['username'] == username:
                return [True, i]

        return [False, '']

    def strong_password(self, password):
        if len(password) >= 8:
            return True
        return False

    def create_account(self, username, password, confirmPassword):

        if not self.same_password(password, confirmPassword):
            self.errorMessage = 'Password and Confirm Password dont match'
            return False
        if self.existing_account(username)[0]:
            self.errorMessage = 'Username already taken'
            return False
        if not self.strong_password(password):
            self.errorMessage = 'Password must be 8 Character minimum'
            return False
        hashedPassword = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        self.collection.insert_one({'username': username, 'password': hashedPassword, 'token': "N/A", 'xref': 'N/A','expire': 'N/A'})
        return True

    def login(self, username, password):

        info = self.existing_account(username)

        if info[0]:
            if bcrypt.checkpw(password.encode(), info[1]['password']):
                messageId = str(uuid.uuid1())
                hashedToken = hashlib.sha512(messageId.encode()).digest()
                self.collection.update_one({'username': username}, {'$set': {'token': hashedToken, 'expire': 'False'}}, upsert=True)
                self.messageId = messageId 
                self.name = username
                self.count = 1
                
                return [True, messageId]

        self.errorMessage = 'Incorrect Username or Password'

        return [False, 'Incorrect Username or Password']

    def cookie_correct(self, request):
        token = request.cookies.get('token')
        if token:
            info = self.collection.find_one({'token': hashlib.sha512(token.encode()).digest()})
            if info:
                if info.get('expire') == 'False':
                    return [True, info]
        
        return [False, '']
    
    def logout(self, request):
        
        token = request.cookies.get('token')
        if token:
            self.collection.update_one({'token': hashlib.sha512(token.encode()).digest()}, {'$set': {'expire': 'True'}}, upsert=True)
            return True
        return False
    
    def findUserName(self, cookie): 
        info = self.collection.find_one({'token': hashlib.sha512(cookie.encode()).digest()})
        if info:
            return info.get('username')
        return None
        
        
    def update_dark_mode_preference(self, username, dark_mode_enabled):
        self.collection.update_one({'username': username}, {'$set': {'dark_mode_enabled': dark_mode_enabled}})

    def get_dark_mode_preference(self, username):
        user = self.collection.find_one({'username': username})
        if user:
            return user.get('dark_mode_enabled', False)
        return False  # False if preference not found
        

        
            
        
