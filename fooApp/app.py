from flask import Flask, make_response, request, Response, url_for

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello world!"


@app.route('/products/')
def products_list():
    return 'Listing of all products we have.'


@app.route('/products/<product_id>/')
def product_detail(product_id):
    return 'Detail of product     #{}.'.format(product_id)


@app.route(
    '/products/<product_id>/edit/',
    methods=['GET', 'POST'])
def product_edit(product_id):
    return 'Form to edit product #.'.format(product_id)


@app.route('/products/create/', methods=['GET', 'POST'])
def product():
    return 'Form to create a new product.'


@app.route('/products/<product_id>/delete/', methods=['DELETE'])
def product_delete(product_id):
    raise NotImplementedError('DELETE')


if __name__ == "__main__":
    app.run()
