import math
from app.admin import *
from app import dao, login, app ,utils
from flask import render_template, redirect, request, flash, url_for, jsonify ,  session
from flask_login import current_user, login_required, logout_user, login_user
from app.dao import dao_authen, dao_student, dao_regulation, dao_class , dao_notification , dao_semester , dao_teacher ,dao_assignment
from app.dao.dao_authen import display_profile_data, update_acc_info, auth_user
from app.dao.dao_regulation import get_regulation_by_type
from app.models import UserRole, TYPE_REGULATION  # Phải ghi là app.models để tránh lỗi profile
from app.utils import get_current_semester
from form import AdmisionStudent, LoginForm, Info_Account, ChangeClass
from decorators import role_only
from datetime import datetime
import cloudinary.uploader
#Đưa api vào
from app.api.student_class import *
from app.api.student_score import *
from app.api.teach import  *


# Index là home
# Hàm này luôn truyền các info vào
@app.context_processor
def common_attr():
    if current_user.is_authenticated:
        profile = dao_authen.get_info_by_id(current_user.id)
        user = dao_authen.load_user(current_user.id)
        semester_name, year = get_current_semester()
        semester = dao_semester.get_or_create_semester(semester_name, year)
        current_year = utils.get_current_year()
        return {'profile': profile,
                'user': user,
                'semester_name':semester.semester_name,
                'year':semester.year,
                'current_year':current_year}
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




@app.route("/regulations")
@login_required
def view_regulations():
    page = request.args.get('page' , 1 , type=int)
    regulations = dao_regulation.get_regulations(page=page)
    total = dao_regulation.count_regulations()
    return render_template('regulations.html', regulations=regulations , current_page = page ,
                           total_pages=math.ceil(total / app.config["PAGE_SIZE_REGULATIONS"]))

#List-class
@app.route('/class/edit')
@login_required
@role_only([UserRole.STAFF])
def class_edit():
    page = request.args.get('page', 1 , type=int)
    classes = dao_class.get_class(page =page)
    total = dao_class.count_class()
    return render_template("list_class.html", classes=classes, current_page = page ,
                           total_pages=math.ceil(total / app.config["PAGE_SIZE_LIST_CLASS"])
                           )


# Edit class
@app.route('/class/<string:name>/<int:grade>/info')
@login_required
@role_only([UserRole.STAFF])
def info_class(name, grade):
    page = request.args.get('page', 1, type=int)
    students, class_info, total_students = dao_class.get_info_class_by_name(name, page=page)
    # print(total_students)
    total_pages = math.ceil(total_students / app.config["PAGE_SIZE_DETAIL_CLASS"])

    student_no_classes = dao_student.student_no_class("KHOI" + str(grade))

    return render_template(
        "class_info.html",
        class_info=class_info,
        student_no_class=student_no_classes,
        current_page=page,
        total_pages=total_pages,
        students=students
    )


#Thêm điểm
@app.route("/grade")
@login_required
@role_only([UserRole.TEACHER])
def input_grade():

    teaching = dao_teacher.get_teaching_of_teacher(current_user.id)
    return render_template("input_score.html", teaching = teaching )




@app.route("/grade/input/<teach_plan_id>/score")
@login_required
@role_only([UserRole.TEACHER])
def input_grade_subject(teach_plan_id):
    teach_plan = dao_teacher.get_teaching_by_id(teach_plan_id)
    current_year = utils.get_current_year()
    return render_template("input_score_subject.html", can_edit=dao_teacher.can_edit_exam, get_score=dao_teacher.get_score_by_student_id,teach_plan=teach_plan, current_year=current_year)

@app.route("/view_score", methods=['GET','POST'])
def view_score():
    semester = dao_semester.get_all_semester()
    return  render_template("view_score.html", semester=semester)

