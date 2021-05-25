from market import app, login_manager
from flask import render_template, request, redirect, url_for, flash
from market.model import Product, db, User, LoginDate
from market.form import LoginForm, RegistrationForm
from flask_login import login_user, current_user, login_required, logout_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/profile')
@login_required
def profile_page():
    all_date = LoginDate.query.filter_by(username_id=current_user.id).all()
    all_date = [date.date for date in all_date]
    return render_template('profile.html', all_date=all_date)


@app.route('/', methods=['POST', 'GET'])
@app.route('/home', methods=['POST', 'GET'])
@login_required
def home_page():
    all_product = Product.query.all()
    brand = sorted(set([item[0] for item in db.session.query(Product.brand).all()]))
    brand.insert(0, 'ALL')
    return render_template('home.html', products=all_product, brands=brand)


@app.route('/your-buys', methods=['POST', 'GET'])
@login_required
def buy_product_page():
    all_product = Product.query.all()
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


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    print(request)
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if user.check_password(form.password.data):
                    login_user(user)
                    a = LoginDate(username_id=current_user.id)
                    db.session.add(a)
                    db.session.commit()
                    return redirect(url_for('home_page'))
                else:
                    form.new_errors = {'password': ['wrong password']}
            else:
                form.new_errors = {'username': ['This username not exist.']}

    if current_user.is_authenticated:
        return redirect(url_for('home_page'))

    return render_template('login.html', form=form)


@app.route('/registration', methods=['POST', 'GET'])
def registration_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))

    form = RegistrationForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            static = True
            if User.query.filter_by(username=form.username.data).first():
                form.new_errors = {'username': ['This username exist enter other one']}
                static = False

            if User.query.filter_by(email=form.email.data).first():
                form.new_errors = {'email': ['This email exist enter other one']}
                static = False

            if static:
                u1 = User(username=form.username.data,
                          email=form.email.data,
                          password=form.password.data)

                db.session.add(u1)
                db.session.commit()
                login_user(u1)
                a = LoginDate(username_id=current_user.id)
                db.session.add(a)
                db.session.commit()

                return redirect(url_for('home_page'))

    return render_template('registration.html', form=form)


@app.route('/logout')
def logout_page():
    if current_user.is_authenticated:
        logout_user()

    return redirect(url_for('login_page'))


@app.route('/buy-<product_id>', methods=['POST'])
@login_required
def buy_page(product_id):
    current_product = Product.query.filter_by(id=product_id).first()
    if current_product:
        if current_product.owner:
            flash('You already have this product.', category='danger')
        elif current_user.wallet >= current_product.price:
            current_product.owner = current_user.id
            current_user.wallet -= current_product.price
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
    if current_product:
        if current_user.id == current_product.owner:
            current_product.owner = None
            current_user.wallet += current_product.price
            db.session.commit()
            flash(f'Congratulation, you delete {current_product.name_en}.', category='success')
        else:
            flash('You dont have this product.', category='danger')
    else:
        flash('some thing gi=o wrong.', category='danger')

    return redirect(request.referrer)
