from datetime import datetime
from flask_login import UserMixin
from app import db, app
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey , Enum,  DateTime ,  CheckConstraint
from sqlalchemy.orm import relationship, backref
import enum

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
class UserRole(enum.Enum):
    ADMIN =1
    TEACHER =2
    STAFF = 3
class GRADE(enum.Enum):
    KHOI10 = 10
    KHOI11 = 11
    KHOI12 = 12
class TYPEEXAM(enum.Enum):
    EXAM_15P = 1
    EXAM_45P = 2
    EXAM_final = 3
#Profile này áp dụng cho học sinh -> sửa đổi các id lại thành int , Xem xét lại các nullable
class Profile(BaseModel):
    name = Column(String(50), nullable=False)
    email =Column(String(50), unique=True, nullable=False)
    birthday = Column(DateTime , nullable=False)
    gender =Column(Boolean)
    address = Column(Text , nullable=False)
    # Gàn buộc sđt
    phone = Column(String(10), unique=True , nullable=False)
#1-1
class User(UserMixin,Profile):
    id = Column(Integer, ForeignKey(Profile.id), primary_key=True, nullable=False, unique=True)
    username = Column(String(50), unique=True , nullable=False)
    password = Column(String(50), nullable=False)
    user_role =Column(Enum(UserRole))
    active = Column(Boolean , default=True)
    avatar = Column(String(100), nullable=False)
    profile = relationship("Profile", backref="user", lazy=True , uselist=False)

#1-1(với user) ,n-n(với class)
#Phải vẽ kế thừa ->


class Subject(BaseModel):
    name = Column(String(50) ,nullable=False )
    grade = Column(Enum(GRADE) )
    number_of_15p = Column(Integer, nullable=False)
    number_of_45p = Column(Integer,nullable=False)


class Class(BaseModel):
    grade = Column(Enum(GRADE))
    count = Column(Integer , nullable=True)
    amount = Column(Integer, default=0)
    # year = Column(Integer, default=datetime.now().year) -> để biết lớp 10 năm nào
    teacher_id = Column(Integer, ForeignKey(User.id))
    students = relationship("Students_Classes", backref="class", lazy=True)
    regulation_id = Column(Integer, ForeignKey('regulation.id'), nullable=False)

class Student(db.Model):
    id = Column(Integer, ForeignKey(Profile.id), primary_key=True, unique=True) #Cái mã học sinh chỉ được tạo 1 lần
    grade = Column(Enum(GRADE), default=GRADE.KHOI10)
    classes = relationship("Students_Classes", backref="student", lazy=True)
    profile = relationship("Profile", backref="student", lazy=True)
    regulation_id = Column(Integer, ForeignKey('regulation.id'), nullable=False)

class Students_Classes(BaseModel):
    class_id = Column(Integer, ForeignKey(Class.id), nullable=False)
    student_id = Column(Integer, ForeignKey(Student.id), nullable=False)


class Teachers_Subject(BaseModel):
    teacher_id = Column(Integer, ForeignKey(User.id), nullable=False)
    subject_id = Column(Integer, ForeignKey(Subject.id), nullable=False)

    teacher = relationship("Teacher", backref="teachers_subject", lazy=True)
    subject = relationship("Subject", backref="subject_teacher", lazy=True)

class Semester(BaseModel):
    semester_name = Column(String(50) , nullable=False)
    year = Column(Integer , default=datetime.now().year)

class Teaching_plan(BaseModel):
    score_deadline = Column(DateTime ,nullable=False)
    class_id = Column(Integer, ForeignKey(Class.id), nullable=False)
    semester_id = Column(Integer, ForeignKey(Semester.id), nullable=False)
    teacher_subject_id = Column(Integer, ForeignKey(Teachers_Subject.id), nullable=False)
    teacher_subject = relationship("Teachers_Subject", backref="teaching_plan")
    # subject_id = Column(Integer, ForeignKey(Subject.id), nullable=False)
    # teacher_id = Column(Integer, ForeignKey(Teacher.id), nullable=False)
    # teacher = relationship("Teacher", backref="teacher", lazy=True)
    semester = relationship("Semester", backref="semester", lazy=True)
    class_teach = relationship("Class", backref="teach", lazy=True)
    # subject = relationship("Subject", backref="subject", lazy=True)
#Bang diem
class Exam(BaseModel):
    student_id = Column(Integer, ForeignKey(Student.id), nullable=False)
    teach_plan_id = Column(Integer, ForeignKey(Teaching_plan.id), nullable=False)
    scores = relationship("Score", backref="exam", lazy=True)

    student = relationship("Student", backref="exam", lazy=True)
    teach_plan = relationship("Teaching_plan", backref="exam", lazy=True)
# diem 15p cuoi kì hoac 45p
class Score(BaseModel):
    score = Column(Float)
    type = Column(Enum(TYPEEXAM))
    count = Column(Integer)
    Exam_id = Column(Integer, ForeignKey(Exam.id), nullable=False)

    __table_args__ = (
        CheckConstraint('score >= 0', name='check_age_min'),
        CheckConstraint('score <= 10', name='check_age_max'),
    )
# #Quy định với Notification
# class Notification(BaseModel):
#     subject = Column(String(200) ,nullable=False)
#     content = Column(Text, nullable=False)
#     created_at = Column(DateTime, default=datetime.now())

class Regulation(BaseModel):
    type = Column(String(50))
    # Quy định tuổi tối đa tối thiểu , sỉ số tối da tôi thiểu
    regulation_name = Column(String(100))
    min_value = Column(Integer,nullable=False)
    max_value = Column(Integer, nullable=False)
    classes = relationship('Class' , backref='regulation', lazy=True)
    students = relationship('Student' , backref='regulation',lazy=True)

if __name__ == "__main__" :
    with app.app_context():
        db.create_all()
