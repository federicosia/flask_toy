from datetime import datetime

from werkzeug.exceptions import HTTPException

from model.order import Order
from model.user import User

from db.init_db import discounts


class BadPaymentError(HTTPException):
    code = 402
    description = 'Credit card does not have sufficient funds to make the order'


def apply_discount(user_item: User, order_item: Order):
    product: dict
    id_products = [product.get("id") for product in order_item.products]

    discount_in_euros = int(user_item.discount_points / 25)
    order_item.discount_applied += discount_in_euros

    item_with_discount: dict
    for item_with_discount in discounts.find({"product_id": {"$in": id_products}}, hint="product_identifier"):
        date_until = datetime.strptime(item_with_discount.get("until"), "%Y-%m-%d")
        for product_item in order_item.products:
            if item_with_discount.get("product_id") == product_item.get("id") and date_until > datetime.today():
                percentage_discount = item_with_discount.get("percentage_discount")
                euros_to_remove_from_total = (product_item.get("price") * percentage_discount) / 100
                order_item.total = round(order_item.total - euros_to_remove_from_total, 2)
                break

    order_item.total -= discount_in_euros
    user_item.discount_points = int(user_item.discount_points - (discount_in_euros * 25))


def load_discount_points(order_item: Order, user_item: User, products: list):
    discount_points: int = 0
    product: dict
    for product in products:
        discount_points += int(product.get("price")) * product.get("discount_multiplier")
    user_item.discount_points += discount_points
    order_item.discount_points_earned = discount_points
