# from flask import Flask
# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rameshb:ramesh@localhost/flaskdatabase'
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
#
# from flask_app import routes
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '4b70b5e6a77a9807c7e0'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("Flask_SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(app)





from flask_app import routes