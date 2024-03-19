from werkzeug.exceptions import BadRequest
from flask_openapi3 import APIBlueprint, Tag
from flask import request, jsonify

from service.order_service import BadPaymentError, apply_discount, load_discount_points
from model.order import Order, OrderBody, OrderResponse, OrderResult
from model.errors import BadRequestMalformedBodyOrderError, PaymentRequiredError
from model.user import User

from db.init_db import orders, users

order_blueprint = APIBlueprint("orders", __name__)

order_tag = Tag(name="Order")


@order_blueprint.errorhandler(BadRequest)
def handle_bad_request(e):
    error = BadRequestMalformedBodyOrderError()
    return jsonify(error.model_dump()), BadRequest.code


@order_blueprint.errorhandler(BadPaymentError)
def handle_not_enough_money(e):
    error = PaymentRequiredError()
    return jsonify(error.model_dump()), BadPaymentError.code


@order_blueprint.post(
    rule="/order",
    tags=[order_tag],
    responses={
        200: OrderResponse,
        400: BadRequestMalformedBodyOrderError,
        402: PaymentRequiredError
    }
)
def make_order(body: OrderBody):
    '''
    Receives the order and store the informations in the database and updating the quantities bought
    '''
    body: dict = request.get_json()
    credit_card: dict = body.get("payment_info")
    user_email: str = body.get("email")
    products: list = body.get("products")
    payment: int = body.get("total")
    order = Order(
        products=products,
        user_email=user_email,
        total=payment,
        payment_info=credit_card
    )
    '''
    request to external service to make payment
    if the customer have not enough money:
        abort(402)
    '''
    user_item = users.find_one(filter={"email": user_email}, hint="email_text")
    user = User(**user_item)
    apply_discount(user, order)
    load_discount_points(order, user, products)
    orders.insert_one(order.model_dump())
    users.update_one(filter={"email": user.email},
                     update={"$set": {"discount_points": user.discount_points}},
                     hint="email_text")
    return jsonify(OrderResponse(total=order.total,
                                 outcome=OrderResult.success,
                                 discount_points_earned=order.discount_points_earned).model_dump())
