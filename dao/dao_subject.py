from app import db ,app
from app.models import Score, Profile, Student, TYPEEXAM, Exam, Teaching, Students_Classes, Class, Semester, Subject
from sqlalchemy import func, case
from app.utils import  get_current_year
from sqlalchemy.sql import text

def get_subject_by_id(subject_id):
    return Subject.query.get(subject_id)

def get_all_subject():
    return Subject.query.all()

def get_avg_score_by_class(semester_id,s_id):
    student_dtb = db.session.query(Student.id.label("id"), (func.sum(case((Score.type == "EXAM_15P", Score.score * 1),(Score.type == "EXAM_45P", Score.score * 2),(Score.type == "EXAM_final", Score.score * 3))) /
                                                                       func.sum(case((Score.type == "EXAM_15P", 1),(Score.type == "EXAM_45P", 2),(Score.type == "EXAM_final", 3)))).label('diem_trung_binh')). \
                            join(Exam, Student.id == Exam.student_id).join(Score).join(Teaching).filter(Teaching.subject_id == s_id).filter(Teaching.semester_id ==semester_id).group_by(Student.id).subquery()

    query_result = db.session.query(Students_Classes.class_id, func.avg(student_dtb.c.diem_trung_binh)). \
                                    join(student_dtb, student_dtb.c.id == Students_Classes.student_id). \
             group_by(Students_Classes.class_id).all()
    return query_result


def get_result_by_class(semester_id, s_id):
    student_dtb = db.session.query(Student.id.label("id"), (func.sum(
        case((Score.type == "EXAM_15P", Score.score * 1), (Score.type == "EXAM_45P", Score.score * 2),
             (Score.type == "EXAM_final", Score.score * 3))) /
                                                            func.sum(case((Score.type == "EXAM_15P", 1),
                                                                          (Score.type == "EXAM_45P", 2),
                                                                          (Score.type == "EXAM_final", 3)))).label(
        'diem_trung_binh')). \
        join(Exam, Student.id == Exam.student_id).join(Score).join(Teaching).filter(
        Teaching.subject_id == s_id).filter(Teaching.semester_id == semester_id).group_by(
        Student.id).subquery()
    student_dtb_final = db.session.query(student_dtb, case((student_dtb.c.diem_trung_binh >= 5, "Đậu"), (student_dtb.c.diem_trung_binh < 5, "Rớt")).label("ket_qua")).subquery()
    query_result = db.session.query(Students_Classes.class_id,func.count(Students_Classes.class_id),
                                    func.count(case((student_dtb_final.c.ket_qua == "Đậu", 1)))). \
        join(student_dtb_final, student_dtb_final.c.id == Students_Classes.student_id). \
        group_by(Students_Classes.class_id).all()
    return query_result


def top_5_highest_score_by_subject(semester_id,s_id):
    student_dtb = db.session.query(Student.id.label("id"), (func.sum(
        case((Score.type == "EXAM_15P", Score.score * 1), (Score.type == "EXAM_45P", Score.score * 2),
             (Score.type == "EXAM_final", Score.score * 3))) /
                                                            func.sum(case((Score.type == "EXAM_15P", 1),
                                                                          (Score.type == "EXAM_45P", 2),
                                                                          (Score.type == "EXAM_final", 3)))).label(
        'diem_trung_binh')). \
        join(Exam, Student.id == Exam.student_id).join(Score).join(Teaching).filter(
        Teaching.subject_id == s_id).filter(Teaching.semester_id == semester_id).group_by(
        Student.id).order_by(text("diem_trung_binh desc")).limit(5).subquery()
    query_result = db.session.query(Profile.name, student_dtb.c.diem_trung_binh).join(student_dtb, student_dtb.c.id == Profile.id).all()
    return query_result


def num_of_classification(semester_id,s_id):
    student_dtb = db.session.query(Student.id.label("id"), (func.sum(
        case((Score.type == "EXAM_15P", Score.score * 1), (Score.type == "EXAM_45P", Score.score * 2),
             (Score.type == "EXAM_final", Score.score * 3))) /
                                                            func.sum(case((Score.type == "EXAM_15P", 1),
                                                                          (Score.type == "EXAM_45P", 2),
                                                                          (Score.type == "EXAM_final", 3)))).label(
        'diem_trung_binh')). \
        join(Exam, Student.id == Exam.student_id).join(Score).join(Teaching).filter(
        Teaching.subject_id == s_id).filter(Teaching.semester_id == semester_id).group_by(
        Student.id).subquery()
    query_result = db.session.query(func.sum(case((student_dtb.c.diem_trung_binh >= 8, 1))),
                                    func.sum(case((student_dtb.c.diem_trung_binh.between(6.5, 7.9444444), 1))),
                                    func.sum(case((student_dtb.c.diem_trung_binh.between(5, 6.444444), 1))),
                                    func.sum(case((student_dtb.c.diem_trung_binh < 5, 1)))).all()
    return query_result
def avg_score_student(semester_id, class_id, subject_id):
    avg_scores = db.session.query(
        Student.id,
        Profile.name,
        func.sum(case(
            (Score.type == TYPEEXAM.EXAM_15P, Score.score * 1),
            (Score.type == TYPEEXAM.EXAM_45P, Score.score * 2),
            (Score.type == TYPEEXAM.EXAM_final, Score.score * 3),
        )) / func.sum(case(
            (Score.type == TYPEEXAM.EXAM_15P, 1),
            (Score.type == TYPEEXAM.EXAM_45P, 2),
            (Score.type == TYPEEXAM.EXAM_final, 3),
        )).label('avg_score')
    ).join(Exam, Score.Exam_id == Exam.id
    ).join(Teaching, Exam.teach_plan_id == Teaching.id
    ).join(Students_Classes, Exam.student_id == Students_Classes.student_id
    ).join(Student, Students_Classes.student_id == Student.id
    ).join(Profile, Student.profile_id == Profile.id
    ).filter(
        Students_Classes.class_id == class_id,
        Teaching.subject_id==subject_id,
        Teaching.semester_id == semester_id,
        Class.year == get_current_year()
    ).group_by(Student.id, Profile.name).all()

    return avg_scores