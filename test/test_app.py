import json

import pytest
import mongomock
from pydantic import ValidationError

import app as source_app
from data.product import get_products_input, get_products_output
from data.categories import get_categories_output, get_by_category_output
from data.search import search_output
from data.order import (order_body_input_correct, order_body_input_wrong, order_output_success,
                        order_input_with_discount_points, order_output_success_with_discount_points,
                        order_input_no_discount_points, order_output_success_no_discount_points,
                        order_input_with_multiplier, order_output_success_with_multiplier,
                        order_input_with_discount_on_products, order_output_with_discount_on_products)
from data.user import (user_order_after_discount_points, user_order_before_discount_points,
                       user_order_no_discount_points, user_order_with_multiplier, user_order_with_product_discounts)


@pytest.fixture
def fake_mongo_client():
    return mongomock.MongoClient()


@pytest.fixture
def fake_db(fake_mongo_client):
    return fake_mongo_client.db


@pytest.fixture
def fake_collection(fake_db):
    collection = fake_db.collection
    collection.create_index("category")
    return fake_db.collection


@pytest.fixture
def fake_collection_insert(monkeypatch, fake_collection):
    for item in get_products_input["products"]:
        fake_collection.insert_one(item)

    monkeypatch.setattr("route.product_route.products", fake_collection)


@pytest.fixture
def fake_user_insert_no_discount(monkeypatch, fake_db):
    users = fake_db.collection["users"]
    users.insert_one(user_order_no_discount_points)
    monkeypatch.setattr("route.order_route.users", users)
    monkeypatch.setattr("route.order_route.users.find_one", lambda filter, hint: user_order_no_discount_points)
    monkeypatch.setattr("route.order_route.users.update_one", lambda filter, update, hint: None)


@pytest.fixture
def fake_user_insert_discount(monkeypatch, fake_db):
    users = fake_db.collection["users"]
    users.insert_one(user_order_before_discount_points)
    monkeypatch.setattr("route.order_route.users", users)
    monkeypatch.setattr("route.order_route.users.find_one", lambda filter, hint: user_order_before_discount_points)
    monkeypatch.setattr("route.order_route.users.update_one", lambda filter, update, hint: user_order_after_discount_points)


@pytest.fixture
def fake_user_insert_with_multiplier(monkeypatch, fake_db):
    users = fake_db.collection["users"]
    users.insert_one(user_order_with_multiplier)
    monkeypatch.setattr("route.order_route.users", users)
    monkeypatch.setattr("route.order_route.users.find_one", lambda filter, hint: user_order_with_multiplier)
    monkeypatch.setattr("route.order_route.users.update_one", lambda filter, update, hint: None)


@pytest.fixture
def fake_disable_products_discount_on_products(monkeypatch, fake_db):
    monkeypatch.setattr("service.order_service.discounts.find", lambda filter, hint: [])


@pytest.fixture
def fake_user_discount_on_products(monkeypatch, fake_db):
    users = fake_db.collection["users"]
    users.insert_one(user_order_with_product_discounts)
    monkeypatch.setattr("route.order_route.users", users)
    monkeypatch.setattr("route.order_route.users.find_one", lambda filter, hint: user_order_with_product_discounts)
    monkeypatch.setattr("route.order_route.users.update_one", lambda filter, update, hint: None)


@pytest.fixture
def fake_flask_client(monkeypatch, fake_collection_insert):
    source_app.app.config.update({"TESTING": True})

    with source_app.app.test_client() as client:
        yield client


def test_get_products(fake_flask_client):
    response = json.loads(fake_flask_client.get("/products").data)
    assert response["products"] == get_products_output["products"][:2]


def test_get_products_bad_page(fake_flask_client):
    assert (json.loads(fake_flask_client.get("/products?page=0").data)).get("error_code") == 404


def test_get_categories(fake_flask_client):
    response = json.loads(fake_flask_client.get("/categories").data)
    assert response == get_categories_output


def test_get_by_category(fake_flask_client):
    response = json.loads(fake_flask_client.get("/category?type=verdura").data)
    assert response == get_by_category_output


def test_search(fake_flask_client):
    response = json.loads(fake_flask_client.get("/search?article=mel").data)
    assert response == search_output


def test_make_order_success(monkeypatch, fake_flask_client, fake_disable_products_discount_on_products):
    monkeypatch.setattr("route.order_route.users.find_one", lambda filter, hint: user_order_no_discount_points)
    monkeypatch.setattr("route.order_route.users.update_one", lambda filter, update, hint: None)
    response = json.loads(fake_flask_client.post("/order", json=order_body_input_correct).data)
    assert response == order_output_success


def test_make_order_failed(fake_flask_client, fake_disable_products_discount_on_products):
    try:
        json.loads(fake_flask_client.post("/order", json=order_body_input_wrong).data)
    except ValidationError:
        assert True


def test_make_order_no_discount(fake_flask_client,
                                fake_user_insert_no_discount,
                                fake_disable_products_discount_on_products):
    response = json.loads(fake_flask_client.post("/order", json=order_input_no_discount_points).data)
    assert response == order_output_success_no_discount_points


def test_make_order_discount(fake_flask_client, fake_user_insert_discount, fake_disable_products_discount_on_products):
    response = json.loads(fake_flask_client.post("/order", json=order_input_with_discount_points).data)
    assert response == order_output_success_with_discount_points


def test_order_product_discount_points_multiplier(fake_flask_client,
                                                  fake_user_insert_with_multiplier,
                                                  fake_disable_products_discount_on_products):
    response = json.loads(fake_flask_client.post("/order", json=order_input_with_multiplier).data)
    assert response == order_output_success_with_multiplier


def test_order_product_with_discounts(fake_flask_client, fake_user_discount_on_products):
    response = json.loads(fake_flask_client.post("/order", json=order_input_with_discount_on_products).data)
    assert response == order_output_with_discount_on_products
