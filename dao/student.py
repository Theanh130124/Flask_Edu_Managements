import json
import random
from app.models import  Student , Students_Classes ,Semester , Profile , Class
from app import db
from app.utils import get_academic_info



#Add info and STUDENT



def get_student_by_id(id):
    return Student.query.get(id)

def check_student_in_class(student_id, class_id):
    return Students_Classes.query.filter(Students_Classes.student_id == student_id).filter(Students_Classes.class_id == class_id).first()


def get_all_semester():
    return Semester.query.all()

def create_student(form):
    profile = Profile(name=form.full_name.data,
                      gender=form.gender.data,
                      birthday=form.birth_date.data,
                      address=form.address.data,
                      phone=form.phone_number.data,
                      email=form.email.data
                      )
    db.session.add(profile)
    db.session.commit()
    student = Student( profile_id=profile.id, regulation_id=1)
    db.session.add(student)
    db.session.commit()
    return student

def verify_student_phone_number(phone_number):
    student_info = db.session.query(Student.id, Profile.name).join(Profile).filter(Profile.phone == phone_number).first()
    if student_info:
        student_info_dict = {'id': student_info[0], 'studentName': student_info[1]}
        return json.dumps(student_info_dict,ensure_ascii=False)
    else:
        return None

# def view_score_student(student_id, semester_id):
#     return (db.session.query(Exam, Subject.name, Score.type, Score.score,Score.count)
#             .join(Teaching_plan, Exam.teach_plan_id == Teaching_plan.id)
#             .join(Score, Exam.id == Score.Exam_id)
#             .join(Teachers_Subject)
#             .join(Subject, Teachers_Subject.subject_id == Subject.id)
#             .filter(Exam.student_id == student_id)
#             .filter(Teaching_plan.semester_id == semester_id).filter(Class.year == get_current_year())
#             .all()
#             )

# def preprocess_scores(scores):
#     subject_scores = {}
#     for exam, name, type, score, count in scores:
#         if name not in subject_scores:
#             subject_scores[name] = {'15_minute': {'scores': [], 'count': 0}, '45_minute': {'scores': [], 'count': 0},
#                                     'final_points': {'scores': [], 'count': 0}}
#
#         if type == TYPEEXAM.EXAM_15P:
#             subject_scores[name]['15_minute']['scores'].append(score)
#         elif type == TYPEEXAM.EXAM_45P:
#             subject_scores[name]['45_minute']['scores'].append(score)
#         elif type == TYPEEXAM.EXAM_final:
#             subject_scores[name]['final_points']['scores'].append(score)
#     return subject_scores

def student_no_class(grade=None):
    student_had_class = db.session.query(Student.id).join(Students_Classes).join(Class).filter(
        Class.year == get_academic_info())
    if grade:
        return db.session.query(Student).filter(Student.id.not_in(student_had_class)).filter(Student.grade == grade).all()
    return db.session.query(Student).filter(Student.id.not_in(student_had_class)).all()

def get_list_student_no_class_by_grade(size,grade):
    student_had_class = db.session.query(Student.id).join(Students_Classes).join(Class).filter(Class.year == get_academic_info())
    non_class_students = db.session.query(Student).filter(Student.id.not_in(student_had_class)).filter(Student.grade == grade).all()
    return random.sample(non_class_students,size)
