import numpy as np
import MySQLdb
from import datetime as dt

conn = MySQLdb.connect(host=    "localhost",
                       user=    "nicho",
                       passwd=  "Spot1000",
                       db=      "stock_basket",)

c = conn.cursor()

# np.zeros(())

sql = '''INSERT INTO ticks (ts, sym, price, bidsz, bidtick, bid, bid_time) VALUES (%s, %s, %s, %s, %s, %s, %s)'''

# params = [(str(keywords[i], date, time, position[i]) for i in range(len(stock_basket.stock_basket.split(' '))))]

params = [
    (str(dt.utcnow()), 'KR', '15.14', '1000', 'd', '15.13', str(dt.utcnow())),
    (str(dt.utcnow()), 'AAPL', '732.10', '20', 'u', '732.50', str(dt.utcnow())),
    (str(dt.utcnow()), 'MSFT', '71.00', '159', 'u', '71.10', str(dt.utcnow())),
]

c.executemany(sql, params)

conn.commit()

c.execute('''SELECT * FROM ticks;''')

results = c.fetchall()

for line in results:
    print(line)