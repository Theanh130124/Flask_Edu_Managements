import math

from app.admin import *
from app import dao, login, app ,utils
from flask import render_template, redirect, request, flash, url_for, jsonify ,  session
from flask_login import current_user, login_required, logout_user, login_user
from app.dao import dao_authen, dao_student, dao_regulation, dao_class , dao_notification , dao_semester , dao_teacher
from app.dao.dao_authen import display_profile_data, update_acc_info, auth_user
from app.dao.dao_regulation import get_regulation_by_type
from app.models import UserRole, TYPE_REGULATION  # Phải ghi là app.models để tránh lỗi profile
from app.utils import get_current_semester
from form import AdmisionStudent, LoginForm, Info_Account, ChangeClass
from decorators import role_only
from datetime import datetime
import cloudinary.uploader


# Index là home
# Hàm này luôn truyền vào
@app.context_processor
def common_attr():
    if current_user.is_authenticated:
        profile = dao_authen.get_info_by_id(current_user.id)
        user = dao_authen.load_user(current_user.id)
        semester_name, year = get_current_semester()
        semester = dao_semester.get_or_create_semester(semester_name, year)
        return {'profile': profile,
                'user': user,
                'semester_name':semester.semester_name,
                'year':semester.year,}
    return {}


# Tải người dùng lên

@login.user_loader
def user_load(user_id):
    return dao_authen.load_user(user_id)


# import pdb
# pdb.set_trace()
@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.user_role == UserRole.ADMIN:
            return redirect("/admin")
        return redirect("/home")
    return redirect('/login')


# Nếu truyền url_for sẽ vào index -> truyền redirect thì vào router
@app.route('/home')
@login_required  # Có cái này để gom user vào -> home
@role_only([UserRole.STAFF, UserRole.TEACHER])
def home():
    page = request.args.get('page', 1 , type=int)
    notifications= dao_notification.load_all_notifications(page=page)
    total = dao_notification.count_notifications()
    return render_template('index.html', notifications=notifications, current_page=page,
                           total_pages=math.ceil(total/app.config["PAGE_SIZE_NOTIFICATIONS"]) )  # Trang home (index.html)


@app.route('/login', methods=['GET', 'POST'])
def login():
    mse = ""
    form = LoginForm()
    if request.method == "POST" and form.SubmitFieldLogin():
        username = form.username.data
        password = form.password.data
        user = dao_authen.auth_user(username=username, password=password)
        if user:
            login_user(user)
            return redirect(url_for('index'))
        mse = "Tài khoản hoặc mật khẩu không đúng"
    return render_template('login.html', form=form, mse=mse)


@app.route('/logout', methods=['get'])
def logout_my_user():
    logout_user()
    return redirect('/login')


# import pdb
# pdb.set_trace()

@app.route('/student/register', methods=['GET', 'POST'])
@login_required
@role_only([UserRole.STAFF])
def register():
    form_student = AdmisionStudent()
    regulation_age = get_regulation_by_type(TYPE_REGULATION.RE_AGE)
    min_age = regulation_age.min_value  # độ tuổi tối thiểu
    max_age = regulation_age.max_value  # độ tuổi tối đa
    if request.method == "POST":
        if form_student.validate_on_submit():
            try:
                birth_date = form_student.birth_date.data
                current_year = datetime.now().year
                age = current_year - birth_date.year
                if age < min_age or age > max_age:
                    flash(f"Độ tuổi phải từ {min_age} đến {max_age}!", "danger")
                    return redirect(url_for("register"))
                dao_student.create_student(form_student)
                flash("Tạo học sinh thành công!", "success")
                return redirect(url_for("register"))
            except Exception as e:
                flash(f"Đã xảy ra lỗi khi tạo học sinh: {e}", "danger")
                return render_template("register_student.html", form_student=form_student)
        else:
            utils.display_form_errors(form_student)
            return render_template("register_student.html", form_student=form_student)

    return render_template("register_student.html", form_student=form_student)


