import hashlib
from app import db

from app.models import User, Profile , Student

#Authen
def get_info_by_id(id):
    return Profile.query.get(id)


def load_user(user_id):
    return User.query.get(user_id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def create_student(form):
    profile = Profile(name=form.full_name.data,
                      gender=int(form.gender.data),
                      birthday=form.birth_date.data,
                      address=form.address.data,
                      phone=form.phone_number.data,
                      email=form.email.data)
    db.session.add(profile)
    db.session.commit()
    student = Student(id=profile.id)
    db.session.add(student)
    db.session.commit()
    return student