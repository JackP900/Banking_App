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

        self.payees = []
        self.transactions = []

    def add_payee(self, account_num, sort_code, name, bank):
        if account_num == "":
            return("Account number invalid")
        elif sort_code == "":
            return("sort code invalid")
        elif name == "":
            return("Name is invalid")
        elif bank == "":
            return("bank is invalid")
        else:
            new_payee = Payee(sort_code, account_num, name, bank)
            self.payees.append(new_payee)
            return("Success")

    def send_money(self, amount, payee):
        if amount <= 0:
            return("Invalid amount")
        elif self.accounts["current"]["balance"] < amount:
            return("Insufficient funds")
        else:
            self.accounts["current"]["balance"] -= amount

            transaction = {
                "amount": amount,
                "payee": payee,
                "type": "payment",
                "date": datetime.now()
            }

            self.transactions.append(transaction)

            return("Success")

    def move_money(self, amount, from_account, to_account):
        if amount <= 0:
            return("invalid amount")
        else:
            if from_account == self.accounts["current"]:

                if self.accounts["current"]["balance"] < amount:
                    return("Insufficient funds")

                else:

                    self.accounts["current"]["balance"] -= amount
                    self.accounts["savings"]["balance"] += amount

                    transaction = {
                        "from_account": self.accounts["current"],
                        "to_account": self.accounts["savings"],
                        "amount": amount,
                        "type": "transfer",
                        "date": datetime.now()
                        }
                    
                    self.transactions.append(transaction)

                    return("Success")

            elif from_account == self.accounts["savings"]:

                if self.accounts["savings"]["balance"] < amount:
                    return("Insufficient fund")

                else:
                    self.accounts["savings"]["balance"] -= amount
                    self.accounts["current"]["balance"] += amount

                    transaction = {
                        "from_account": self.accounts["savings"],
                        "to_account": self.accounts["current"],
                        "amount": amount,
                        "type": "transfer",
                        "date": datetime.now()
                        }
                    
                    self.transactions.append(transaction)

                    return("Success")