from pywebio.input import input, PASSWORD
from pywebio.output import put_text
from models import Payee, User

users = []

test_user = User(username="admin", password="password")
users.append(test_user)

def login():
    username = input("username")
    password = input("password", type=PASSWORD)

    for user in users:
        if user.username == username and user.password == password:
            put_text("login successful")
            return user
    
    put_text("Wrong Credentials")
            

