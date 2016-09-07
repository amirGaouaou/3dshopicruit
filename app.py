import os
import uuid

import urllib,json
from flask import Flask, render_template, redirect, request,jsonify

app = Flask(__name__)
app.debug = True

url = "http://shopicruit.myshopify.com/products.json?page="
prodType = ['Clock', 'Watch']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    total = 0
    page = 1
    prodlist = []
    result={}
    while True:
        response = urllib.urlopen(url+str(page))
        data = json.loads(response.read())
        if not data['products']:
            break
        for product in data['products']:
            type = product['product_type']
            if type == prodType[0] or type == prodType[1]:
                prodlist.append(product)
                for variant in product['variants']:
                    test = float(variant['price'])
                    total += test
        page+=1
    result['total']= "{0:.2f}".format(total)
    result['products']= prodlist
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

