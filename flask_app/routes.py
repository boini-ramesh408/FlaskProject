import os
import pdb

import bcrypt as bcrypt
import flask
from flask import jsonify, render_template, url_for, flash, session, make_response
from flask_mail import Message, Mail
from flask_restful import Resource, Api
from httplib2 import Response

from flask_app import db, app
from flask_app.forms import RegistrationForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from flask_app.models import User
from flask_app.token import TokenGenaration
from flask_app.validators import validate_credentials

api = Api(app)
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
DATABASE_URL = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

app.config['DEBUG'] = True
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)
mail.init_app(app)

smd = {
    'success': True,
    'message': 'registration sucessfull',
    'data': [],
}


# sachinlokesh05

class Register(Resource):

    def post(self, *args, **kwargs):

        try:

            # pdb.set_trace()

            form = RegistrationForm()
            username = form.username.data
            email = form.email.data
            password = form.password.data
            status = validate_credentials(password, email)

            if status:
                user = User(username=username, email=email, password=password)
                db.session.add(user)
                db.session.commit()
                user = User.query.filter_by(email=email).first()
                url = os.getenv('Url')
                token = TokenGenaration.encode_token(self, user)
                # characters=string.digits+string.ascii_letters
                # short_url=''.join(choices(characters,k=5))

                # link=self.query.filter(short_url=short_url).first()
                mail_subject = 'link to activate the account'
                msg = Message(mail_subject, sender=email, recipients=[MAIL_USERNAME])
                msg.body = f"Click here to activate : {url}/forgot/{token}"

                mail.send(msg)

                flash('registration successfull')
                return jsonify(smd, status=200)
            else:
                # return Response(
                #     "The response body goes here",
                #     status=400,
                # )
                # return make_response()
                status_code = flask.Response(status=400)
                #
                return status_code
                # return render_template('page_not_found.html'), 404
                # return jsonify({'message': 'enter valid credentials', }, status=400)
        except:
            return jsonify({'status': False, 'message': 'registration failed'})

    def get(self, token, *args, **kwargs):
        try:
            # pdb.set_trace()

            details = TokenGenaration.decode_token(self, token)
            email = details['mail']
            user_id = details['id']
            user = User.query.filter_by(id=user_id).first()
            if user.active == 0:

                user.active = 1
                db.session.add(user)
                db.session.commit()

                return jsonify({'status': 200, 'message': 'token activation suessfull', 'data': []})
            else:
                return jsonify({'status': 400, 'message': 'token already activated', 'data': []})

        except:
            return jsonify({'status': False, 'message': 'token activation  failed'})


api.add_resource(Register, '/register')
api.add_resource(Register, '/register/<string:token>', endpoint='token')


class Login(Resource):

    def post(self, *args, **kwargs):
        try:
            # pdb.set_trace()
            form = LoginForm()
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(email=email).first()
            if user.active == 1:
                user_id = user.id
                session['username'] = user.username
                session["email"] = user.email
                flash('login successfully')
            return jsonify({'status': 200, 'message': 'login suessfull ', 'data': []})
        except:
            return jsonify({'status': False, 'message': 'login failed'})


api.add_resource(Login, '/login')


class ForgotPasword(Resource):

    def post(self):

        import pdb
        pdb.set_trace()

        form = ForgotPasswordForm()
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            url = os.getenv('Url')
            token = TokenGenaration.encode_token(self, user)
            mail_subject = 'link to activate the account'
            msg = Message(mail_subject, sender=email, recipients=[MAIL_USERNAME])
            msg.body = f"Click here to reset : {url}/forgot/{token}"
            mail.send(msg)

    def get(self, token, *args, **kwargs):
        try:
            # pdb.set_trace()

            details = TokenGenaration.decode_token(self, token)
            email = details['mail']
            user_id = details['id']
            user = User.query.filter_by(id=user_id).first()
            if user.active == 0:

                user.active = 1
                db.session.add(user)
                db.session.commit()

                return jsonify({'status': 200, 'message': 'token activation suessfull', 'data': []})
            else:
                return jsonify({'status': 400, 'message': 'token already activated', 'data': []})

        except:
            return jsonify({'status': False, 'message': 'token activation  failed'})

    def put(self, token):

        pdb.set_trace()
        try:
            form = ResetPasswordForm()

            password = form.password.data
            confirm_password = form.password.data("confirm_password")
            details = TokenGenaration.decode_token(self, token)
            email = details['mail']
            user = User.query.filter_by(email=email).first()

            hashed_password = bcrypt.generate_password_hash(confirm_password).decode('utf-8')
            user = User.query.filter_by(username=user.username).first()
            user.password = hashed_password
            db.session.add(user)
            db.session.commit()
        except:
            return jsonify({'status': False, 'message': 'reset failed'})



api.add_resource(ForgotPasword, '/forgot')
api.add_resource(ForgotPasword, '/forgot/<string:token>',endpoint='token1')


class Logout(Resource):
    def post(self):
        session.clear()


api.add_resource(Logout, '/logout')
