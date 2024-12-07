from datetime import datetime , date


from flask_login import UserMixin
from sqlalchemy.dialects.mssql.information_schema import views

from app import db, app
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey, Enum, DateTime, CheckConstraint
from sqlalchemy.orm import relationship, backref
import enum
import hashlib



class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)



class UserRole(enum.Enum):
    ADMIN = 1
    TEACHER = 2
    STAFF = 3


class GRADE(enum.Enum):
    KHOI10 = 10
    KHOI11 = 11
    KHOI12 = 12



class TYPE_REGULATION(enum.Enum):
    RE_AGE = "Quy_Dinh_Tuoi"
    RE_AMOUNT = "Quy_Dinh_SiSo"


class GENDER(enum.Enum):
    Nam = 'Nam'
    Nu = 'Nữ'

class TYPEEXAM(enum.Enum):
    EXAM_15P = 1
    EXAM_45P = 2
    EXAM_final = 3

class Profile(BaseModel):
    name = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    birthday = Column(db.Date ,nullable=False)
    gender = Column(Enum(GENDER), default=GENDER.Nam)
    address = Column(Text, nullable=False)
    phone = Column(String(10), unique=True, nullable=False)
    # Các trường ràng buộc khi admin nhập liệu dưới CSDL
    __table_args__ = (
        CheckConstraint("LENGTH(phone) = 10 AND phone REGEXP '^[0-9]+$'", name="check_phone_format"),
    )
    def __str__(self):
        return self.name

    @property
    def teacher_name(self):
        return self.teacher.username if self.teacher else "Chưa có giáo viên"


class User(UserMixin, BaseModel):
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    user_role = Column(Enum(UserRole), default=UserRole.STAFF)
    active = Column(Boolean, default=True)
    avatar = Column(String(255), default="https://res.cloudinary.com/dxiawzgnz/image/upload/v1732632586/pfvvxablnkaeqmmbqeit.png")
    profile_id = Column(Integer, ForeignKey("profile.id"), unique=True, nullable=False)
    profile = relationship("Profile", backref="user", lazy=True, uselist=False)

#Của GVCN
    class_teach = relationship("Class", backref="teacher", lazy=True)
    notifications = relationship('Notification', backref="user", lazy=True)

    def __str__(self):
        return self.username





class Subject(BaseModel):
    name = Column(String(50), nullable=False)
    grade = Column(Enum(GRADE), default=GRADE.KHOI10)
    number_of_15p = Column(Integer, nullable=False)
    number_of_45p = Column(Integer, nullable=False)
    # teachings = relationship('Teaching', backref='subject', lazy=True)

    __table_args__ = (
        CheckConstraint("number_of_15p >= 0 AND number_of_15p <=5", name="check_number_of_15p"),
        CheckConstraint("number_of_45p >= 0 AND number_of_45p <=3 ", name="check_number_of_45p"),
    )



class Class(BaseModel):
    grade = Column(Enum(GRADE))
    name = Column(String(10), nullable=False)
    amount = Column(Integer, default=0)
    year = Column(Integer, default=datetime.now().year)
    # 1 lớp chỉ có 1 Giáo viên chủ nhiệm
    teacher_id = Column(Integer, ForeignKey(User.id),
                        unique=True)
    # teachings = relationship('Teaching', backref='class', lazy=True)
    students = relationship("Students_Classes", backref="class", lazy=True)
    regulation_id = Column(Integer, ForeignKey('regulation.id'), nullable=False)
    __table_args__ = (
        CheckConstraint("amount >= 0", name="check_class_amount"),
    )

    def __str__(self):
       return self.name



class Student(BaseModel):

    grade = Column(Enum(GRADE), default=GRADE.KHOI10)
    classes = relationship("Students_Classes", backref="student", lazy=True)
    profile = relationship("Profile", backref="student", lazy=True, uselist=False)
    profile_id = Column(Integer, ForeignKey("profile.id"), unique=True ,nullable=False)
    regulation_id = Column(Integer, ForeignKey('regulation.id'),nullable=False) #default = "Regulation.type.RE_AGE.id")

    def __str__(self):
        return self.profile.name

class Students_Classes(BaseModel):
    class_id = Column(Integer, ForeignKey(Class.id), nullable=False)
    student_id = Column(Integer, ForeignKey(Student.id), nullable=False)


class Semester(BaseModel):
    semester_name = Column(String(50), nullable=False)
    year = Column(Integer, default=datetime.now().year)
    # teachings = relationship('Teaching', backref='semester', lazy=True)
    __table_args__ = (
        db.UniqueConstraint('semester_name', 'year', name='unique_semester_year'),
    )
    def __str__(self):
        return f"< {self.semester_name} - {self.year}"


