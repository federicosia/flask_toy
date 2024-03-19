import os

from flask import abort
from flask_openapi3 import OpenAPI
from flask_openapi3 import Info

from route.product_route import product_blueprint
from route.order_route import order_blueprint

address = os.getenv("IP_ADDRESS_FLASK", "localhost")

info = Info(title="Cart Market API", version="1.0.0")
app = OpenAPI(__name__, info=info, validation_error_callback=lambda e: abort(400))

app.register_api(product_blueprint)
app.register_api(order_blueprint)

if __name__ == "__main__":
    app.run(host=address, port=5000, debug=False)
