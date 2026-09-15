import csv
from datetime import datetime
import pandas as pd
import os

class BankAccount:
    def __init__(self, account_number, account_holder, initial_balance=0.0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = initial_balance
        self.transactions = []
        
        if initial_balance > 0:
            self._record_transaction("Deposit", initial_balance)

    def _record_transaction(self, trans_type, amount):
        """Internal method to log a transaction."""
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transactions.append({
            "Date": date_str,
            "Account_Number": self.account_number,
            "Type": trans_type,
            "Amount": amount,
            "Balance_After": self.balance
        })

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self._record_transaction("Deposit", amount)
            print(f"[{self.account_holder}] Deposited ${amount:.2f}. New balance: ${self.balance:.2f}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self._record_transaction("Withdrawal", amount)
            print(f"[{self.account_holder}] Withdrew ${amount:.2f}. New balance: ${self.balance:.2f}")
        else:
            print(f"[{self.account_holder}] Failed to withdraw ${amount:.2f}: Insufficient funds or invalid amount.")

    def export_history_to_csv(self, filename="transactions.csv"):
        """Exports the transaction history to a CSV file for analysis."""
        keys = ["Date", "Account_Number", "Type", "Amount", "Balance_After"]
        
        file_exists = os.path.isfile(filename)
        
        with open(filename, 'a' if file_exists else 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            if not file_exists:
                dict_writer.writeheader()
            dict_writer.writerows(self.transactions)
        
        print(f"\nTransaction history saved to {filename} ")
        self.transactions = [] # Clear memory after export

class BankAnalyzer:
    def __init__(self, csv_filepath):
        self.filepath = csv_filepath
        try:
            self.df = pd.read_csv(csv_filepath)
        except FileNotFoundError:
            print(f"Error: The file {csv_filepath} does not exist.")
            self.df = None

    def generate_report(self):
        if self.df is None or self.df.empty:
            print("No data available to analyze.")
            return


        print(" TRANSACTION DATA ANALYSIS REPORT ")

        print("\n Most Recent Transactions:")
        print(self.df.tail())

        print("\n Totals by Transaction Type:")
        totals = self.df.groupby('Type')['Amount'].sum()
        print(totals.to_string())

        print("\n Average Transaction Size:")
        averages = self.df.groupby('Type')['Amount'].mean()
        print(averages.to_string())

        print("\n Largest Single Transaction:")
        max_idx = self.df['Amount'].idxmax()
        largest_trans = self.df.iloc[max_idx]
        print(f"Type:   {largest_trans['Type']}")
        print(f"Amount: ${largest_trans['Amount']:.2f}")
        print(f"Date:   {largest_trans['Date']}")
  


if __name__ == "__main__":
    csv_file = "bank_dataset.csv"
    
    if os.path.exists(csv_file):
        os.remove(csv_file)

    print("Bank Activity ")
    
    account = BankAccount(account_number="CHK-12345", account_holder="Jane Doe", initial_balance=500.0)
    
    account.deposit(1200.50)
    account.withdraw(200.00)
    account.withdraw(50.25)
    account.deposit(300.00)
    account.withdraw(2000.00) 
    account.withdraw(150.00)

    account.export_history_to_csv(csv_file)

    analyzer = BankAnalyzer(csv_file)
    analyzer.generate_report()