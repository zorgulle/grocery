"""
This is the entry point of the app
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

from flask_api import FlaskAPI
from flask import request

APP = FlaskAPI(__name__)
engine = create_engine('sqlite:///my_db.db')
session = sessionmaker(bind=engine, autocommit=True)()


Base = declarative_base()


class Stock(Base):
    __tablename__='Stock'

    ean = Column(String, primary_key=True)
    quantity= Column(Integer)

def format_product(product):
    return {'ean': product.ean, 'quantity': product.quantity}

@APP.route('/products/<string:ean>', methods=['DELETE'])
def delete_product(ean):
    product = session.query(Stock).filter_by(ean=ean).first()
    if not product:
        return {"Error": "No product found"}

    product.quantity -= 1
    product.quantity = max(0, product.quantity)

    session.add(product)
    return format_product(product)


@APP.route('/products/<string:ean>', methods=['GET'])
def get_product(ean):
    product = session.query(Stock).filter_by(ean=ean).first()
    if not product:
        return {"Error": "No product found"}
    return format_product(product)


@APP.route('/products', methods=['GET'])
def get_products():
    products = session.query(Stock).all()
    return [format_product(product) for product in products]


@APP.route('/products', methods=['POST'])
def create_product():
    data = request.json
    product = session.query(Stock).filter_by(ean=data['ean']).first()
    if product:
        product.quantity += 1
    else:
        product = Stock(ean=data['ean'], quantity=1)
    session.add(product)
    return format_product(product)


@APP.route('/', methods=['GET'])
def index():
    return {'mgs': "ok"}


if __name__ == '__main__':
    APP.run('0.0.0.0', debug=True)
