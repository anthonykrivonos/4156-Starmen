import os
import atexit
from simplecrypt import decrypt

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from sys import path
from os.path import join, dirname
path.append(join(dirname(__file__), '../../..'))

from src.util.env import Env  # noqa


# Paths to encrypted and decrypted certificates
enc_cert_path = join(
    os.path.dirname(
        os.path.realpath(__file__)),
    'encrypted_cert.enc')
dec_cert_path = join(
    os.path.dirname(
        os.path.realpath(__file__)),
    'decrypted_cert.json')

"""
Read encrypted file
"""
with open(enc_cert_path, mode="rb") as file:
    encrypted_cert = file.read()

"""
Decrypt and write decrypted file
"""
decrypted_cert = decrypt(Env.FIREBASE_PRIVATE_KEY(), encrypted_cert)
with open(dec_cert_path, mode="wb") as file:
    file.write(decrypted_cert)

"""
Ensure decrypted JSON certificate is deleted on exit
"""


def delete_decrypt_on_exit():
    os.remove(dec_cert_path)


atexit.register(delete_decrypt_on_exit)

"""
Initialize a Firebase instance with the decrypted certificate
"""
cred = credentials.Certificate(dec_cert_path)
firebase_admin.initialize_app(cred)

"""
Expose authenticated globals to adjacent files
"""
db = firestore.client()
