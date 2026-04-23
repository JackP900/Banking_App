#libraries
from pywebio import start_server
from ui import login, users
from models import User

#creates a test user to check everything is working
test_user = User("admin", "password")
users.append(test_user)

#creates a server and calls login function first
start_server(login, port=8080, debug=True)