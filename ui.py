from pywebio.input import input, PASSWORD
from models import Payee, User

username = input("username")
password = input("password", type=PASSWORD)

users = []

test_user = User(username="admin", password="password")
users.append(test_user)

