"""
Market place Config
"""

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = '083fd1de6e125667b4d972b4'  # os.urandom(12).hex()

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


from market import routes
# from market.model import Item

