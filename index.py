from app import  app , login
from flask_login import current_user
from app.dao import dao_authen ,dao_semester
from app import utils
from app import controllers


# Index là home
# Hàm này luôn truyền các info vào
@app.context_processor
def common_attr():
    if current_user.is_authenticated:
        profile = dao_authen.get_info_by_id(current_user.id)
        user = dao_authen.load_user(current_user.id)
        semester_name, year = utils.get_current_semester()
        semester = dao_semester.get_or_create_semester(semester_name, year)
        current_year = utils.get_current_year()
        list_semester = dao_semester.get_all_semester()
        return {'profile': profile,
                'user': user,
                'semester_name':semester.semester_name,
                'year':semester.year,
                'current_year':current_year,
                'list_semester':list_semester}
    return {}
# Tải người dùng lên
@login.user_loader
def user_load(user_id):
    return dao_authen.load_user(user_id)

app.add_url_rule("/" , 'index' , controllers.index)
app.add_url_rule("/home",'home', controllers.home)
app.add_url_rule("/login",'login' ,controllers.login ,methods=['GET', 'POST'])
app.add_url_rule("/logout",'logout_my_user',controllers.logout_my_user , methods=['get'])
app.add_url_rule("/student/register",'register',controllers.register,  methods=['GET', 'POST'])
app.add_url_rule("/acc_info","info_acc",controllers.info_acc,methods=['GET', 'POST'])
app.add_url_rule("/regulations","view_regulations",controllers.view_regulations)
app.add_url_rule("/class/edit","class_edit",controllers.class_edit)
app.add_url_rule("/class/<string:name>/<int:grade>/info","info_class",controllers.info_class)
app.add_url_rule("/grade","input_grade",controllers.input_grade)
app.add_url_rule("/grade/input/<teach_plan_id>/score","input_grade_subject",controllers.input_grade_subject)
app.add_url_rule("/view_score","view_score",controllers.view_score,methods=['GET','POST'])
app.add_url_rule("/teacher/assignment","teacher_assignment",controllers.teacher_assignment,  methods=['GET', 'POST'])
app.add_url_rule("/api/class/","get_class" ,controllers.get_class , methods=['GET'])
app.add_url_rule("/teacher/assignment/<grade>/<string:classname>","teacher_assignment_class",controllers.teacher_assignment_class ,methods=['GET', 'POST', 'DELETE'])





if __name__ == '__main__':
    app.run(debug=True)  # Lên pythonanywhere nhớ để Falsse