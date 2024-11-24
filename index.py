
from app import dao, login , app
from flask import render_template, redirect,  request , flash
from flask_login import current_user, login_required, logout_user, login_user
from app.models import UserRole #Phải ghi là app.models để tránh lỗi profile
from form import AdmisionStudent
from decorators import role_only
from dao import create_student


#Index là home





# Tải người dùng lên

@login.user_loader
def user_load(user_id):
    return dao.load_user(user_id)

@app.route('/')
def index():
    return redirect('/login')

@app.route('/home')
@login_required #Có cái này để gom user vào -> home
def home():
    profile = dao.get_info_by_id(current_user.id)
    return render_template('index.html',  profile=profile)  # Trang home (index.html)


@app.route('/login', methods=['GET', 'POST'])
def login_my_user():
        err_msg = ''
        if request.method.__eq__('POST'):
            username = request.form.get('username')
            password = request.form.get('password')
            # Truyền cả profile và user của người đó vào
            user = dao.auth_user(username=username, password=password)
            if user:
                login_user(user)
                return redirect('/home' )
            else:
                flash('Thông tin đăng nhập không hợp lệ', 'danger')


        return render_template('login.html', err_msg=err_msg)

@app.route('/logout', methods=['get'])
def logout_my_user():
    logout_user()
    return redirect('/login')


# import pdb
# pdb.set_trace()

#FIX ROLE_ONLY -> VÀ CÁI PROFILE PHẢI TRUYỀN VÀO LẠI




@app.route('/student/register', methods=['GET', 'POST'])
@login_required
@role_only([UserRole.STAFF])
def register():
    form_student = AdmisionStudent()
    profile = dao.get_info_by_id(current_user.id)

    if request.method == "POST" and form_student.submit():
        try:
            s = dao.create_student(form_student)
        except Exception as e:
            print(e)
            # min = regulation.get_regulation_by_name("Tiếp nhận học sinh").min
            # if (datetime.now().year - form_student.birth_date.data.year) < min:
            #     return render_template("register_student.html", form_student=form_student,mse="Tuổi không phù hợp")

            # send_mail(subject="Thông báo nhập học ", student_name=s.profile.name, recipients=[s.profile.email])
            flash("Đã xảy ra lỗi khi tạo học sinh", "error")  # Thêm thông báo lỗi
            return render_template("register_student.html", form_student=form_student, profile=profile)
        if s:
            flash("Tạo học sinh thành công!", "success")  # Thông báo thành công
            return redirect("/index")
    return render_template("register_student.html", form_student=form_student, profile=profile)

if __name__ == '__main__':
    app.run(debug=True) #Lên pythonanywhere nhớ để Falsse