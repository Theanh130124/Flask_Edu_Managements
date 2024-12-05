from app.models import Class ,Teacher ,Students_Classes
from app import db , utils , app
from app.dao import  dao_student


def get_class(page =1):
    classes = db.session.query(Class).join(Teacher).filter(Class.year.__eq__(utils.get_current_year()))
    page_size = app.config['PAGE_SIZE_DETAIL_CLASS']
    start = (page -1) * page_size
    classes = classes.slice(start , start + page_size)
    return classes.all()
# Kiểm tra xem có viết trùng tên cái dưới đc không
def count_class_not_grade(grade=None):
    query = db.session.query(Class).join(Teacher).filter(Class.year == utils.get_current_year())
    if grade is not None:
        query = query.filter(Class.grade != grade)
    return query.count()


def count_class(grade=None):
    query = Class.query.filter(Class.year == utils.get_current_year())
    if grade is not None:
        query = query.filter(Class.grade == grade)
    return query.count()
def create_class(form):
    new_class = Class(grade=form.grade.data,
                      year=utils.get_current_year(),
                      count=count_class(form.grade.data)+1,
                      teacher_id=form.teacher.data)
    db.session.add(new_class)
    db.session.commit()
    temp_student = dao_student.get_list_student_no_class_by_grade(form.class_size.data,form.grade.data)
    for s in temp_student:
        student_class = Students_Classes(student_id=s.id,class_id=new_class.id)
        db.session.add(student_class)
        db.session.commit()

def get_info_class_by_name(name):
    return db.session.query(Class).filter(Class.name == name, Class.year == utils.get_current_year()).first()




