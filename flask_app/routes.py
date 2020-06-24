import os
from flask import jsonify, render_template, url_for, flash
from flask_mail import Message, Mail
from flask_restful import Resource, Api
from flask_app import db, app
from flask_app.forms import RegistrationForm, LoginForm
from flask_app.models import User
from flask_app.token import TokenGenaration

api = Api(app)
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rameshb:ramesh@localhost/flaskdatabase'

app.config['DEBUG'] = True
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)
mail.init_app(app)
import pdb


class Register(Resource):

    def post(self, *args, **kwargs):

        try:

            # pdb.set_trace()

            form = RegistrationForm()
            username = form.username.data
            email = form.email.data
            password = form.password.data
            user = User(username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            user = User.query.filter_by(email=email).first()
            db_id = user.id
            url = "127.0.0.1:5000"
            token = TokenGenaration.encode_token(self, user)
            mail_subject = 'link to activate the account'
            msg = Message(mail_subject, sender=email, recipients=[MAIL_USERNAME])
            msg.body = f"Click here to activate : {url}/register/{token}"

            mail.send(msg)

            flash('registration successfull')
            return jsonify({'status': True, 'message': 'registration sucesfull', 'data': []})
        except:
            return jsonify({'status': False, 'message': 'registration failed'})

    def get(self, token):
        try:
            pdb.set_trace()
            details = TokenGenaration.decode_token(self, token)
            # email = details['mail']
            user_id=details['id']
            user = User.query.filter_by(id=user_id).first()
            user.active = 1
            db.session.add(user)
            db.session.commit()

            return jsonify({'status': True, 'message': 'token activation suessfull', 'data': []})
        except:
            return jsonify({'status': False, 'message': 'token activation  failed'})


api.add_resource(Register, '/register')
api.add_resource(Register, '/register/<string:token>', endpoint='token')


class Login(Resource):

    def post(self):
        try:
            pdb.set_trace()
            form = LoginForm()
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(email=email).first()
            if user.active==1:
                # user_id = user.id
            flash('login successfully')
            return jsonify({'status': True, 'message': 'login suessfull ', 'data': []})
        except:
            return jsonify({'status': False, 'message': 'login failed'})

api.add_resource(Login, '/login')
