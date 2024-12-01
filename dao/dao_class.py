from app.models import Class ,Teacher ,Students_Classes
from app import db , utils
from app.dao import  dao_student


def get_class():
    return db.session.query(Class).join(Teacher).filter(Class.year.__eq__(utils.get_current_year())).all()
def count_class(grade):
    return Class.query.filter(Class.year.__eq__(utils.get_current_year())).filter(Class.grade.__eq__(grade)).count
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




