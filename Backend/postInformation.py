from Backend.Login import LoginAndRegistration
class StoreInformation:
    
    def __init__(self, collection, account: LoginAndRegistration):
        self.collection = collection
        self.account = account
        
        
    def storeRequest(self, title,content,filename,request):
        token = request.cookies.get('token')
        username = self.account.findUserName(token)
        # json = request.json
        # upload_name = request.json.get('filename')
        self.collection.insert_one({'username': username, 'title': title, 'content': content, 'url':filename if filename else None})
        return
    
    def sendPost(self, request):
        info = []
        for i in self.collection.find():
            i.pop('_id')
            info.append(i)
            
        return info
        
        
        