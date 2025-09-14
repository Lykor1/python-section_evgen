from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Order:
    total: float
    is_loyal: bool = False

    def apply_discount(self, discounts: List[BaseDiscount]) -> float:
        final_total = self.total
        for discount in discounts:
            final_total = discount.apply(final_total, self)
        return final_total


class BaseDiscount:
    def apply(self, current_total: float, order: Order) -> float:
        raise NotImplementedError


class FixedDiscount(BaseDiscount):
    def __init__(self, amount: float):
        self.amount = amount

    def apply(self, current_total: float, order: Order) -> float:
        return max(0, current_total - self.amount)


class PersentDiscount(BaseDiscount):
    def __init__(self, percent: float):
        self.percent = percent

    def apply(self, current_total: float, order: Order) -> float:
        discount_amount = current_total * (self.percent / 100)
        return max(0, current_total - discount_amount)


class LoyaltyDiscount(BaseDiscount):
    def apply(self, current_total: float, order: Order) -> float:
        if order.is_loyal:
            discount_amount = current_total * 0.1
            return max(0, current_total - discount_amount)
        return current_total


class DiscountFactory:
    @staticmethod
    def get_discounts(order: Order) -> List[BaseDiscount]:
        discounts: List[BaseDiscount] = []
        discounts.append(PersentDiscount(10))
        if order.is_loyal:
            discounts.append(LoyaltyDiscount())
        if order.total > 1000:
            discounts.append(FixedDiscount(100))
        return discounts


if __name__ == '__main__':
    order_1 = Order(total=500, is_loyal=True)
    order_2 = Order(total=1500, is_loyal=False)

    discounts_1 = DiscountFactory.get_discounts(order_1)
    discounts_2 = DiscountFactory.get_discounts(order_2)

    final_price = order_1.apply_discount(discounts_1)
    print(f'Сумма: {order_1.total}\nКоличество скидок: {len(discounts_1)}\nИтоговая цена: {final_price}\n')

    final_price = order_2.apply_discount(discounts_2)
    print(f'Сумма: {order_2.total}\nКоличество скидок: {len(discounts_2)}\nИтоговая цена: {final_price}')
