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
from flask_cors import CORS

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow




app = Flask(__name__)

# app = Flask(__name__)
app.config['SECRET_KEY'] = '4b70b5e6a77a9807c7e0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://flaskuser:flaskpassword@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)
app.app_context().push()
# db.create_all()
db.init_app(app)
ma = Marshmallow(app)
CORS(app)
with app.app_context():
    from . import routes  # Import routes

    db.create_all()  # Create sql tables for our data models




from flask_app import routes
