from app.admin import *
from app import dao, login, app
from flask import render_template, redirect, request, flash, url_for, jsonify
from flask_login import current_user, login_required, logout_user, login_user
from app.dao import authen, student
from app.dao.authen import display_profile_data, update_acc_info
from app.dao.regulation import get_regulation_by_name
from app.models import UserRole  # Phải ghi là app.models để tránh lỗi profile
from form import AdmisionStudent, LoginForm, Info_Account, ChangeClass
from decorators import role_only
from datetime import datetime
import cloudinary.uploader


# Index là home
# Hàm này luôn truyền vào
@app.context_processor
def common_attr():
    if current_user.is_authenticated:
        profile = authen.get_info_by_id(current_user.id)
        user = authen.load_user(current_user.id)
        return {'profile': profile,
                'user': user}
    return {}


# Tải người dùng lên

@login.user_loader
def user_load(user_id):
    return authen.load_user(user_id)


# import pdb
# pdb.set_trace()
@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.user_role == UserRole.ADMIN:
            return redirect("/admin")
        return redirect("/home")
    return redirect('/login')


# Nếu truyền url_for sẽ vào index -> truyêền redirect thì vào router
@app.route('/home')
@login_required  # Có cái này để gom user vào -> home
@role_only([UserRole.STAFF, UserRole.TEACHER])
def home():
    return render_template('index.html', )  # Trang home (index.html)


@app.route('/login', methods=['GET', 'POST'])
def login():
    mse = ""
    form = LoginForm()
    if request.method == "POST" and form.SubmitFieldLogin():
        username = form.username.data
        password = form.password.data
        user = authen.auth_user(username=username, password=password)
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

# FIX ROLE_ONLY -> VÀ CÁI PROFILE PHẢI TRUYỀN VÀO LẠI




from flask import session


@app.route('/student/register', methods=['GET', 'POST'])
@login_required
@role_only([UserRole.STAFF])
def register():
    form_student = AdmisionStudent()

    # Lấy quy định độ tuổi từ regulation
    regulation = get_regulation_by_name("Tiếp nhận học sinh")
    min_age = regulation.min_value  # độ tuổi tối thiểu
    max_age = regulation.max_value  # độ tuổi tối đa

    if request.method == "POST":
        # Kiểm tra các trường hợp không hợp lệ trong form
        if form_student.validate_on_submit():
            try:
                # Tính toán tuổi học sinh
                birth_date = form_student.birth_date.data
                current_year = datetime.now().year
                age = current_year - birth_date.year

                # Kiểm tra độ tuổi của học sinh
                if age < min_age or age > max_age:
                    flash(f"Độ tuổi phải từ {min_age} đến {max_age}!", "danger")
                    return redirect(url_for("register"))

                # Nếu độ tuổi hợp lệ, tạo học sinh
                student.create_student(form_student)
                flash("Tạo học sinh thành công!", "success")
                return redirect(url_for("register"))
            except Exception as e:
                flash(f"Đã xảy ra lỗi khi tạo học sinh: {e}", "danger")
                return render_template("register_student.html", form_student=form_student)
        else:
            for field, errors in form_student.errors.items():
                for error in errors:
                    flash(error, "danger")

            return render_template("register_student.html", form_student=form_student)

    return render_template("register_student.html", form_student=form_student)


# import pdb
# pdb.set_trace()
@app.route('/acc_info', methods=['GET', 'POST'])
@login_required
@role_only([UserRole.STAFF, UserRole.TEACHER])
def info_acc():
    form_account = Info_Account()
    profile = authen.get_info_by_id(current_user.id)

    if form_account.validate_on_submit():
        try:
            update_acc_info(form_account)
            db.session.refresh(current_user)
            flash('Thông tin tài khoản đã được cập nhật', 'success')  # Flash thông báo thành công
            return redirect('/acc_info')  # Điều hướng lại sau khi cập nhật thành công
        except Exception as e:
            flash(f'Cập nhật không thành công. Lỗi: {str(e)}', 'danger')  # Flash thông báo lỗi

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


if __name__ == '__main__':
    app.run(debug=True)  # Lên pythonanywhere nhớ để Falsse
