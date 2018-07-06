from flask import request
from flask_api import FlaskAPI

app = FlaskAPI(__name__)

PRODUCTS = []


def create_product(product):
    PRODUCTS.append(product)


@app.route('/products', methods=['GET', 'POST'])
def prodcuts():
    if request.method == 'POST':
        create_product(request.json)
        return PRODUCTS[-1]
    elif request.method == 'GET':
        return PRODUCTS


@app.route('/', methods=['GET'])
def index():
    return {'mgs': 'Ok'}


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)