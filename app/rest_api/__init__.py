from flask import Blueprint
from flask_restful import Api
from flask_cors import CORS

api_bp = Blueprint('api', __name__)
api = Api(api_bp)
CORS(api_bp)

from . import endpoints, forms
