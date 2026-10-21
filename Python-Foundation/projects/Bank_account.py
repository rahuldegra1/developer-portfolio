class Account:
    def __init__(self, acc_no, acc_bal, acc_name):
        self.acc_name = acc_name
        self.acc_bal = acc_bal
        self.acc_no = acc_no
        self.acc_transaction = []

    def deposit(self, amount):
        if amount > 0:
            self.acc_bal += amount
            print(f"deposited {amount} . New Balance {self.acc_bal}")
            self.acc_transaction.append(("deposit", amount))

    def withdraw(self, amount):
        if amount > 0 and amount <= self.acc_bal:
            self.acc_bal -= amount
            print(f"withdrew {amount} . New Balance {self.acc_bal}")
            self.acc_transaction.append(("withraw", amount))
        else:
            print("Insufficient funds or invalid amount.")

    def get_balance(self):
        return self.acc_bal

    def History(self):
        return self.acc_transaction


class SavingAccount(Account):
    def __init__(self, acc_no, acc_bal, acc_name, interest_rate):
        super().__init__(acc_no, acc_bal, acc_name)
        self.interest_rate = interest_rate

    def add_interest(self):
        interest = self.acc_bal * self.interest_rate / 100
        self.acc_bal += interest
        print(f"New Balance {self.acc_bal}")


acc1 = Account(12321, 10000, "stark")
acc1.deposit(int(input("Enter amount You want to deposit: ")))
acc1.withdraw(int(input("Enter amount You want to withdraw: ")))
print(acc1.get_balance())
print(acc1.History())
sav1 = SavingAccount(12321, 10000, "stark", 5)
print(sav1.acc_bal)
sav1.add_interest()
print(sav1.acc_bal)
