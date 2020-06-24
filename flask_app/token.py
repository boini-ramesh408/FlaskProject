import os
import jwt

SECRET_KEY_Token = os.getenv('SECRET_KEY_Token')


class TokenGenaration:
    def encode_token(self, user):
        payload = \
            {
                'username': user.username,
                'mail': user.email,
                'id': user.id
            }
        token = jwt.encode(payload, SECRET_KEY_Token, algorithm='HS256').decode('utf-8')
        return token

    def decode_token(self, token):

        details = jwt.decode(token,SECRET_KEY_Token, algorithm='HS256')
        return details



