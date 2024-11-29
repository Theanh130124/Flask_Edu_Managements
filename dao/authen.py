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


# Display profile hiện tại -> Enum nhớ lấy thêm name hoặc name
def display_profile_data(profile, form_account):
    form_account.name.data = profile.name
    form_account.email.data = profile.email
    form_account.birthday.data = profile.birthday
    form_account.gender.data = profile.gender.value
    form_account.phone.data = profile.phone
    form_account.address.data = profile.address


def update_acc_info(form_account):
        profile = Profile.query.filter_by(user_id=current_user.id).first()
        if profile:
            profile.phone = form_account.phone.data
            profile.address = form_account.address.data
            if form_account.avatar.data:
                avatar_file = form_account.avatar.data
                avatar_url = upload_to_cloudinary(avatar_file)
                if avatar_url:
                    profile.avatar = avatar_url

            db.session.commit()

