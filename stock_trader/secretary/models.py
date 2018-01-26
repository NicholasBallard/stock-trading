import sys
import os

ROOTDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(ROOTDIR)

from connector.connection import Connection

# prepare daily summary report.

class Secretary(Connection):

    def __init__(self, name):
        super().__init__()
        self.name = name
    
    def __str__(self):
        return "Hiya! I'm a big busty blonde!"

    def summarize_day(self):
        # values: all, today, current_week, current_month, last_month
        transactions = Secretary.history(self, "today").findAll('transaction')
        return transactions

sec = Secretary("Ms. Huge Tits")
transactions = sec.summarize_day()

commission = 0

for i in transactions:
    i = i.find("commission").text
    i = float(i)
    commission += i

print(commission)