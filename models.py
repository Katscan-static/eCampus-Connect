from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_login import UserMixin
from datetime import datetime
import hashlib
import secrets

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


class User_data:
    """Handles retrieval of user data."""
    

    def __init__(self, user_id):
        """Initialize the User_data object."""
        self.user_id = user_id

    def query_user_by_id(self):
        """Query the database for user data based on user ID."""
        query = {"email": self.user_id}  # Replace with the actual field name that stores user IDs
        user_data = myusers.find_one(query)
        return user_data


class User(UserMixin):
    """Represents a user object."""
    
    def __init__(self, user_data):
        self.email = user_data.get("email")
        self.name = user_data.get("name")
        self.message = None
        self.submit = None

        if 'phone_number' in user_data:
            self.phone_number = user_data.get("phone_number")
            self.created_at = datetime.now().isoformat()
            user_data["created_at"] = self.created_at

            if user_data["submit"] == "Send Message":
                self.message = user_data.get("message")
                self.institution = user_data.get("institution")

        if 'password' in user_data:
            self.password = user_data["password"]
            self.pw_encrypt()

        print(self.__dict__)

    def check_email(self):
        """Check if the user's email exists in the database."""
        check_user = myusers.count_documents({'email': self.email})
        return check_user

    def pw_encrypt(self):
        """Encrypt the user's password using SHA-256."""
        m = hashlib.sha256()
        m.update(self.password.encode('utf-8'))
        self.password = m.hexdigest()

    def pw_compare(self):
        """Compare the user's password with the stored password in the database."""
        query = {'email': self.email}
        document = myusers.find_one(query)

        if document:
            stored_pw = document.get("password")
            if stored_pw == self.password:
                return User(document)
            else:
                return "Invalid password. Please try again"
        else:
            return f"User with {self.email} is not registered. Please sign up."

    def save_to_db(self):
        """Save user data to the appropriate collection."""
        if self.message is None:
            self.rmv_submit_msg()
            myusers.insert_one(self.__dict__)
        else:
            self.rmv_submit()
            mycontact.insert_one(self.__dict__)

    def get_id(self):
        """Return user email as the identifier."""
        return str(self.email)
        
    def rmv_submit_msg(self):
        del self.submit
        del self.message
    
    def rmv_submit(self):
        del self.submit
