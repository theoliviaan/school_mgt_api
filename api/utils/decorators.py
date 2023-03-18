from ..models.user import User
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from functools import wraps
from http import HTTPStatus


def get_user_type(id:int):
    user = User.query.filter_by(id=id).first()
    if user:
        return user.user_type
    else:
        return None

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if get_user_type(claims['sub']) == 'admin':
                return fn(*args, **kwargs)
            else:
                return {"message": "Administrator access required"}, HTTPStatus.FORBIDDEN
        return decorator
    return wrapper