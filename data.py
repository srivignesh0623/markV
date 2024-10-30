from flask_mongoengine import MongoEngine # type: ignore

url = "mongodb+srv://Srivignesh:sri12345*@cluster0.2pgxwru.mongodb.net/vicky?retryWrites=true&w=majority"

mydata = MongoEngine()

# User Model
class Users(mydata.Document):
    username = mydata.StringField(required=True, unique=True)
    password = mydata.StringField(required=True)  # Hashed password
    email = mydata.StringField(required=True, unique=True)
    phone = mydata.StringField()
