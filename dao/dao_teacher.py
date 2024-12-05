from app.models import Teaching , Class
from app.utils import get_current_year
from app import db

def get_teaching_of_teacher(teacher_id):
    teaching = db.session.query(Teaching).join(Class).filter(Teaching.teacher_id==teacher_id).filter(Class.year==get_current_year())
    return  teaching.all()
