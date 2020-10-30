from flask import Blueprint

hcp_endpoints = Blueprint('hcp', __name__)

@hcp_endpoints.route('/')
def root():
    return "hcp"
