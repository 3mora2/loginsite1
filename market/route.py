from market import app, login_manager
from flask import render_template, request, redirect, flash, jsonify
from market.model import Product, db, User

from flask_login import current_user, login_required


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@app.route('/your-buys', methods=['POST', 'GET'])
@login_required
def buy_product_page():
    all_product = current_user.items
    brand = sorted(set([item[0] for item in db.session.query(Product.brand).all()]))
    brand.insert(0, 'ALL')
    return render_template('buy_product.html', products=all_product, brands=brand)


@app.route('/brand-<brand>')
@login_required
def brand_page(brand):
    brand = brand.strip()
    if brand == 'ALL':
        product = Product.query.all()
    else:
        product = Product.query.filter_by(brand=brand).all()

    if product:
        return render_template('current_brand.html', products=product)
    else:
        return 'Not found'


@app.route('/product/<id_product>')
@login_required
def product_page(id_product):
    product = Product.query.filter_by(id=id_product).first()
    if product:
        return render_template('product.html', product=product)
    else:
        return 'Some Thing Go Wrong'


@app.route('/buy-<product_id>', methods=['POST'])
@login_required
def buy_page(product_id):
    current_product = Product.query.filter_by(id=product_id).first()
    if current_product and current_product not in current_user.items and current_product.quantity > 0:
        if current_user.wallet >= current_product.price:
            current_user.items.append(current_product)
            current_user.wallet -= current_product.price
            current_product.quantity -= 1
            db.session.commit()
            flash(f'Congratulation, you buy {current_product.name_en} for {current_product.price}.', category='success')
        else:
            flash('You dont have enough money.', category='danger')
    else:
        flash('some thing go wrong.', category='danger')

    return redirect(request.referrer)


@app.route('/delete-<product_id>', methods=['POST'])
@login_required
def delete_page(product_id):
    current_product = Product.query.filter_by(id=product_id).first()
    if current_product in current_user.items:
        current_user.items.remove(current_product)
        current_user.wallet += current_product.price
        current_product.quantity += 1
        db.session.commit()
        flash(f'Congratulation, you delete {current_product.name_en}.', category='success')
    else:
        flash('You dont have this product.', category='danger')

    return redirect(request.referrer)
