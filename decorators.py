from functools import wraps
from flask import session, redirect, url_for, flash, abort
from flask_login import current_user


def role_only(roles):
    def wrap(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.user_role not in roles:
                flash("Bạn không có quyền sử dụng chức năng này", "forbidden")
                return redirect('/home')
            return f(*args, **kwargs)
        return decorated_function
    return wrap