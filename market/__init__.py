from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

# import os
# os.urandom(32)

SECRET_KEY = b'ammar'

app = Flask(__name__, template_folder=r'..\templates')
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///..\dbase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = SECRET_KEY
app.config["JWT_SECRET_KEY"] = f"{SECRET_KEY}super-secret"  # Change this!
# csrf = CSRFProtect(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
api = Api(app)
login_manager = LoginManager(app=app)
login_manager.login_view = '/login'

from . import route, home, profile, auth, api_file
app.register_blueprint(auth.auth)
