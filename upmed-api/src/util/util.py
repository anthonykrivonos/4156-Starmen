import datetime
import jwt
from twilio.rest import Client
from twilio.jwt.access_token import AccessToken

from .env import Env

"""
Util and helper functions
"""


class Auth:
    """ TOKEN FUCNTIONS"""

    def encode_auth_token(self, user_id, type):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() +
                datetime.timedelta(days=7, seconds=0),
                'iat': datetime.datetime.utcnow(),
                'googleId': user_id,
                'userType': type
            }
            return jwt.encode(
                payload,
                Env.UPMED_PRIVATE_KEY(),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, Env.UPMED_PRIVATE_KEY())
            # print(payload)
            return payload['googleId'], payload['userType']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.', None
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.', None


class Twilio():

    def connect(self):
        account_sid = Env.TWILIO_ACCOUNT_SID()
        auth_token = Env.TWILIO_AUTH_TOKEN()
        return Client(account_sid, auth_token)

    @staticmethod
    def access_token(identity):
        return AccessToken(Env.TWILIO_ACCOUNT_SID(), Env.TWILIO_API_KEY_SID(),
                           Env.TWILIO_API_KEY_SECRET(), identity=identity)
