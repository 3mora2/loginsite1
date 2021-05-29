from flask import render_template
from flask_login import login_required

from . import app, db
from .model import Product


@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
@login_required
def home_page():
    all_product = Product.query.all()
    brand = sorted(set([item[0] for item in db.session.query(Product.brand).all()]))
    brand.insert(0, 'ALL')
    return render_template('home.html', products=all_product, brands=brand)