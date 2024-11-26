import hashlib

from flask_login import current_user

from app import db
import cloudinary
from  flask import  flash
import cloudinary.uploader

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

#Student
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
#Update profile ->
def update_user_info(profile, form_account):
    if form_account.email.data != profile.email:
        profile.email = form_account.email.data

    if form_account.address.data != profile.address:
        profile.address = form_account.address.data

    if form_account.phone.data != profile.phone:
        profile.phone = form_account.phone.data

    if form_account.avatar.data:
        avatar_file = form_account.avatar.data
        try:
            upload_result = cloudinary.uploader.upload(avatar_file)
            avatar_url = upload_result['secure_url']
            current_user.avatar = avatar_url
        except Exception as e:
            flash(f"Lỗi tải ảnh: {str(e)}", 'error')
            return None  # Nếu có lỗi thì trả về None

    try:
        db.session.commit()  # Lưu thay đổi vào cơ sở dữ liệu
        flash('Thông tin của bạn đã được cập nhật!', 'success')
    except Exception as e:
        db.session.rollback()  # Rollback nếu có lỗi
        flash(f"Cập nhật thất bại: {str(e)}", 'error')
        return None

    return current_user.avatar  # Trả về URL avatar nếu có thay đổi


#Display profile hiện tại -> Enum nhớ lấy thêm name hoặc name
def display_profile_data(profile, form_account):
    form_account.name.data = profile.name
    form_account.email.data = profile.email
    form_account.birthday.data = profile.birthday
    form_account.gender.data = profile.gender.value
    form_account.phone.data = profile.phone
    form_account.address.data = profile.address
