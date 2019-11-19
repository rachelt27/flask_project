from bson.objectid import ObjectId
from flask import Flask, render_template, abort, redirect, request, url_for, jsonify
from flask_pymongo import PyMongo
import bson
from fooApp.forms import ProductForm

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'foodb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/foodb'

mongo = PyMongo(app)


@app.route('/')
def index():
    return redirect(url_for('products_list'))


@app.route('/products/')
def products_list():
    """Provide HTML listing of all Products."""
    # Query: Get all Products objects, sorted by date.
    products = mongo.db.products.find()[:]
    return render_template('product/index.html',
                       products=products)


@app.route('/products/<product_id>/')
def product_detail(product_id):
    """Provide HTML page with a given product."""
    # Query: get Product object by ID.
    product = mongo.db.products.find_one({"_id": ObjectId(product_id)})
    print(product)
    if product is None:
        # Abort with Not Found.
        abort(404)
    return render_template('product/detail.html',
                           product=product)


@app.route(
    '/products/<product_id>/edit/',
    methods=['GET', 'POST'])
def product_edit(product_id):
    return 'Form to edit product #.'.format(product_id)


@app.route('/products/create/', methods=['GET', 'POST'])
def product_create():
    """Provide HTML form to create a new product."""
    form = ProductForm(request.form)
    if request.method == 'POST' and form.validate():
        mongo.db.products.insert_one(form.data)
        # Success. Send user back to full product list.
        return redirect(url_for('products_list'))
    # Either first load or validation error at this point.
    return render_template('product/edit.html', form=form)


@app.route('/products/<product_id>/delete/', methods=['DELETE'])
def product_delete(product_id):
    """Delete record using HTTP DELETE, respond with JSON."""
    result = mongo.db.products.delete_one({ "_id": ObjectId(product_id) })
    if result.deleted_count == 0:
        # Abort with Not Found, but with simple JSON response.
        response = jsonify({'status': 'Not Found'})
        response.status = 404
        return response
    return jsonify({'status': 'OK'})


@app.errorhandler(404)
def error_not_found(error):
    return render_template('error/not_found.html'), 404


@app.errorhandler(bson.errors.InvalidId)
def error_not_found(error):
    return render_template('error/not_found.html'), 404


if __name__ == "__main__":
    app.run()
