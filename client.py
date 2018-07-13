"""Client side to be installed on rasberry pi with a zapper
"""
import os
import requests

START_CODE = 'start'
EXIT_CODE = 'exit'
ADD_PRODUCTS = 'add'
STOP_CODE = 'stop'

host = 'http://localhost:5000'


def add_product(product_id):
    print("Product %s" % product_id)
    url = os.path.join(host, 'products')
    payload = {
        'ean': int(product_id)
    }
    try:
        response = requests.post(url, json=payload)
    except Exception:
        print("Unable to send product %s to the server" % (product_id))
        raise

    try:
        response.raise_for_status()
    except Exception as e:
        print("%r" % (e))



def add_products():
    product_id = input("scan product to add : ")
    while product_id != STOP_CODE:
        add_product(product_id)
        product_id = input("scan product to add : ")


if __name__ == '__main__':
    actions = {
        ADD_PRODUCTS: add_products,
    }
    code = START_CODE
    while code != EXIT_CODE:
        code = input('Scan action :') # input by read by the zapper
        action = actions[code]
        action()


