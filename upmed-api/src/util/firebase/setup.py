import os
from os import path

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

"""
Initialize a Firebase instance
"""
path_to_key = path.join(os.path.dirname(os.path.realpath(__file__)), 'upmed-starmen-firebase-adminsdk-1q74r-24bca7fa41.json')
cred = credentials.Certificate(path_to_key)
firebase_admin.initialize_app(cred)

"""
Expose authenticated globals to adjacent files
"""
db = firestore.client()
