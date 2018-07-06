from flask_api import FlaskAPI

app = FlaskAPI(__name__)

@app.route('/products', methods=['GET'])
def prodcuts():
    products = [{
        'id': 1,
        'ean': 123123123
    }]
    return products

@app.route('/', methods=['GET'])
def index():
    return {'mgs': 'Ok'}

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)