from market import db, bcrypt, login_manager
from flask_bcrypt import check_password_hash
from flask_login import UserMixin
from datetime import datetime

products = db.Table('prod',
                    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
                    )


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    brand = db.Column(db.String(), nullable=False, default='_')
    desk_en = db.Column(db.String())
    img = db.Column(db.String(), nullable=False)
    other_img = db.Column(db.String(), nullable=False)
    quantity = db.Column(db.Integer)
    # owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    @property
    def item_to_json(self):
        return {"id": self.id,
                "name_en": self.name_en,
                "price": self.price,
                "img": self.img,
                "owner": self.owner
                }


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    _password = db.Column(db.String(), nullable=False)
    wallet = db.Column(db.Integer, nullable=False, default=1000)
    # items = db.relationship('Product', backref='owned_user', lazy=True)
    items = db.relationship('Product', secondary=products, backref=db.backref('owned_user', lazy=True))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = bcrypt.generate_password_hash(password).decode()

    def check_password(self, password):
        return check_password_hash(self.password, password)


class LoginDate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime, default=datetime.now())  # strftime("%d/%m/%Y %H:%M:%S")