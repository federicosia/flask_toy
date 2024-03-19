items_per_page = 2


def get_num_page(num_page: int):
    return (num_page - 1) * 2


def get_image(image: dict):
    return image["$binary"]["base64"]