# import pdb
# pdb.set_trace()
@app.route('/acc_info', methods=['GET', 'POST'])
@login_required
@role_only([UserRole.STAFF, UserRole.TEACHER])
def info_acc():
    form_account = Info_Account()
    profile = dao_authen.get_info_by_id(current_user.id)

    if form_account.validate_on_submit():
        try:
            update_acc_info(form_account)
            db.session.refresh(current_user)
            flash('Thông tin tài khoản đã được cập nhật !', 'success')
            return redirect('/acc_info')
        except Exception as e:
            flash(f'Cập nhật không thành công. Lỗi: {str(e)}', 'danger')
    else:
        utils.display_form_errors(form_account)
    display_profile_data(profile, form_account)
    return render_template('acc_info.html', form_account=form_account)


#
# @app.route('/class/change', methods=['GET','POST'])
# @login_required
# @role_only([UserRole.STAFF])
# def change_class():
#     form_create_class = ChangeClass()
#     form_create_class.teacher.choices = [(temp_teacher.id, temp_teacher.user.profile.name) for temp_teacher in
#                                          teacher.get_teacher_not_presidential()]
#     if request.method == "POST" and form_create_class.validate_on_submit():
#         try:
#             # if form_create_class.class_size.data > regulation.get_regulation_by_name("Sĩ số tối đa").max:
#             #     return render_template("create_class.html", form_create_class=form_create_class, list_class=group_class.get_class(),
#             #                student_no_class=student.student_no_class(),mse="Sĩ số lớp không phù hợp")
#             temp_class = group_class.create_class(form_create_class)
#         except Exception as e:
#             redirect("/home")
#         redirect(url_for("index"))
#     return render_template("create_class.html", form_create_class=form_create_class, list_class=group_class.get_class(),
#                            student_no_class=student.student_no_class())


@app.route("/regulations")
@login_required
def view_regulations():
    page = request.args.get('page' , 1 , type=int)
    regulations = dao_regulation.get_regulations(page=page)
    total = dao_regulation.count_regulations()
    return render_template('regulations.html', regulations=regulations , current_page = page ,
                           total_pages=math.ceil(total / app.config["PAGE_SIZE_REGULATIONS"]))


@app.route('/class/edit')
@login_required
@role_only([UserRole.STAFF])
def class_edit():
    page = request.args.get('page', 1 , type=int)
    classes = dao_class.get_class(page =page)
    total = dao_class.count_class()
    return render_template("list_class.html", classes=classes, current_page = page ,
                           total_pages=math.ceil(total / app.config["PAGE_SIZE_DETAIL_CLASS"])
                           )


# Edit class
@app.route('/class/<string:name>/<int:grade>/info')
@login_required
@role_only([UserRole.STAFF])
def info_class(name, grade):
    class_info = dao_class.get_info_class_by_name(name)
    student_no_classes = dao_student.student_no_class("KHOI" + str(grade))
    return render_template("class_info.html", class_info=class_info, student_no_class=student_no_classes)

#Thêm điểm
@app.route("/grade")
@login_required
@role_only([UserRole.TEACHER])
def input_grade():
    profile = dao_authen.get_info_by_id(current_user.id)
    # Fix lại chổ id vào
    return render_template("input_score.html", teaching =dao_teacher.get_teaching_of_teacher(current_user.id) )




@app.route("/grade/input/<teach_plan_id>/score")
@login_required
@role_only([UserRole.TEACHER])
def input_grade_subject(teach_plan_id):
    teach_plan = dao_teacher.get_teaching_by_id(teach_plan_id)
    return render_template("input_score_subject.html", can_edit=dao_teacher.can_edit_exam, get_score=dao_teacher.get_score_by_student_id,teach_plan=teach_plan)
if __name__ == '__main__':
    app.run(debug=True)  # Lên pythonanywhere nhớ để Falsse
