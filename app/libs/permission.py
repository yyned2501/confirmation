from functools import wraps

from flask_login import current_user

from app.models.confirmation import ConfirmationLink


def permission_required(permission):
    def wrap(f):
        @wraps(f)
        def _wrap(*args, **kwargs):
            if current_user.can(permission):
                return f(*args, **kwargs)
            else:
                return "您没有权限访问该页面"

        return _wrap

    return wrap


def user_permission(f):
    @wraps(f)
    def _wrap(*args, **kwargs):
        if kwargs.get("co_id"):
            co_id = int(kwargs.get("co_id"))
            if ConfirmationLink.query.get(co_id).user == current_user:
                return f(*args, **kwargs)
            else:
                return "不是您的客户，请不要随便输入地址访问"
        else:
            return f(*args, **kwargs)

    return _wrap
