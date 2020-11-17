from twilio.rest import Client
from .env import Env
import datetime
import jwt
import sys
import os
from os.path import join
sys.path.append(join(os.getcwd(), '..'))
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
