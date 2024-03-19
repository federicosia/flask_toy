from werkzeug.exceptions import NotFound
from bson import json_util
import json

from flask_openapi3 import APIBlueprint, Tag
from flask import request, abort, jsonify

from model.product import Product, ProductQuery, ProductResponse, SearchQuery
from model.category import CategoryQuery, CategoriesResponse
from model.errors import PageNotFoundError
from service.product_service import get_image, items_per_page, get_num_page

from db.init_db import products

product_blueprint = APIBlueprint("products", __name__)

product_tag = Tag(name="Product")
category_tag = Tag(name="Category")
search_tag = Tag(name="Search")


@product_blueprint.errorhandler(NotFound)
def handle_bad_page_request(e):
    error = PageNotFoundError()
    return jsonify(error.model_dump()), NotFound.code


@product_blueprint.get(
    rule="/products",
    tags=[product_tag],
    responses={
        200: ProductResponse,
        404: PageNotFoundError
    })
def get_products(query: ProductQuery):
    """
    Get some products by page
    """
    result = []
    num_page = request.args.get("page", 1, type=int)
    if num_page < 1:
        abort(404)
    for item in products.find(skip=get_num_page(num_page), limit=items_per_page):
        converted_image = json.loads(json_util.dumps(item["image"]))
        product = Product(
            id=str(item.get("id", "")),
            name=item.get("name", ""),
            category=item.get("category", ""),
            quantity=item.get("quantity", 0),
            price=item.get("price", 999),
            image=get_image(converted_image)
        )
        result.append(product)
    return jsonify(ProductResponse(products=result).model_dump())


@product_blueprint.get(
    rule="/categories",
    tags=[category_tag],
    responses={
        200: CategoriesResponse
    })
def get_categories():
    '''
    Get categories and number of products per category
    '''
    result = {}
    for item in products.find({}).hint("category_text"):
        converted_image = json.loads(json_util.dumps(item["image"]))
        product = Product(
            id=str(item.get("id", "")),
            name=item.get("name", ""),
            category=item.get("category", ""),
            quantity=item.get("quantity", 0),
            price=item.get("price", 999),
            image=get_image(converted_image)
        )
        if product.category in result:
            result[product.category] += 1
        else:
            result[product.category] = 1
    return jsonify(CategoriesResponse(num_products_per_categories=result).model_dump())


@product_blueprint.get(
    rule="/category",
    tags=[category_tag],
    responses={
       200: ProductResponse,
       404: PageNotFoundError
    })
def get_by_category(query: CategoryQuery):
    '''
    Get articles by category
    '''
    result = []
    num_page = request.args.get("page", 1, type=int)
    type_category = request.args.get("type", "", type=str)
    if num_page < 1:
        abort(404)
    for item in products.find({"category": type_category}, skip=get_num_page(num_page), limit=items_per_page).hint("category_text"):
        converted_image = json.loads(json_util.dumps(item["image"]))
        product = Product(
            id=str(item.get("id", "")),
            name=item.get("name", ""),
            category=item.get("category", ""),
            quantity=item.get("quantity", 0),
            price=item.get("price", 999),
            image=get_image(converted_image)
        )
        result.append(product)
    return jsonify(ProductResponse(products=result).model_dump())


@product_blueprint.get(
    rule="/search",
    tags=[search_tag],
    responses={
        200: ProductResponse,
        404: PageNotFoundError
    })
def search(query: SearchQuery):
    '''
    Search articles by name
    '''
    result = []
    num_page = request.args.get("page", 1, type=int)
    article = request.args.get("article", type=str)
    if num_page < 1:
        abort(404)
    for item in products.find({"name": {"$regex": article}}, skip=get_num_page(num_page), limit=items_per_page):
        converted_image = json.loads(json_util.dumps(item["image"]))
        product = Product(
            id=str(item.get("id", "")),
            name=item.get("name", ""),
            category=item.get("category", ""),
            quantity=item.get("quantity", 0),
            price=item.get("price", 999),
            image=get_image(converted_image)
        )
        result.append(product)
    return jsonify(ProductResponse(products=result).model_dump())