#Phan cong Teaching
@app.route('/teacher/assignment', methods=['GET', 'POST'])
@login_required
@role_only([UserRole.STAFF])
def teacher_assignment():
    classname = ''
    if request.method == "POST":
        classname = request.form.get("class-list")
        grade_value = request.form.get("grade-list")

        # Kiểm tra nếu thiếu giá trị
        if not classname or not grade_value:
            flash("Bạn phải chọn cả khối và lớp trước khi tìm kiếm.", "error")
            return redirect(request.referrer or '/teacher/assignment')  # Quay lại trang hiện tại hoặc trang assignment

        # Chuyển hướng nếu có đủ dữ liệu
        return redirect(f'/teacher/assignment/{grade_value}/{classname}')

    return render_template("teacher_assignment.html", classname=classname)


@app.route('/api/class/', methods=['GET'])
@role_only([UserRole.STAFF])
def get_class():
    q = request.args.get('q')
    res = {}
    if q:
        class_list = dao_assignment.load_class_by_grade(q)
        json_class_list = [
            {
                "grade": c.grade.value,
                "name": c.name,
            }
            for c in class_list
        ]
        return jsonify({"class_list": json_class_list})
    return jsonify({})
@app.route('/teacher/assignment/<grade>/<string:classname>', methods=['GET', 'POST', 'DELETE'])
@login_required
@role_only([UserRole.STAFF])
def teacher_assignment_class(grade, classname):
    subject_list = dao_assignment.load_subject_of_class(grade='KHOI' + grade)
    if not subject_list:
        flash("Không tìm thấy danh sách môn học cho khối này!", "error")
        return redirect("/teacher/assignment")  # Điều hướng về trang chính nếu lỗi

    class_info = dao_class.get_class_by_name(name=classname)
    if not class_info:
        flash("Không tìm thấy lớp học này!", "error")
        return redirect("/teacher/assignment")

    class_id = class_info.id
    teachers = dao_teacher.get_all_teacher()
    if not teachers:
        flash("Không tìm thấy danh sách giáo viên!", "error")
        return redirect("/teacher/assignment")

    if request.method == "GET":
        plan = dao_assignment.load_assignments_of_class(class_id=class_id)
        if plan is None:
            flash("Không có kế hoạch phân công cho lớp này!", "info")
        return render_template("teacher_assignment.html", grade=grade, classname=classname, subjects=subject_list,
                               get_teachers=teachers, plan=plan)

    elif request.method == "POST" and request.form.get("type") == "save":
        try:
            for s in subject_list:
                teacher_id = request.form.get(f"teacher-assigned-{s.id}")
                if not teacher_id:
                    continue  # Bỏ qua nếu không chọn giáo viên cho môn học

                teacher_subject = dao_assignment.get_id_teacher_subject(teacher_id=teacher_id, subject_id=s.id)
                semester_id = None
                if request.form.get(f"total-seme-{s.id}"):
                    semester_id = "1,2"  # Cả 2 kỳ
                elif request.form.get(f"seme1-{s.id}"):
                    semester_id = "1"  # Kỳ 1
                elif request.form.get(f"seme2-{s.id}"):
                    semester_id = "2"  # Kỳ 2

                if teacher_subject is None:
                    # Tạo mới nếu chưa có bản ghi
                    new_teacher_subject = Teaching(
                        teacher_id=teacher_id,
                        subject_id=s.id,
                        semester_id=semester_id,
                        class_id=class_id
                    )
                    db.session.add(new_teacher_subject)
                else:
                    # Cập nhật nếu đã có bản ghi
                    teacher_subject.semester_id = semester_id

            db.session.commit()
            flash("Phân công giảng dạy thành công!", "success")
        except Exception as e:
            flash(f"Lỗi khi lưu phân công: ", "error")
        return redirect(f"/teacher/assignment/{grade}/{classname}")

    elif request.method == "POST" and request.form.get("type") == "delete":
        try:
            dao_assignment.delete_assignments(class_id)
            flash("Đã xóa phân công giảng dạy thành công!", "success")
        except Exception as e:
            flash(f"Lỗi khi xóa phân công:", "error")
        return redirect(f"/teacher/assignment/{grade}/{classname}")

    flash("Có lỗi xảy ra, vui lòng thử lại!", "error")
    return render_template("teacher_assignment.html", grade=grade, classname=classname, subjects=subject_list,
                           get_teachers=teachers)

if __name__ == '__main__':
    app.run(debug=True)  # Lên pythonanywhere nhớ để Falsse