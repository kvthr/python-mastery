import csv
from validate import PositiveInteger, PositiveFloat, String

class Stock():
    _types = (str, int, float)

    name   = String()
    shares = PositiveInteger()
    price  = PositiveFloat()

    def __init__(self, name, shares, price) -> None:
        self.name = name
        self.shares = shares
        self.price = price

    def __setattr__(self, name, value):
        if name not in { 'name', 'shares', 'price', '_name', '_shares', '_price'}:
            raise AttributeError('No attribute %s' % name)
        super().__setattr__(name, value)

    @classmethod
    def from_row(cls, row):
        values = [func(val) for func, val in zip(cls._types, row)]
        return cls(*values)

    @property
    def shares(self):
        return self._shares

    @shares.setter
    def shares(self, value):
        self._shares = PositiveInteger.check(value)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, self._types[2]):
            raise TypeError(f"Expected {self._types[2].__name__} for share price")

        if value < 0:
            raise ValueError("Share price must be positive")
        
        self._price = value

    @property
    def cost(self):
        return self.shares * self.price

    def sell(self, num):
        self.shares -= num

    def __repr__(self):
        return f"Stock('{self.name}', {self.shares}, {self.price})"

    def __eq__(self, other):
        return isinstance(other, Stock) and (self.name, self.shares, self.price) == (other.name, other.shares, other.price)


def print_portfolio(portfolio):

    print('%10s %10s %10s' % ('name', 'shares', 'price'))
    print(('-'*10 + ' ')*3)
    for s in portfolio:
        print('%10s %10d %10.2f' % (s.name, s.shares, s.price))

if __name__ == '__main__':
    portfolio = read_portfolio('Data/portfolio.csv')
    print_portfolio(portfolio)