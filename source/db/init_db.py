import os

from pymongo import MongoClient
from db.init_db_service import (try_create_index, load_collections, discounts_path,
                                products_path, orders_path, users_path)

address = os.getenv("IP_ADDRESS_DB", "localhost")

client = MongoClient("mongodb://" + address + ":27017")
cart_market = client.get_database("cart_market")
products = cart_market.get_collection("products")
orders = cart_market.get_collection("orders")
users = cart_market.get_collection("users")
discounts = cart_market.get_collection("discounts")

collections_list = [products, orders, users, discounts]
product_ids = load_collections(collections_list, [products_path, orders_path, users_path, discounts_path])

indexes_map = {
    products.name: [
        {
            "key": "category",
            "name": "category_text"
        }
    ],
    orders.name: [],
    users.name: [
        {
            "key": "email",
            "name": "email_text"
        }
    ],
    discounts.name: [
        {
            "key": "product_id",
            "name": "product_identifier"
        }
    ]
}
try_create_index(collections_list, indexes_map)
