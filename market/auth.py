import jwt

from market import app
from market.form import LoginForm, RegistrationForm
from flask import request, redirect, url_for, render_template, jsonify, session
from market.model import User, LoginDate, db
from flask_login import login_user, current_user, logout_user
from flask import Blueprint
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST', 'GET'])
def login_page():
    # token = session.get('web-token', None)
    # if token:
    #     print(jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256"))
    # else:
    #     print('- not found', token)

    if current_user.is_authenticated:
        return redirect(url_for('home_page'))

    form = LoginForm(request.form)
    if request.method == 'GET':
        # token = jwt.encode({'web': True}, app.config['SECRET_KEY'])
        # session['web-token'] = token
        # print(token)
        return render_template('login.html', form=form)

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

    return render_template('login.html', form=form)



@auth.route('/registration', methods=['POST', 'GET'])
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


@auth.route('/logout')
def logout_page():
    if current_user.is_authenticated:
        logout_user()

    return redirect(url_for('auth.login_page'))
