from flask import request
from flask_api import FlaskAPI

app = FlaskAPI(__name__)


class Product:
    def __init__(self):
        self.products = []

    def add(self, product):
        self.products.append(product)

    def all(self):
        return self.products


class ProductManager:
    def __init__(self, model):
        self.model = model

    def add_product(self, product):
        self.model.add(product)
        return self.model.all()[-1]

    def get_product(self, product_id):
        return list(filter(lambda x: x['id'] == product_id, self.model.all()))

    def get_products(self):
        return self.model.all()


MODEL = Product()
PRODUCT_MANAGER = ProductManager(MODEL)


@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    products = PRODUCT_MANAGER.get_product(product_id)
    return products


@app.route('/products', methods=['POST'])
def create_product():
    product = PRODUCT_MANAGER.add_product(request.json)
    return product


@app.route('/products', methods=['GET'])
def products():
    return PRODUCT_MANAGER.get_products()


@app.route('/', methods=['GET'])
def index():
    return {'mgs': 'Ok'}


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)