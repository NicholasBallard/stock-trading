from connection import Connection


class TaxMan(Connection):
    def init(self):
        super().__init__()

    def __str__(self):
        return "I'm the Tax Man! Gains... losses... I'm your man!"