import os
import pdb
import flask
from flask import jsonify, render_template, url_for, flash, session, make_response, request
from flask_cors import cross_origin, CORS
from flask_login import login_user, logout_user, LoginManager
from flask_mail import Message, Mail
from flask_migrate import Migrate
from flask_restful import Resource, Api

from flask_bcrypt import Bcrypt

from flask_app import db, app
from flask_app.forms import RegistrationForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from flask_app.models import User, Token
from flask_app.serializers import RegisterSerializer
from flask_app.short_url import ShortUrlGenerator
from flask_app.token import TokenGenaration
from flask_app.validators import validate_credentials, password_validators

migrate = Migrate(app, db)
api = Api(app)
migrate.init_app(app)
CORS(app)
login_manager = LoginManager()
login_manager.init_app(app)
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
DATABASE_URL = os.getenv('DATABASE_URL')
# app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:ramesh123@localhost/flaskdatabase'

app.config['DEBUG'] = True
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)
mail.init_app(app)

bcrypt = Bcrypt()
smd = {
    'success': True,
    'message': 'registration sucessfull',
    'data': [],
}

register_schema = RegisterSerializer()


class Register(Resource):
    """
        Registration- class is used for registering the user credentials, and stores th credentials in the database
       Methods:
       --------
       post: Here post rest_api used to send the data to the database,and stores data into database
       get: here get method is use to get the data from the database,and also activating user for login.
       """

    @cross_origin()
    def post(self, *args, **kwargs):

        try:
            # pdb.set_trace()

            data = request.data

            # result = register_schema.dumps(data)
            # username=request.json['username']
            # result=register_schema.dump(username)
            # return jsonify(result)
            form = RegistrationForm()
            username = form.username.data
            email = form.email.data
            password = form.password.data
            confirm_password = form.confirm_password.data

            hashed_password = bcrypt.generate_password_hash(confirm_password)
            status = validate_credentials(password, email)

            if status:

                user = User(username=username, email=email, password=hashed_password)
                db.session.add(user)
                db.session.commit()
                user = User.query.filter_by(email=email).first()
                url = os.getenv('Url')
                token = TokenGenaration.encode_token(self, user)

                short = ShortUrlGenerator.short_url(self, 10)

                token = Token(token=token, short=short)
                db.session.add(token)
                db.session.commit()
                # characters=string.digits+string.ascii_letters
                # short_url=''.join(choices(characters,k=5))
                # link=self.query.filter(short_url=short_url).first()
                mail_subject = 'link to activate the account'
                msg = Message(mail_subject, sender=email, recipients=[MAIL_USERNAME])
                msg.body = f"Click here to activate : {url}/register/{short}"
                mail.send(msg)
                # status_code = flask.Response(status=200)
                # return status_code
                # return jsonify(smd, status=200)
                return jsonify({'status': True, 'message': 'mail sent for activating account'})
            else:
                # return Response(
                #     "The response body goes here",
                #     status=400,
                # )
                # return make_response()
                # return jsonify({'status': True, 'message': 'Error occured while activating account'})
                status_code = flask.Response(status=400)
                return status_code
                # return render_template('page_not_found.html'), 404
                # return jsonify({'message': 'enter valid credentials', }, status=400)
        except:
            status_code = flask.Response(status=406)
            #
            return status_code
            # return jsonify({'status': False, 'message': 'registration failed'})

    def get(self, token, *args, **kwargs):
        try:
            # pdb.set_trace()
            token_data = Token.query.filter_by(short=token).first()
            token = token_data.token
            details = TokenGenaration.decode_token(self, token)
            email = details['mail']
            user_id = details['id']
            user = User.query.filter_by(id=user_id).first()
            if user.is_active == 0:

                user.is_active = 1
                db.session.add(user)
                db.session.commit()
                # result = register_schema.dumps(user).data

                return jsonify({'status': True, 'message': 'account activation  success'})

            else:
                return jsonify({'status': False, 'message': 'account activation  failed'})

        except:
            return jsonify({'status': False, 'message': 'account is already activated'})


api.add_resource(Register, '/register')
api.add_resource(Register, '/register/<string:token>', endpoint='token')


class Login(Resource):
    """
          Login class is used for Logging into the flask_app using active credentials

          Methods:
          --------
          post: Post API is used to for storing the login credentials in to the database if the user is active

          """

    @cross_origin()
    def post(self, *args, **kwargs):

        try:
            pdb.set_trace()

            form = LoginForm()
            email = form.email.data
            password = form.password.data
            user = User.query.filter_by(email=email).first()
            if user.is_active == 1:
                user_id = user.id
                # db.session.add(user)

                # login_user(user)
                session['username'] = user.username
                session["email"] = user.email

                return jsonify({'status': True, 'message': 'login suessfull ', 'data': []})
            else:
                pass
        except:
            return flask.Response(status=400)


api.add_resource(Login, '/login')


class ForgotPasword(Resource):
    """
          For class is used for updating the password

            Methods:
            --------
            post: post API is used for checkong the forgot credentials, after checking credentials send token for
                forgot mailId

            put:Put Api is used for updating the password in the database
            """

    @cross_origin()
    def post(self):

        # import pdb
        # pdb.set_trace()
        try:
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
                return jsonify({'status': True, 'message': 'mail sent for reset ', 'data': token})
            else:
                return flask.Response(status=400)
        except:
            return flask.Response(status=400)

    @cross_origin()
    def put(self):

        # pdb.set_trace()
        try:
            token = request.headers.get('token')
            # token1=request.headers['token']
            form = ResetPasswordForm()

            password = form.password.data
            status = password_validators(password)
            if status:
                confirm_password = form.password.data
                details = TokenGenaration.decode_token(self, token)
                email = details['mail']
                user = User.query.filter_by(email=email).first()

                hashed_password = bcrypt.generate_password_hash(confirm_password)
                user = User.query.filter_by(username=user.username).first()
                if password == confirm_password:
                    user.password = hashed_password
                    db.session.add(user)
                    db.session.commit()
                    # return flask.Response(status=200)
                    return jsonify({'status': 200, 'message': 'password updated ', 'data': []})
        except:
            return jsonify({'status': False, 'message': 'reset failed'})


api.add_resource(ForgotPasword, '/forgot')
api.add_resource(ForgotPasword, '/forgot/<string:token>', endpoint='token1')


class Logout(Resource):
    """
            Logout API used for closing the flask-app

               Methods:
               --------
               post: post API is used for stop authentication and to close flask_app


               """

    def post(self):
        logout_user()
        return jsonify({'status': 200, 'message': 'logout suessfull ', 'data': []})


api.add_resource(Logout, '/logout')
