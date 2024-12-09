import hashlib



from app.models import Profile, User
from app import db, app
from app.utils import upload_to_cloudinary
from flask_login import current_user


# User and Info
def get_info_by_id(id):
    return Profile.query.get(id)


def load_user(user_id):
    return User.query.get(user_id)


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()



def display_profile_data(profile, form_account):
    form_account.name.data = profile.name
    form_account.email.data = profile.email
    form_account.birthday.data = profile.birthday
    form_account.gender.data = profile.gender.value
    form_account.phone.data = profile.phone
    form_account.address.data = profile.address


def update_acc_info(form_account):
    profile = current_user.profile


    profile.email = form_account.email.data
    profile.phone = form_account.phone.data
    profile.address = form_account.address.data


    if form_account.avatar.data:
        avatar_file = form_account.avatar.data
        uploaded_url = upload_to_cloudinary(avatar_file)
        if uploaded_url:
            current_user.avatar = uploaded_url
        else:
            raise Exception("Tải ảnh lên Cloudinary thất bại.")
    db.session.commit()
def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def check_password_md5(user, password):
    if user and user.password:  # Đảm bảo user tồn tại và có trường password
        hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()
        return hashed_password == user.password
    return False

def check_email_exists(email):
    return Profile.query.filter_by(email=email).first() is not None

def check_phone_exists(phone):
    return Profile.query.filter_by(phone=phone).first() is not None