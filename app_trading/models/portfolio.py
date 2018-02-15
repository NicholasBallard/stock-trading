from connection import Connection

class Portfolio(Connection):

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "I'm saying something"
