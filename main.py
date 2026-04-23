from pywebio import start_server
from ui import login, users
from models import User

test_user = User("admin", "password")
users.append(test_user)

start_server(login, port=8080, debug=True)