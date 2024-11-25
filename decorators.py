from functools import wraps
from flask import session, redirect, url_for, flash, abort
from flask_login import current_user


def role_only(role):
    def wrap(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.user_role not in role:
                flash("Bạn không có quyền thực hiện chức năng này", "forbidden")
                # abort(403)
                return redirect(url_for("index"))
            else:
                return f(*args, **kwargs)
        return decorated_function
    return wrap