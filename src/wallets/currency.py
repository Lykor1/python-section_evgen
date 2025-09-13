class Currency:
    def __init__(self, code: str):
        self.code = code

    def __eq__(self, other):
        return isinstance(other, Currency) and self.code == other.code

    def __hash__(self):
        return hash(self.code)

    def __repr__(self):
        return f'Currency({self.code})'


rub = Currency('RUB')
usd = Currency('USD')
