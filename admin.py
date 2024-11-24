from flask_login import logout_user, current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import  expose , BaseView
from app.models import UserRole
from flask import  redirect

class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/login')

    def is_accessible(self):
        return current_user.is_authenticated