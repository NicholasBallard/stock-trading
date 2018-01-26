import os
date = "2018-01-25"
x = os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ticker"), "ticks"), date + " ticker.csv")

print(x)