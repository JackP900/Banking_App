#libraries
from datetime import datetime

class Payee:
    def __init__(self, sort_code, account_num, name, bank):
        self.name = name
        self.sort_code = sort_code
        self.account_num = account_num
        self.bank = bank 


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        #Creating a accounts dictionary to store account details
        self.accounts = {
            "current": {
                "balance": 1500.0,
                "account_number": "123456",
                "sort_code": "1234"
            },

            "savings": {
                "balance": 4000.0,
                "account_number": "123456",
                "sort_code": "1234"
            }
        }

        #creating two lists to store payess and transactions
        self.payees = []
        self.transactions = []

    def add_payee(self, account_num, sort_code, name, bank):
        #checks all payee inputs to validate that something was entered
        if account_num == "":
            return("Account number invalid")
        elif sort_code == "":
            return("sort code invalid")
        elif name == "":
            return("Name is invalid")
        elif bank == "":
            return("bank is invalid")
        else:
            #creates a new payee object and adds it to the payees list
            new_payee = Payee(sort_code, account_num, name, bank)
            self.payees.append(new_payee)
            return("Success")

    def send_money(self, amount, payee):
        #checks if amount entered is valid and if they have enough in their current account
        if amount <= 0:
            return("Invalid amount")
        elif self.accounts["current"]["balance"] < amount:
            return("Insufficient funds")
        else:
            #removes the amount from their current balance
            self.accounts["current"]["balance"] -= amount

            #create a transaction dictionary to store details
            transaction = {
                "amount": amount,
                "payee": payee,
                "type": "payment",
                "date": datetime.now()
            }

            #appends the transaction into the transactions list
            self.transactions.append(transaction)

            return("Success")

    def move_money(self, amount, from_account, to_account):
        #checks amount entered is valid and checks if they have enough balance
        if amount <= 0:
            return("invalid amount")
        else:
            #if the from_account variable is coming from the current account continue
            if from_account == self.accounts["current"]:
                #checks the current balance 
                if self.accounts["current"]["balance"] < amount:
                    return("Insufficient funds")

                else:
                    #takes away amount entered from the current balance and adds it to the savings balance
                    self.accounts["current"]["balance"] -= amount
                    self.accounts["savings"]["balance"] += amount

                    #creates a transaction dictionary that stores the detials
                    transaction = {
                        "from_account": self.accounts["current"],
                        "to_account": self.accounts["savings"],
                        "amount": amount,
                        "type": "transfer",
                        "date": datetime.now()
                        }
                    
                    #appends the transaction to the transactions list
                    self.transactions.append(transaction)

                    return("Success")

            #if from_account variable is coming from savings account continue
            elif from_account == self.accounts["savings"]:

                #checks the savings balance
                if self.accounts["savings"]["balance"] < amount:
                    return("Insufficient fund")

                else:
                    #removes the amount from savings balance and adds it too the current balance
                    self.accounts["savings"]["balance"] -= amount
                    self.accounts["current"]["balance"] += amount

                    #creates a transaction ditionary to store the details
                    transaction = {
                        "from_account": self.accounts["savings"],
                        "to_account": self.accounts["current"],
                        "amount": amount,
                        "type": "transfer",
                        "date": datetime.now()
                        }
                    
                    #appends the transaction to the transactions list
                    self.transactions.append(transaction)

                    return("Success")