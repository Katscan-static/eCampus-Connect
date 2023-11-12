from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from hashlib import sha256
from datetime import datetime

uri = "mongodb+srv://madinganakn:Muhluri82129@ecampusconnect.ja8oeji.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

mydb = client["eCampusConnect"]
myusers = mydb["users"]
mycontact = mydb["contact"]

class DataHandler:

    def __init__(self, input_dict):
        self.data = input_dict.to_dict()
        self.data["created_at"] = datetime.now().isoformat()
        
    def check_email(self):
        checkuser = myusers.count_documents({"email": self.data["email"]})
        return checkuser
        
    def pw_encrypt(self):
        m = sha256()
        m.update(self.data["password"].encode('utf-8'))
        self.data["password"] = m.hexdigest()
        
    def pw_compare(self):
        
        query = {"email": self.data["email"]}
        document = myusers.find_one(query)
        
        if document:
            pw = document.get("password")
            if pw == self.data["password"]:
                return "valid"
            else:
                return "Please insert the correct password, INVALID PASSWORD!"
        else:
            return f"User with {self.data['email']} is not registerd please signup"
            
    def insert(self):
        myusers.insert_one(self.data)
    
    def insert_contact(self):
        mycontact.insert_one(self.data)