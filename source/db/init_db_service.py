import json
from pathlib import Path

import pymongo.collection

base_path = Path(__file__).parent
products_path = (base_path / "../db/products.json").resolve()
orders_path = (base_path / "../db/orders.json").resolve()
users_path = (base_path / "../db/users.json").resolve()
discounts_path = (base_path / "../db/discounts.json").resolve()


def load_collections(collections: list, source_paths: list):
    size_collections = len(collections)
    size_source_paths = len(source_paths)
    product_ids_inserted = []

    if size_collections != size_source_paths:
        print("Something went wrong...")
        exit(-1)

    for i in range(0, size_collections):
        collection: pymongo.collection.Collection = collections[i]
        path: Path = source_paths[i]
        if collection.estimated_document_count() == 0:
            with open(path, "r") as source:
                result = collection.insert_many(item for item in json.load(source))


def try_create_index(collections: list, indexes: dict):
    collection: pymongo.collection.Collection
    for collection in collections:
        indexes_in_collection = [index.get("name") for index in collection.list_indexes()]
        for index_to_insert in indexes[collection.name]:
            if index_to_insert["name"] not in indexes_in_collection:
                collection.create_index(keys=index_to_insert["key"], name=index_to_insert["name"])


def enrich_discounts_with_ids(discounts: pymongo.collection.Collection, product_ids: list):
    with open(discounts_path, "r") as source:
        data_to_insert = json.load(source)
        item: dict
        for index, item in enumerate(data_to_insert):
            item["product_id"] = str(product_ids[index])
        discounts.insert_many(item for item in data_to_insert)
