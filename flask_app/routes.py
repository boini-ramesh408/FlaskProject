import jwt as jwt
from flask import jsonify, render_template, url_for
from flask_mail import Message, Mail
from flask_restful import Resource, Api
from flask_app import db, app
from flask_app.forms import RegistrationForm
from flask_app.models import User

api = Api(app)
mail = Mail(app)

app.config.update(dict(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME='rameshboini408@gmail.com',
    MAIL_PASSWORD='Rammi408',
    DEFAULT_MAIL_SENDER='rameshboini408@gmail.com',
)

)
class Register(Resource):

    def post(self):
        try:
            import pdb
            pdb.set_trace()
            form = RegistrationForm()
            username = form.username.data
            email = form.email.data
            password = form.password.data

            user = User(username=username, email=email, password=password)
            # user_exist = User.query.filter_by(email=email).first()

            db.session.add(user)
            db.session.commit()
            user = User.query.filter_by(email=email).first()

            db_id = user.id
            token = jwt.encode({'id': db_id, "email": email}, 'secret', algorithm='HS256').decode('utf-8')
            # short = short_object.short_url(10)
            mail_subject = 'link to activate the account'
            msg = Message(mail_subject,
                          sender="rameshboini408@gmail.com",
                          recipients=["rameshboini408@gmail.com"])
            mail.send(msg)
            return jsonify("registration sucesfull")

        except:
            return jsonify("registration failed")


api.add_resource(Register, '/register')


@app.route('/activate/token=<string:token>/')
def activate(token):
    # getting token from short url in mail
    # secure = Secure.query.filter_by(short=token).first()
    # l_token = secure.token
    #
    # # decoding token to get user id
    # payload = jwt.decode(l_token, 'secret', algorithms=['HS256'])
    # user_id = payload.get('id')
    #
    # # activating user by updating User table
    # user = User.query.filter_by(id=user_id).first()
    # user.active = 1
    # db.session.commit()

    return render_template('activate.html', token=token)
