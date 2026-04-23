#libraries
from pywebio.input import input, PASSWORD, input_group, select, NUMBER
from pywebio.output import put_text, put_markdown, put_button, clear, put_image
from models import Payee, User

#creates a list to store users
users = []

def show_account(user):
    clear()
    #title for the page
    put_markdown("# 🏦 Banking App")

    #displays all the information for the current account
    put_markdown("Account 1")
    put_markdown(f"Balance: £{user.accounts['current']['balance']}")
    put_markdown(f"Account Number: {user.accounts['current']['account_number']} sort_code: {user.accounts['current']['sort_code']}")

    #displays all the information for the savings account
    put_markdown("Account 2")
    put_markdown(f"Balance: £{user.accounts['savings']['balance']}")
    put_markdown(f"Account Number: {user.accounts['savings']['account_number']} sort_code: {user.accounts['savings']['sort_code']}")

    #creates 3 buttons 
    put_button("Home", onclick=lambda: show_account(user))
    put_button("Payments", onclick=lambda: show_payment(user))
    put_button("Product", onclick=lambda: show_products(user))

def show_payment(user):
    clear()

    #page title
    put_markdown("Payment Page")

    #goes through the payees list and displays all the payees
    for payee in user.payees:
        put_text(f"Name: {payee.name} Account Number: {payee.account_num} Sort Code: {payee.sort_code} Bank: {payee.bank}")

    #creates 2 buttons 
    put_button("Add new payee", onclick=lambda: show_newpayee(user))
    put_button("Cancel", onclick=lambda: show_account(user))

def show_newpayee(user):
    clear()
    #page title
    put_markdown("New Payee Page")

    #stores all the inputs under a single variable
    data = input_group("New Payee Details", [

            input("Payee Name", name="name"),
            input("Bank", name="bank"),
            input("Account Number", name="account_num"),
            input("Sort Code", name="sort_code")
    ])

    #calls the add_payee function in models and gives a message
    message = user.add_payee(

        account_num = data["account_num"],
        sort_code = data["sort_code"],
        name = data["name"],
        bank = data["bank"]
    )

    #print the message and create a home button
    put_markdown(message)
    put_button("Home", onclick=lambda: show_account(user))

def show_send_money(user):
    clear()
    #page title
    put_markdown("Send Money")

    #goes through the payess list and retrieves all their names
    payee_options = [payee.name for payee in user.payees]

    #stores all the inputs and creates a select with payee_options
    data = input_group("send Money", [
        select("Select Payee", options=payee_options, name="payee"),
        input("Amount", name="amount", type=NUMBER)
    ])

    #money_payee stores which payee they selected
    money_payee = data["payee"]
    #money converts the string amount into a float and stores it
    money = float(data["amount"])

    #calls the send_money function with the money and money_payee varaibles 
    message = user.send_money(money, money_payee)
    put_markdown(message)
    put_button("Return", onclick=lambda: show_account(user))

def show_move_money(user):
    clear()
    #title page
    put_markdown("Move Money")

    #stores all the inputs, creates 2 select options
    data = input_group("Move Money", [
        select("From Account", options=["current", "savings"], name="from_account"),
        select("To Account", options=["current", "savings"], name="to_account"),
        input("Amount", name="amount", type=NUMBER)
    ])

    #retrieves the accounts information and converts the amount to a float
    from_account = user.accounts[data["from_account"]]
    to_account = user.accounts[data["to_account"]]
    amount = float(data["amount"])

    #calls the move_money function
    message = user.move_money(amount, from_account, to_account)
    put_markdown(message)

    #creates a next button
    put_button("Next", onclick=lambda: show_account(user))

def show_products(user):
    clear()
    #page title
    put_markdown("Products")

    #allows the user to click and get more details about loans
    put_markdown("Loans")
    put_markdown("Click below to look at loan options")
    put_button("Loan", onclick=lambda: show_loan(user))

    #allows the user to click and get information about mortgages
    put_markdown("Mortgages")
    put_markdown("Click below to look at mortgages options")
    put_button("Mortgages", onclick=lambda: show_mortgages(user))

    #allows the user to click and get information about credit cards
    put_markdown("Credit Cards")
    put_markdown("Click below to look at credit card options")
    put_button("Credit Card", onclick=lambda: show_credit(user))

    #creates a home button to return
    put_button("Home", onclick=lambda: show_account(user))

