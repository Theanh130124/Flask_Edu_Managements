
from flask_login import logout_user, current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import  expose , BaseView ,Admin
from app.models import UserRole, Regulation, Subject, Teaching, Class, Profile, User, Student
from app import app , db
from flask import  redirect

#De authen
class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN #Phải có dòng sau này để người dùng STAFF không thể truy cập admin

class SubjectView(AuthenticatedView):
    column_labels = {
        'id':'Mã',
        'name': 'Tên môn',
        'grade' :'Khối ',
        'number_of_15p' :'15P',
        'number_of_45p' :'45P',

    }
class RegulationsView(AuthenticatedView):
    column_labels = {
        'type': 'Loại quy định',
        'regulation_name': 'Tên quy định',
        'min': 'Giá trị tối thiểu',
        'max': 'Giá trị tối đa',
    }
    can_view_details = True
class TeachingView(AuthenticatedView):
    column_list = ['id' , 'class_id', 'subject_id']
    can_view_details = True

class UserView(AuthenticatedView):
    column_list = ['name']
class ProfileView(AuthenticatedView):
    column_list = ['name']


admin = Admin(app , name = 'Quản lý học sinh ', template_mode='bootstrap4')

admin.add_view(RegulationsView(Regulation, db.session, name="Chỉnh sửa quy định"))
admin.add_view(AuthenticatedView(Subject, db.session , name="Danh sách môn học")) #Thêm
admin.add_view(LogoutView(name = 'Đăng xuất'))
admin.add_view(TeachingView(Teaching,db.session,name='Dạy học'))
admin.add_view(UserView(User,db.session,name='Người dùng'))
admin.add_view(ProfileView(Profile, db.session , name ="Hồ sơ"))

#Fix bug đăng xuất trả về login.html