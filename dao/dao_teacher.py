from app.models import Teaching, Class, User, Exam, Score, UserRole
from app.utils import get_current_year
from app import db
from app.dao import dao_class , dao_semester

def get_teaching_of_teacher(teacher_id):
    teaching = db.session.query(Teaching).join(Class).filter(Teaching.teacher_id==teacher_id).filter(Class.year==get_current_year())
    return  teaching.all()
def get_teacher_name(teacher_id):
    teacher_obj = User.query.get(teacher_id)
    return teacher_obj.profile.name if teacher_obj and teacher_obj.profile else "Chưa áp dụng"

def get_teaching_by_id(teach_id):
    return Teaching.query.get(teach_id)
def can_edit_exam(student_id, teach_plan_id):
    e = db.session.query(Exam).filter(Exam.student_id == student_id).filter(teach_plan_id == teach_plan_id).first()
    if e:
        return True
    return False


def get_score_by_student_id(teach_plan_id,student_id, type,count):
    return db.session.query(Score).join(Exam).filter(Exam.teach_plan_id == teach_plan_id)\
                                                .filter(Exam.student_id == student_id)\
                                                .filter(Score.type == type)\
                                                .filter(Score.count == count).first()