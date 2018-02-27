from connection import Connection


class Portfolio(Connection):

    def __init__(self):
        self.portfolio = dict()
        super().__init__()

    def __str__(self):
        return "I'm a portfolio. You are a portfolio. We are a portfolio together."


    # TODO: position

    # TODO: basis

    # TODO: transaction costs

    # TODO: protection plan (sell/cover)

    # TODO: time to planned divestiture
