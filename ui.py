from pywebio.input import input, PASSWORD, input_group
from pywebio.output import put_text, put_markdown, put_button, clear
from models import Payee, User


users = []

test_user = User(username="admin", password="password")
users.append(test_user)



def show_account(user):
    put_markdown("# 🏦 Banking App")

    put_markdown("Account 1")
    put_markdown(f"Balance: £{user.accounts['current']['balance']}")
    put_markdown(f"Account Number: {user.accounts['current']['account_number']} sort_code: {user.accounts['current']['sort_code']}")

    put_markdown("Account 2")
    put_markdown(f"Balance: £{user.accounts['savings']['balance']}")
    put_markdown(f"Account Number: {user.accounts['savings']['account_number']} sort_code: {user.accounts['savings']['sort_code']}")

    put_button("Home", onclick=lambda: show_account(user))
    put_button("Payments", onclick=lambda: show_payment(user))
    put_button("Product", onclick=lambda: show_product(user))

def show_payment(user):
    clear()

    put_markdown("Payment Page")

    for payee in user.payees:
        put_text(f"Name: {payee.name} Account Number: {payee.account_num} Sort Code: {payee.sort_code} Bank: {payee.bank}")

    put_button("Add new payee", onclick=lambda: show_newpayee(user))
    put_button("Cancel", onclick=lambda: show_account(user))

def show_newpayee(user):
    clear()
    message = user.add_payee()
    put_markdown("New Payee Pagw")

    data = input_group("New Payee Details", [

            input("Payee Name", name="name"),
            input("Bank", name="bank"),
            input("Account Number", name="account_num"),
            input("Sort Code", name="sort_code")
    ])

    user.add_payee(

        account_num = data["account_num"],
        sort_code = data["sort_code"],
        name = data["name"],
        bank = data["bank"]
    )

    put_markdown(message)

def show_products(user):
    clear()
    put_markdown("Product Page")

    put_markdown("Loans")
    put_markdown("Click below to look at loan options")
    put_button("Loan", onclick=lambda: show_loan())

    put_markdown("Mortgages")
    put_markdown("Click below to look at mortgages options")
    put_button("Mortgages", onclick=lambda: show_mortgages())

    put_markdown("Credit Cards")
    put_markdown("Click below to look at credit card options")
    put_button("Credit Card", onclick=lambda: show_credit())

    put_button("Home", onclick=lambda: show_account(user))

def login():
    username = input("username")
    password = input("password", type=PASSWORD)

    for user in users:
        if user.username == username and user.password == password:
            put_text("login successful")
            return user
    
    put_text("Wrong Credentials")
            

