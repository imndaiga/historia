from functools import wraps
from flask import request, jsonify, _app_ctx_stack
import jwt
import os
from ..models import Person
from .. import db, seed

jwt_secret = os.environ.get('JWT_SECRET', 'superSECRETth!ng')


def handle_error(error, status_code):
    resp = jsonify(error)
    resp.status_code = status_code
    return resp


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', None)
        if not auth:
            return handle_error({'code': 'authorization_header_missing',
                                 'description':
                                     'Authorization header is expected'}, 401)

        parts = auth.split()
        if parts[0].lower() != 'bearer':
            return handle_error({'code': 'invalid_header',
                                 'description':
                                     'Authorization header must start with'
                                     'Bearer'}, 401)
        elif len(parts) == 1:
            return handle_error({'code': 'invalid_header',
                                 'description':
                                     'Authorization Token not found'}, 401)
        elif len(parts) > 2:
            return handle_error({'code': 'invalid_header',
                                 'description':
                                     'Authorization header must be Bearer'
                                     '+ \s + token'}, 401)

        token = parts[1]

        try:
            payLoad = jwt.decode(
                token,
                jwt_secret
            )
        except jwt.ExpiredSignature:
            return handle_error({'code': 'token_expired',
                                 'description': 'token is expired'}, 401)
        except jwt.DecodeError:
            return handle_error({'code': 'token_invalid_signature',
                                 'description':
                                     'token signature is invalid'}, 401)
        except Exception:
            return handle_error({'code': 'invalid_header',
                                 'description': 'Unable to parse'
                                 ' authentication token'}, 400)
        user_id = payLoad['id']
        print('Validating ID: {}'.format(user_id))
        (person, created_status) = seed._get_or_create_one(
            session=db.session,
            model=Person,
            create_method='auto',
            id=user_id
        )
        if (created_status is True):
            print('User registered')
        else:
            print('User already registered')
        _app_ctx_stack.top.current_user = payLoad
        return f(*args, **kwargs)
    return decorated