def show_loan(user):
    clear()

    #page title
    put_markdown("Loans")

    #adds an image and displays loan information
    put_image("https://www.picpedia.org/chalkboard/images/loan.jpg")
    put_markdown("Loan Options:")

    put_markdown("Personal Loans:")
    put_markdown("Borrow between £1,000 - £25,000.")

    put_markdown("Student Loans:")
    put_markdown("We have flexible repayment options.")

    #creates a button to return back to the product page
    put_button("Back", onclick=lambda: show_products(user))

def show_mortgages(user):
    clear()
    #page title
    put_markdown("Mortgages")

    put_markdown("Coming Soon")

    # creates a button to return back to the product page
    put_button("Back", onclick=lambda: show_products(user))

def show_credit(user):
    clear()
    #page title
    put_markdown("Credit Cards")

    put_markdown("Coming Soon")

    #creates a button to return back to the products page
    put_button("Back", onclick=lambda: show_products(user))

def login():
    clear()
    #creates two buttons that allows the user to either register or change password
    put_button("Register", onclick=lambda: show_register())
    put_button("Forgot Password", onclick=lambda: show_fpassword())

    #creates an attempts variable
    attempts = 0

    #while the attempts varaible is less than 3 conintue
    while attempts < 3:

        #creates two inputs so the user can put their username and password
        username = input("username")
        password = input("password", type=PASSWORD)

        #goes through the users list
        for user in users:
            #if the user is in the list continue
            if user.username == username and user.password == password:
                put_markdown("Login Success")
                #takes them to their accounts page
                show_account(user)
                return user
        
        #if user is not in users list attempt + 1
        attempts += 1
        put_markdown(f"Wrong Credentials {3 - attempts} left")
    put_markdown("Account Locked!")

def show_fpassword():
    clear()
    put_markdown("Username")
    
    #asks for user name
    name = input("Name")

    #checks if they have a valid input
    if name == "":
        put_markdown("Invalid name")
    else:
        #goes through the users list
        for user in users:
            #if name is found continue
            if name == user.username:
                
                #stores the inputs under one varaible
                data = input_group("New Password", [
                    #asks for new password
                    input("New Password", name="new_password"),
                    #asks to confirm new password
                    input("Confirm Password", name="confirm_password")
                ])

                #checks if the new password and confirm password variables are valid
                if data["new_password"] == "":
                    put_markdown("Invalid password")
                elif data["confirm_password"] == "":
                    put_markdown("Invalid")
                elif data["new_password"] != data["confirm_password"]:
                    put_markdown("Passwords don't match")
                else:
                    #retrives their old password and replaces it with new password
                    user.password = data["new_password"]
                    put_markdown("Password Updated Successfully")
                    #creates a next button
                    put_button("Next", onclick=lambda: login())
                    return
                
        put_markdown("Invalid Username")
        return
            
def show_register():
    clear()
    #page title
    put_markdown("Register")

    #stores inputs under one varaible
    data = input_group("Register User", [
        input("Name", name="name"),
        input("Password", name="password", type=PASSWORD),
        input("Confirm Password", name="confirm_password")
    ])

    #checks if all inputs are valid
    if data["name"] == "":
        put_markdown("Enter valid name")
    elif data["password"] == "":
        put_markdown("Enter valid password")
    elif data["password"] != data["confirm_password"]:
        put_markdown("Passwords don't match")
    else:
        #goes through users list
        for user in users:
            #if the name already exisits it stops
            if data["name"] == user.username:
                put_markdown("Username already exists")
                return
    
        #creates a new user object
        new_user = User(data["name"], data["password"])
        #appends the new user to the users list
        users.append(new_user)
    
        #creates a continue button
        put_button("Continue", onclick=lambda: login())