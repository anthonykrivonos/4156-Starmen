from flask import Blueprint

patient_endpoints = Blueprint('patient', __name__)

@patient_endpoints.route('/')
def root():
    return "patient"
