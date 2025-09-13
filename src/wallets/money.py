from dataclasses import dataclass

from src.wallets.exceptions import NegativeValueException, NotComparisonException


@dataclass(frozen=True)
class Money:
    value: float
    currency: object

    def __post_init__(self):
        if self.value < 0:
            raise NegativeValueException('Отрицательное число!')

    def _check_currency(self, other):
        if self.currency != other.currency:
            raise NotComparisonException('Операции с разными валютами!')

    def __add__(self, other):
        self._check_currency(other)
        return Money(self.value + other.value, self.currency)

    def __sub__(self, other):
        self._check_currency(other)
        result = self.value - other.value
        if result < 0:
            raise NegativeValueException('Недостаточно средств!')
        return Money(result, self.currency)

    def __eq__(self, other):
        return isinstance(other, Money) and self.currency == other.currency and self.value == other.value

    def __repr__(self):
        return f'Money(value={self.value}, currency={self.currency})'


class Wallet:
    def __init__(self, money):
        self.currencies = {}
        self.add(money)

    def add(self, money):
        current = self.currencies.get(money.currency, Money(0, money.currency))
        self.currencies[money.currency] = current + money
        return self

    def sub(self, money):
        current = self.currencies.get(money.currency, Money(0, money.currency))
        if current.value < money.value:
            raise NegativeValueException('Недостаточно средств!')
        self.currencies[money.currency] = current - money
        if self.currencies[money.currency].value == 0:
            del self.currencies[money.currency]
        return self

    def __getitem__(self, currency):
        return self.currencies.get(currency, Money(0, currency))

    def __len__(self):
        return len(self.currencies)

    def __contains__(self, currency):
        return currency in self.currencies

    def __delitem__(self, currency):
        if currency in self.currencies:
            del self.currencies[currency]
