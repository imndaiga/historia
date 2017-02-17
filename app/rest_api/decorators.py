from functools import wraps
from flask import request, jsonify, _app_ctx_stack
import jwt
import os

# AUTH0 JWT DECODING
client_secret = os.environ.get('CLIENT_SECRET', None)
client_id = os.environ.get('CLIENT_ID', None)


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
                client_secret,
                audience=client_id
            )
        except jwt.ExpiredSignature:
            return handle_error({'code': 'token_expired',
                                 'description': 'token is expired'}, 401)
        except jwt.InvalidAudienceError:
            return handle_error({'code': 'invalid_audience',
                                 'description': 'Incorrect audience,'
                                 'expected:' + client_id}, 401)
        except jwt.DecodeError:
            return handle_error({'code': 'token_invalid_signature',
                                 'description':
                                     'token signature is invalid'}, 401)
        except Exception:
            return handle_error({'code': 'invalid_header',
                                 'description': 'Unable to parse'
                                 ' authentication token'}, 400)

        _app_ctx_stack.top.current_user = payLoad
        return f(*args, **kwargs)
    return decorated
