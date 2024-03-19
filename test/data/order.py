order_body_input_correct = {
    "total": 10.21,
    "email": "ginoverdi@gmail.com",
    "payment_info": {
        "json": "dati"
    },
    "products": [

    ]
}

order_body_input_wrong = {
    "total": 10.21,
    "email": "prova@prova.com",
    "products": [

    ]
}

order_output_success = {'outcome': 'The order was successfully made', 'total': 10.21, 'discount_points_earned': 0}
order_output_failed = {'error_code': 400, 'description': 'The body sent has missing informations or bad formatting'}

order_input_no_discount_points = {
    "total": 123.21,
    "email": "ginoverdi@gmail.com",
    "payment_info": {
        "json": "dati"
    },
    "products": []
}

order_output_success_no_discount_points = {'outcome': 'The order was successfully made',
                                           'total': 123.21,
                                           'discount_points_earned': 0}

order_input_with_discount_points = {
    "total": 123.21,
    "email": "mariorossi@gmail.com",
    "payment_info": {
        "json": "dati"
    },
    "products": []
}
# discount of 3 euros applied
order_output_success_with_discount_points = {'outcome': 'The order was successfully made',
                                             'total': 119.21,
                                             'discount_points_earned': 0}

order_input_with_multiplier = {
    "total": 123.54,
    "payment_info": {
        "json": "dati"
    },
    "email": "lucaazzurri@gmail.com",
    "products": [
        {
            "id": "2",
            "category": "verdura",
            "name": "melanzana",
            "price": 2.5,
            "quantity": 2,
            "discount_multiplier": 1
        },
        {
            "id": "5",
            "category": "pesce",
            "name": "spada",
            "price": 25.7,
            "quantity": 2,
            "discount_multiplier": 3
        }
    ]
}

order_output_success_with_multiplier = {'outcome': 'The order was successfully made',
                                        'total': 123.54,
                                        "discount_points_earned": 77}

order_input_with_discount_on_products = {
    "total": 123.54,
    "payment_info": {
        "json": "dati"
    },
    "email": "francogialli@gmail.com",
    "products": [
        {
            "id": "2",
            "category": "verdura",
            "name": "broccoli",
            "price": 2.5,
            "quantity": 22,
            "discount_multiplier": 1
        },
        {
            "id": "1",
            "category": "carne",
            "name": "salsiccia di suino",
            "price": 25.7,
            "quantity": 15,
            "discount_multiplier": 3
        }
    ]
}

order_output_with_discount_on_products = {
    "discount_points_earned": 77,
    "outcome": "The order was successfully made",
    "total": 120.97
}
