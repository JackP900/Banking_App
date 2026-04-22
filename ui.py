from pywebio.input import input, PASSWORD, input_group, select, NUMBER
from pywebio.output import put_text, put_markdown, put_button, clear, put_image
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

def show_send_money(user):
    clear()
    put_markdown("Send Money")

    payee_options = [payee.name for payee in user.payees]

    data = input_group("send Money", [
        select("Select Payee", options=payee_options, name="payee"),
        input("Amount", name="amount", type=NUMBER)
    ])

    money_payee = data["payee"]
    money = float(data["amount"])

    message = user.send_money(money, money_payee)
    put_markdown(message)
    put_button("Return", onclick=lambda: show_account(user))

def show_products(user):
    clear()
    put_markdown("Products")

    put_markdown("Loans")
    put_markdown("Click below to look at loan options")
    put_button("Loan", onclick=lambda: show_loan(user))

    put_markdown("Mortgages")
    put_markdown("Click below to look at mortgages options")
    put_button("Mortgages", onclick=lambda: show_mortgages(user))

    put_markdown("Credit Cards")
    put_markdown("Click below to look at credit card options")
    put_button("Credit Card", onclick=lambda: show_credit(user))

    put_button("Home", onclick=lambda: show_account(user))

def show_loan(user):
    clear()
    put_markdown("Loans")
    put_image("https://www.picpedia.org/chalkboard/images/loan.jpg")
    put_markdown("Loan Options:")

    put_markdown("Personal Loans:")
    put_markdown("Borrow between £1,000 - £25,000.")

    put_markdown("Student Loans:")
    put_markdown("We have flexible repayment options.")

    put_button("Back", onclick=lambda: show_products(user))

def show_mortgages(user):
    clear()
    put_markdown("Mortgages")
    put_markdown("Coming Soon")

    put_button("Back", onclick=lambda: show_products(user))

def show_credit(user):
    clear()
    put_markdown("Credit Cards")
    put_markdown("Coming Soon")

    put_button("Back", onclick=lambda: show_products(user))

def login():
    put_button("Register", onclick=lambda: show_register())
    put_button("Forgot Password", onclick=lambda: show_fpassword())

    attempts = 0

    while attempts < 3:

        username = input("username")
        password = input("password", type=PASSWORD)

        for user in users:
            if user.username == username and user.password == password:
                put_markdown("Login Success")
                show_account(user)
                return user
        
        attempts += 1
        put_markdown(f"Wrong Credentials {3 - attempts} left")
    put_markdown("Account Locked!")


def show_fpassword():
    clear()
    put_markdown("Username")
    
    name = input("Name")

    if name == "":
        put_markdown("Invalid name")
    else:
        for user in users:
            if name == user.username:
                
                data = input_group("New Password", [
                    input("New Password", name="new_password"),
                    input("Confirm Password", name="confirm_password")
                ])

                if data["new_password"] == "":
                    put_markdown("Invalid password")
                elif data["confirm_password"] == "":
                    put_markdown("Invalid")
                elif data["new_password"] != data["confirm_password"]:
                    put_markdown("Passwords don't match")
                else:
                    user.password = data["new_password"]
                    put_markdown("Password Updated Successfully")
                    put_button("Next", onclick=lambda: login())
                    return
                
        put_markdown("Invalid Username")
        return
            





def show_register():
    clear()
    put_markdown("Register")

    data = input_group("Register User", [
        input("Name", name="name"),
        input("Password", name="password", type=PASSWORD),
        input("Confirm Password", name="confirm_password")
    ])

    if data["name"] == "":
        put_markdown("Enter valid name")
    elif data["password"] == "":
        put_markdown("Enter valid password")
    elif data["password"] != data["confirm_password"]:
        put_markdown("Passwords don't match")
    else:
        for user in users:
            if data["name"] == user.username:
                put_markdown("Username already exists")
                return
    
        new_user = User(data["name"], data["password"])
        users.append(new_user)
    
        put_button("Continue", onclick=lambda: login())