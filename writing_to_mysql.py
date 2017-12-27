import MySQLdb

conn = MySQLdb.connect(host=    "localhost",
                       user=    "nicho",
                       passwd=  "Spot1000",
                       db=      "stock_basket",)

c = conn.cursor()

c.execute('''DESCRIBE ticks;''')

results = c.fetchall()

for line in results:
    print(line)