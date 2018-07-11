"""
This is the entry point of the app
"""
from flask import request
from flask_api import FlaskAPI

APP = FlaskAPI(__name__)


class Product:
    """This is the product Model manager
    """
    def __init__(self):
        self.products = []

    def add(self, product):
        """Add a products into the model
        :param product: product to add
        :return: None
        """
        self.products.append(product)

    def all(self):
        """Get all products from the model
        :return: list(dict)
        """
        return self.products


class ProductManager:
    """Logic
    """
    def __init__(self, model):
        self.model = model

    def add_product(self, product):
        """This is the loguic of add product
        :param product: product to add from client
        :return: product added
        """
        self.model.add(product)
        return self.model.all()[-1]

    def get_product(self, product_id):
        """Get seach produc with id
        :param product_id: id of product
        :return: product with id == product_id
        """
        return list(filter(lambda x: x['id'] == product_id, self.model.all()))

    def get_products(self):
        """Get all products
        :return: all products
        """
        return self.model.all()

    def get_product_with_quantity(self):
        products = self.model.all()
        ids = (product['ean'] for product in products)
        from collections import Counter
        counter = Counter(ids)
        return counter


MODEL = Product()
PRODUCT_MANAGER = ProductManager(MODEL)

@APP.route('/fridge', methods=['GET'])
def fridge():
    """
    Get products in the fridge
    :return:
    """
    return PRODUCT_MANAGER.get_product_with_quantity()


@APP.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """View of get product
    :param product_id:
    :return: list(dict)
    """
    return PRODUCT_MANAGER.get_product(product_id)


@APP.route('/products', methods=['POST'])
def create_product():
    """View of create products
    :return: product
    """
    product = PRODUCT_MANAGER.add_product(request.json)
    return product


@APP.route('/products', methods=['GET'])
def products():
    """view for get all products
    :return: all products
    """
    return PRODUCT_MANAGER.get_products()


@APP.route('/', methods=['GET'])
def index():
    """Ping
    :return: dict
    """
    return {'mgs': 'Ok'}


if __name__ == '__main__':
    APP.run('0.0.0.0', debug=True)
