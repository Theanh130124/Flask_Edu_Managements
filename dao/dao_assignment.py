from app.models import Class, Subject, Semester, Teaching, User, UserRole
from app import db
from datetime import date , datetime



#Phân công
def load_class_by_grade(grade):
    return Class.query.filter_by(grade=grade)

def load_subject_of_class(grade):
    return Subject.query.filter_by(grade=grade)


def load_all_teacher_subject(subject_id):
    return User.query.join(Teaching).filter(Teaching.subject_id == subject_id).all()


def get_semester(semester_id):
    return db.session.get(Semester, semester_id)

def load_assignments_of_class(class_id):
    return Teaching.query.filter_by(class_id=class_id)

def get_id_teacher_subject(teacher_id, subject_id):
    return Teaching.query.filter_by(teacher_id=teacher_id, subject_id=subject_id).first()


def save_subject_assignment(class_id, semester_id, teacher_subject_id):
    if isinstance(semester_id, int):
        plan, created = get_or_create(class_id=class_id, semester_id=semester_id, teacher_subject_id=teacher_subject_id)
        if created:
            plan.class_id = class_id
            plan.semester_id = semester_id
            plan.teacher_subject_id = teacher_subject_id
            db.session.commit()
        another = Teaching.query.filter_by(class_id=class_id, semester_id=3 - semester_id,
                                                teacher_subject_id=teacher_subject_id).first()
        if another:
            db.session.delete(another)
            db.session.commit()

    else:
        for s in semester_id:
            plan, created = get_or_create(class_id=class_id, semester_id=s, teacher_subject_id=teacher_subject_id)
            if created:
                plan.class_id = class_id
                plan.semester_id = s
                plan.teacher_subject_id=teacher_subject_id
                db.session.commit()



def get_or_create(class_id, semester_id, teacher_subject_id):
    plan = Teaching.query.filter_by(class_id=class_id, semester_id=semester_id, teacher_subject_id=teacher_subject_id).first()
    if plan:
        return plan, True
    else:
        score_dl = None
        if semester_id == 1:
            score_dl = datetime(year=date.today().year - 1, month=12, day=31)
        else:
            score_dl = datetime(year=date.today().year, month=6, day=29)

        create_plan = Teaching(
            class_id=class_id,
            semester_id=semester_id,
            teacher_subject_id=teacher_subject_id,
            score_deadline=score_dl
        )

        db.session.add(create_plan)
        db.session.commit()
        return create_plan, False



def delete_assignments(class_id):
    plans = Teaching.query.filter_by(class_id=class_id)
    for plan in plans:
        db.session.delete(plan)
        db.session.commit()