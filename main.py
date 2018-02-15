import os
import sys
import time

sys.path.append(os.path.join(os.path.split(__file__)[0], "models"))

from models.portfolio import Portfolio


def Main():

    # t = Ticker()

    # t.run()
    # time.sleep(1)

    p = Portfolio()
    return print(p)


if __name__ == '__main__':
    Main()
