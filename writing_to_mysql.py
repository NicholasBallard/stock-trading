import numpy as np
import MySQLdb
import datetime

conn = MySQLdb.connect(host=    "localhost",
                       user=    "nicho",
                       passwd=  "Spot1000",
                       db=      "stock_basket",)

c = conn.cursor()

# np.zeros(())

sql = '''INSERT INTO ticks (ts, sym, price, bidsz, bidtick, bid, bid_time) VALUES (%s, %s, %s, %s, %s, %s, %s)'''

# params = [(str(keywords[i], date, time, position[i]) for i in range(len(stock_basket.stock_basket.split(' '))))]

params = [
    (str(datetime.datetime.utcnow()), 'KR', '15.14', '1000', 'd', '15.13', str(datetime.datetime.utcnow())),
    (str(datetime.datetime.utcnow()), 'AAPL', '732.10', '20', 'u', '732.50', str(datetime.datetime.utcnow())),
    (str(datetime.datetime.utcnow()), 'MSFT', '71.00', '159', 'u', '71.10', str(datetime.datetime.utcnow())),
]

c.executemany(sql, params)

conn.commit()

c.execute('''DESCRIBE ticks;''')

c.execute('''SELECT * FROM ticks;''')

results = c.fetchall()

for line in results:
    print(line)