

from flask_login import logout_user, current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import expose, BaseView, Admin
from app.models import UserRole, Regulation, Subject, Teaching, Class, Profile, User, Student, Notification , Semester
from app import app, db, login , utils
from flask import redirect, request
from app.controllers import hash_password
from app.dao import  dao_subject ,dao_semester , dao_class


# De authen
class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN  # Phải có dòng sau này để người dùng STAFF không thể truy cập admin


class LoginUserView(BaseView):
    @expose('/')
    def index(self):
        return redirect('/login')
    def is_accessible(self):
        return not current_user.is_authenticated

class SubjectAdminView(AuthenticatedView):
    column_list = ['id', 'name', 'grade', 'number_of_15p', 'number_of_45p', 'teachings']
    column_labels = {
        'id': 'Mã',
        'name': 'Tên môn',
        'grade': 'Khối ',
        'number_of_15p': 'Số bài kiểm tra 15P',
        'number_of_45p': 'Số bài kiểm tra 45P',
        'teachings': 'Áp dụng cho'
    }
    column_filters = [
        'name',
        'grade',
        'number_of_15p',
        'number_of_45p',
    ]
    can_view_details = True

    def format_teachings(view, context, model, name):
        if model.teachings:
            result = []
            for teaching in model.teachings:
                # Lấy thông tin từ các quan hệ liên kết
                class_name = teaching.classes.name if teaching.classes else 'Không rõ lớp'
                semester_name = teaching.semester.semester_name if teaching.semester else 'Không rõ học kỳ'
                teacher_name = teaching.teacher.profile.name if teaching.teacher and teaching.teacher.profile else 'Không rõ giáo viên'

                # Thêm thông tin vào danh sách
                result.append(f'Lớp: {class_name}, {semester_name}, Giáo viên: {teacher_name}')
            return ', '.join(result)  # Kết hợp danh sách thành chuỗi
        return 'Chưa áp dụng'

    # Sử dụng trong Flask-Admin
    column_formatters = {
        'teachings': format_teachings
    }


class RegulationsAdminView(AuthenticatedView):
    # Display class and student -> toString bên models -> displayname
    column_list = ['type', 'name', 'min_value', 'max_value', 'classes', 'students']

    column_labels = {
        'type': 'Loại quy định',
        'name': 'Tên quy định',
        'min_value': 'Giá trị tối thiểu',
        'max_value': 'Giá trị tối đa',
        'classes': 'Danh sách lớp',
        'students': 'Danh sách học sinh',
    }

    # Có thể xem chi tiết class và student
    column_details_list = ['type', 'name', 'min_value', 'max_value', 'classes', 'students']
    can_view_details = True


class UserView(AuthenticatedView):
    column_list = ['username', 'password', 'user_role', 'active', 'profile']
    # Phải loại bỏ học sinh khỏi profile ở đây
    column_labels = {
        'username': 'Tên đăng nhập',
        'password': 'Mật khẩu',
        'user_role': 'Vai trò',
        'active': 'Trạng thái',
        'profile': 'Họ tên người dùng'
    }
    column_filters = [
        'username',
        'user_role',
        'active',
    ]
    can_view_details = True

    # Lọc profile là học sinh
    def get_query(self):
        return self.session.query(self.model).filter(self.model.profile_id.notin_(
            self.session.query(Student.profile_id).distinct()
        ))

    # Hook sau
    def on_model_change(self, form, model, is_created):
        if is_created:
            model.password = hash_password(form.password.data)
        elif form.password.data:
            model.password = hash_password(form.password.data)
        return super().on_model_change(form, model, is_created)

class ProfileView(AuthenticatedView):
    column_list = ['name', 'email', 'birthday', 'gender', 'address', 'phone']
    column_labels = {
        'name': 'Họ tên',
        'email': 'Email',
        'birthday': 'Ngày sinh',
        'gender': 'Giới tính',
        'address': 'Địa chỉ',
        'phone': 'Số điện thoại'
    }
    column_filters = [
        'name',
        'email',
        'address',
        'phone',
    ]
    can_view_details = True


class ClassCreateView(AuthenticatedView):
    column_list = ['name' ,'grade','amount','year']
    column_labels = {
        'name': 'Tên lớp',
        'grade': 'Khối',
        'amount': 'Sỉ số',
        'year': 'Năm học',



    }
    can_edit = False
    can_view_details = True





class NotificationView(AuthenticatedView):
    column_list = ['subject','content','created_at']
    column_labels =  {
        'subject':'Tiêu đề thông báo',
        'content':'Nội dung',
        'created_at':'Thời gian tạo'
    }
    can_view_details = True

class StatView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html',list_subject= dao_subject.get_all_subject(),
                           )
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN
class StatInfoView(BaseView):
    @expose('/')
    def index(self):
        res = dao_subject.get_avg_score_by_class(request.args.get("semester"), request.args.get("subject"))
        classification = [int(item) if item is not None else 0 for item in dao_subject.num_of_classification(request.args.get("semester"), request.args.get("subject"))[0]]
        list_class_id = [t[0] for t in res]
        list_dtb = [t[1] for t in res]
        semester_id = request.args.get('semester')
        semester = dao_semester.get_semester_by_id(semester_id)

        return self.render('admin/stats_info.html', subject_info=dao_subject.get_subject_by_id(request.args.get("subject")),
                           semester =semester,
                           list_class_id=list_class_id,
                           list_dtb=list_dtb,
                           def_get_class=dao_class.get_class_by_id,
                           num_of_classification=classification,
                           top_5_student=dao_subject.top_5_highest_score_by_subject(request.args.get("semester"), request.args.get("subject")),
                           res_final=dao_subject.get_result_by_class(request.args.get("semester"), request.args.get("subject")))

    def is_visible(self):
        return False

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

admin = Admin(app, name='Quản lý học sinh ', template_mode='bootstrap4')

admin.add_view(RegulationsAdminView(Regulation, db.session, name="Chỉnh sửa quy định"))
admin.add_view(ClassCreateView(Class,db.session,name="Tạo lớp học"))
admin.add_view(SubjectAdminView(Subject, db.session, name="Quản lý môn học"))  # Thêm
admin.add_view(UserView(User, db.session, name='Người dùng'))
admin.add_view(ProfileView(Profile, db.session, name="Hồ sơ"))
admin.add_view(NotificationView(Notification , db.session,name="Quản lý thông báo"))
admin.add_view(StatView(name='Thống kê'))
admin.add_view(StatInfoView(name="Thống kê chi tiết"))
admin.add_view(LogoutView(name='Đăng xuất'))
admin.add_view(LoginUserView(name='Về trang đăng nhập người dùng'))

# Fix bug đăng xuất trả về login.html
