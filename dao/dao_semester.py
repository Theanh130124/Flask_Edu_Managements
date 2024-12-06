from app.models import  Semester
from app import db


def get_all_semester():
    return Semester.query.order_by(Semester.id.desc()).all()

def get_or_create_semester(semester_name, year):
    semester = Semester.query.filter_by(semester_name=semester_name, year=year).first()
    if not semester:
        semester = Semester(semester_name=semester_name, year=year)
        db.session.add(semester)
        db.session.commit()
    return semester

