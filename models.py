from datetime import datetime
from flask_login import UserMixin
from app import db, app
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey , Enum,  DateTime ,  CheckConstraint
from sqlalchemy.orm import relationship
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
class TYPE_REGULATION(enum.Enum):
    RE_AGE =1
    RE_AMOUNT =2

class Profile(BaseModel):
    name = Column(String(50), nullable=False)
    email =Column(String(50), unique=True, nullable=False)
    birthday = Column(DateTime , nullable=False)
    gender =Column(Boolean, default=True)
    address = Column(Text , nullable=False)
    phone = Column(String(10), unique=True , nullable=False)
    __table_args__ = (
    CheckConstraint("LENGTH(phone) = 10 AND phone REGEXP '^[0-9]+$'", name="check_phone_format"),)

class User(UserMixin,db.Model):
    id = Column(Integer, ForeignKey(Profile.id), primary_key=True, nullable=False)
    username = Column(String(50), unique=True , nullable=False)
    password = Column(String(50), nullable=False)
    user_role =Column(Enum(UserRole), default=UserRole.STAFF)
    active = Column(Boolean , default=True)
    avatar = Column(String(100), nullable=False) #Có sửa deffault cũng được
    profile_id = relationship("Profile", backref="user", lazy=True , uselist=False)

class Subject(BaseModel):
    name = Column(String(50) ,nullable=False )
    grade = Column(Enum(GRADE) , default=GRADE.KHOI10)
    number_of_15p = Column(Integer, nullable=False)
    number_of_45p = Column(Integer,nullable=False)
    teachings = relationship('Teaching', backref='subject', lazy=True)

    __table_args__ = (
    CheckConstraint("number_of_15p >= 0", name="check_number_of_15p"),
    CheckConstraint("number_of_45p >= 0", name="check_number_of_45p"),
)
# class Teacher(db.Model):
#     id = Column(Integer, ForeignKey(User.id), primary_key=True, nullable=False)
#
#     teachings = relationship('Teaching', backref='teacher', lazy=True)
#     user = relationship("User", backref="teacher", lazy=True,  uselist=False)

# User.id phải là của giáo viên
class Class(BaseModel):
    grade = Column(Enum(GRADE))
    name = Column(String(10),nullable=False)
    amount = Column(Integer, default=0)
    year = Column(Integer, default=datetime.now().year)
    teacher_id = Column(Integer, ForeignKey(User.id)) #Giao vien chu nhiem-> nữa nhớ bổ sung dô đường noi so do
    teachings = relationship('Teaching', backref='class' ,lazy=True)
    students = relationship("Students_Classes", backref="class", lazy=True)
    regulation_id = Column(Integer, ForeignKey('regulation.id'), nullable=False)
    __table_args__ = (
    CheckConstraint("amount >= 0", name="check_class_amount"),
    )

class Student(db.Model):
    id = Column(Integer, ForeignKey(Profile.id), primary_key=True)
    grade = Column(Enum(GRADE), default=GRADE.KHOI10)
    classes = relationship("Students_Classes", backref="student", lazy=True)
    profile = relationship("Profile", backref="student", lazy=True,  uselist=False)
    regulation_id = Column(Integer, ForeignKey('regulation.id'), nullable=False)

class Students_Classes(BaseModel):
    class_id = Column(Integer, ForeignKey(Class.id), nullable=False)
    student_id = Column(Integer, ForeignKey(Student.id), nullable=False)


class Semester(BaseModel):
    semester_name = Column(String(50) , nullable=False)
    year = Column(Integer , default=datetime.now().year)
    teachings = relationship('Teaching', backref='semester' ,lazy=True)


class Teaching(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    class_id = Column(Integer, ForeignKey(Class.id), nullable=False)
    semester_id = Column(Integer, ForeignKey(Semester.id), nullable=False)
    subject_id = Column(Integer, ForeignKey(Subject.id), nullable=False)
    teacher_id = Column(Integer, ForeignKey(User.id), nullable=False)
#Score_final
class Score(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    score_final = Column(Float, nullable=False)
    student_id = Column(Integer, ForeignKey("student.id"), nullable=False)
    teach_plan_id = Column(Integer, ForeignKey("teaching.id"), nullable=False)

    student = relationship("Student", backref="score", lazy=True)
    teach_plan = relationship("Teaching", backref="score", lazy=True)
    __table_args__ = (
        CheckConstraint('score_final >= 0', name='check_score_min'),
        CheckConstraint('score_final <= 10', name='check_score_max'),
    )
class Score_of_15p(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    score = Column(Float, nullable=False)
    student_id = Column(Integer, ForeignKey("student.id"), nullable=False)
    teach_plan_id = Column(Integer, ForeignKey("teaching.id"), nullable=False)

    student = relationship("Student", backref="score_of_15p", lazy=True)
    teach_plan = relationship("Teaching", backref="score_of_15p", lazy=True)
    __table_args__ = (
        CheckConstraint('score >= 0', name='check_score_of_15p_min'),
        CheckConstraint('score <= 10', name='check_score_of_15p_max'),
    )

class Score_of_45p(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    score = Column(Float, nullable=False)
    student_id = Column(Integer, ForeignKey("student.id"), nullable=False)
    teach_plan_id = Column(Integer, ForeignKey("teaching.id"), nullable=False)

    student = relationship("Student", backref="score_of_45p", lazy=True)
    teach_plan = relationship("Teaching", backref="score_of_45p", lazy=True)
    __table_args__ = (
        CheckConstraint('score >= 0', name='check_score_of_45p_min'),
        CheckConstraint('score <= 10', name='check_score_of_45p_max'),
    )


# #Quy định với Notification
# class Notification(BaseModel):
#     subject = Column(String(200) ,nullable=False)
#     content = Column(Text, nullable=False)
#     created_at = Column(DateTime, default=datetime.now())

class Regulation(BaseModel):
    type = Column(Enum(TYPE_REGULATION), default=TYPE_REGULATION.RE_AGE)
    name = Column(String(100))
    min_value = Column(Integer,nullable=False)
    max_value = Column(Integer, nullable=False)
    classes = relationship('Class' , backref='regulation', lazy=True)
    students = relationship('Student' , backref='regulation',lazy=True)
    __table_args__ = (
        CheckConstraint("min_value <= max_value", name="check_min_less_equal_max"),
    )

if __name__ == "__main__" :
    with app.app_context():
     db.create_all()