class Teaching(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    class_id = Column(Integer, ForeignKey(Class.id), nullable=False)
    semester_id = Column(Integer, ForeignKey(Semester.id), nullable=False)
    subject_id = Column(Integer, ForeignKey(Subject.id), nullable=False)
    teacher_id = Column(Integer, ForeignKey(User.id), nullable=False)



    classes = relationship('Class', backref='teachings', lazy=True)
    semester = relationship('Semester',backref='teachings',lazy=True)
    subject = relationship('Subject', backref='teachings', lazy=True)
    teacher = relationship('User',backref='teachings',lazy=True)
    # Thêm __str__ method để hiển thị thông tin
    def __str__(self):
        return f"Lớp: {self.classes.name}, {self.semester.semester_name}, Giáo viên: {self.teacher.profile.name}"



# Chi tiết điểm
class Exam(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey(Student.id), nullable=False)
    teach_plan_id = Column(Integer, ForeignKey(Teaching.id), nullable=False)
    scores = relationship("Score", backref="exam", lazy=True)

    student = relationship("Student", backref="exam", lazy=True)
    teach_plan = relationship("Teaching", backref="exam", lazy=True)


class Score(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    score = Column(Float)
    type = Column(Enum(TYPEEXAM))
    count = Column(Integer)
    Exam_id = Column(Integer, ForeignKey(Exam.id), nullable=False)

    __table_args__ = (
        CheckConstraint('score.js >= 0', name='check_age_min'),
        CheckConstraint('score.js <= 10', name='check_age_max'),
    )


class Regulation(BaseModel):
    type = Column(Enum(TYPE_REGULATION), default=TYPE_REGULATION.RE_AGE)
    name = Column(String(100))
    min_value = Column(Integer, nullable=False)
    max_value = Column(Integer, nullable=False)
    classes = relationship('Class', backref='regulation', lazy=True)
    students = relationship('Student', backref='regulation', lazy=True)
    __table_args__ = (
        CheckConstraint("min_value <= max_value", name="check_min_less_equal_max"),
    )
    def __str__(self):
        return self.name

#Mở rộng
class Notification(BaseModel):
    subject = Column(String(200),nullable=False)
    content = Column(Text,nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    admin_id = Column(Integer, ForeignKey(User.id))

    def __str__(self):
        return self.subject
if __name__ == "__main__":
    with app.app_context():
        # db.session.commit()
        # db.drop_all()
        # db.create_all()


        p1 = Profile(
            name="Trần Thế Anh",
            email="theanhtran13012004@gmail.com",
            birthday=datetime(1995, 1, 13).date(),
            gender=GENDER.Nam,
            address="1508 Lê Văn Lương , Nhà Bè , TPHCM",
            phone="0933033801"
        )

        p2 = Profile(
            name="Nguyễn Thị Minh Tuyết",
            email="minhtuyet31082004@gmail.com",
            birthday=datetime(1995, 8, 31).date(),
            gender=GENDER.Nu,
            address="802 Lê Văn Lương , Nhà Bè , TPHCM",
            phone="0522194804"
        )

        p3 = Profile(
            name="Trần Đức Huy",
            email="duchuytran30112004@gmail.com",
            birthday=datetime(1995, 11, 30).date(),
            gender=GENDER.Nam,
            address="145 Cộng hòa , Tân Bình , TPHCM",
            phone="0913001642"
        )

        p4 = Profile(
            name="Đào Trương Bách",
            email="daotruongbach123@gmail.com",
            birthday=datetime(1995, 10, 30).date(),
            gender=GENDER.Nam,
            address="1004 Linh Xuân , Thử Đức , TPHCM",
            phone="0531571272"
        )

        p5 = Profile(
            name="Võ Duy Khang",
            email="duykhangvo004@gmail.com",
            birthday=datetime(1995, 11, 20).date(),
            gender=GENDER.Nam,
            address="1403 Thủy Vân , Phường 3 , TP.Vũng Tàu",
            phone="0958473712"
        )

        p6 = Profile(
            name="Nguyễn Trọng Nhân",
            email="trongnhan3011@gmail.com",
            birthday=datetime(1993, 11, 12).date(),
            gender=GENDER.Nam,
            address="1312 đường Tên Lửa , Quận 12 , TPHCM",
            phone="0914201642"
        )

        p7 = Profile(
            name="Nguyễn Xuân Nghi",
            email="xuannghi3021@gmail.com",
            birthday=datetime(1994, 8, 12).date(),
            gender=GENDER.Nu,
            address="371 Nguyễn Kiệm , Gò Vấp , TPHCM",
            phone="0913001125"
        )

        p8 = Profile(
            name="Trần Thị Mến",
            email="thimentran001@gmail.com",
            birthday=datetime(1995, 3, 30).date(),
            gender=GENDER.Nu,
            address="1349 Nguyễn Thị Thập , Quận 7 , TPHCM",
            phone="0912101642"
        )

        # db.session.add_all([p1, p2 ,p3 ,p4 ,p5,p6 ,p7,p8])
        db.session.commit()
        # #  #
        acc1 = User( username="theanh", password=str(hashlib.md5("123456".encode("utf-8")).hexdigest()),
                    user_role=UserRole.ADMIN, profile_id =1)
        acc2 = User( username="minhtuyet", password=str(hashlib.md5("123456".encode("utf-8")).hexdigest()),
                    user_role=UserRole.STAFF , profile_id =2)
        acc3 = User( username="duchuy", password=str(hashlib.md5("123456".encode("utf-8")).hexdigest()),
                    user_role=UserRole.TEACHER , profile_id =3)
        acc4 = User( username="truongbach", password=str(hashlib.md5("123456".encode("utf-8")).hexdigest()),
                    user_role=UserRole.TEACHER , profile_id =4)
        acc5 = User( username="duykhang", password=str(hashlib.md5("123456".encode("utf-8")).hexdigest()),
                    user_role=UserRole.TEACHER,profile_id =5)
        acc6 = User( username="trongnhan", password=str(hashlib.md5("123456".encode("utf-8")).hexdigest()),
                    user_role=UserRole.TEACHER,profile_id =6)
        acc7 = User( username="xuannghi", password=str(hashlib.md5("123456".encode("utf-8")).hexdigest()),
                    user_role=UserRole.TEACHER, profile_id =7)
        acc8 = User( username="thimen", password=str(hashlib.md5("123456".encode("utf-8")).hexdigest()),
                    user_role=UserRole.TEACHER, profile_id =8)
        # db.session.add_all([acc1,acc2,acc3,acc4,acc5,acc6,acc7,acc8])
        db.session.commit()
        regulations = [
            Regulation(type=TYPE_REGULATION.RE_AGE, name="Tiếp nhận học sinh", min_value=16, max_value=20),
            Regulation(type=TYPE_REGULATION.RE_AMOUNT,name="Sĩ số tối đa", min_value=0, max_value=40), ]
        for r in regulations:
            # db.session.add(r)
            db.session.commit()



        db.session.commit()

        cl101 = Class(grade=GRADE.KHOI10, name='10A1', amount=0, teacher_id=3, regulation_id=2)
        cl102 = Class(grade=GRADE.KHOI10, name='10A2', amount=0, teacher_id=4, regulation_id=2)
        cl111 = Class(grade=GRADE.KHOI11, name='11A1', amount=0, teacher_id=5,regulation_id=2)
        cl112 = Class(grade=GRADE.KHOI11, name='11A2', amount=0, teacher_id=6,regulation_id=2)
        cl121 = Class(grade=GRADE.KHOI12, name='12A1', amount=0, teacher_id=7,regulation_id=2)
        cl122 = Class(grade=GRADE.KHOI12, name='12A2', amount=0, teacher_id=8,regulation_id=2)
        #
        # db.session.add_all([cl101, cl102, cl111, cl112, cl121, cl122,])
        db.session.commit()

        sb1 = Subject(name='Toán' , grade=GRADE.KHOI10 , number_of_15p=3, number_of_45p=2)
        sb2 = Subject(name='Ngữ Văn', grade=GRADE.KHOI10, number_of_15p=3, number_of_45p=2)
        sb3 = Subject(name='Lý', grade=GRADE.KHOI10, number_of_15p=3, number_of_45p=2)
        sb4 = Subject(name='Hóa', grade=GRADE.KHOI10, number_of_15p=3, number_of_45p=2)
        sb5 = Subject(name='Toán', grade=GRADE.KHOI11, number_of_15p=3, number_of_45p=2)
        sb6 = Subject(name='Lý', grade=GRADE.KHOI11, number_of_15p=3, number_of_45p=2)
        sb7 = Subject(name='Toán', grade=GRADE.KHOI12, number_of_15p=3, number_of_45p=2)
        # db.session.add_all([sb1,sb2,sb3,sb4,sb5,sb6,sb7])
        db.session.commit()


        #Tạo thử Student
        # st1 = Student(profile_id =10 , regulation_id = 1   )
        # db.session.add(st1)
        db.session.commit()
