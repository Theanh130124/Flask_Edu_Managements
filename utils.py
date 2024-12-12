from datetime import datetime
from app import app , db
import cloudinary.uploader
from flask import flash

from datetime import date

def get_current_year():
    if datetime.now().month < 6:
        return datetime.now().year - 1
    return datetime.now().year

def get_current_semester():
    now = datetime.now()
    if now.month < 6:
        semester_name = "Học kỳ 2"
        year = now.year - 1
    else:
        semester_name = "Học kỳ 1"
        year = now.year
    return semester_name, year

def upload_to_cloudinary(file):
    try:
        upload_result = cloudinary.uploader.upload(file, folder="user_avatars/")
        return upload_result.get('secure_url')
    except Exception as e:
        flash(f"Lỗi tải lên Cloudinary: {e}")
        return None
def display_form_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Lỗi ở trường {field}: {error}", 'danger')  # Hiển thị lỗi lên giao diện

