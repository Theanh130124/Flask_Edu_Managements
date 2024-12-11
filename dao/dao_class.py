from app.models import Class, Students_Classes, User, UserRole , Student
from app import db , utils , app
from app.dao import  dao_student

# Outerjoin để lấy cả class chưa có GVCN
def get_class(page =1):
    classes = (db.session.query(Class).outerjoin(User, Class.teacher_id == User.id)
               .filter(Class.year == utils.get_current_year()))
    page_size = app.config['PAGE_SIZE_LIST_CLASS']
    start = (page -1) * page_size
    classes = classes.slice(start , start + page_size)
    return classes.all()

def get_class_by_id(class_id):
    return  Class.query.get(class_id)

def count_class_not_grade(grade=None):
    query = db.session.query(Class).join(User).filter(Class.year == utils.get_current_year())
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


def get_info_class_by_name(name, page=1):

    class_query = db.session.query(Class).filter(Class.name == name, Class.year == utils.get_current_year())
    class_info = class_query.first()
    if not class_info:
        return None
    students_query = db.session.query(Student).join(Students_Classes).join(Class).filter(
        Class.id == class_info.id
    )

    total_students = students_query.count()

    page_size = app.config['PAGE_SIZE_DETAIL_CLASS']
    start = (page - 1) * page_size
    students_query = students_query.offset(start).limit(page_size)
    students = students_query.all()
    return students, class_info ,total_students

def get_class_by_name(name):
    return db.session.query(Class).filter_by(name=name).first()

def teacher_name(teacher_id):
        teacher = User.query.get(teacher_id)
        if teacher:
            return teacher.profie.name
        return None

