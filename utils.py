from datetime import datetime
from app import app
import cloudinary.uploader
from flask import flash
from datetime import date


# Nếu tháng 1-5: Học kỳ vẫn thuộc năm học trước (ví dụ: 2023-2024, thì đây vẫn là năm 2023).
# Nếu tháng 6-12: Năm học mới đã bắt đầu (ví dụ: 2024-2025, thì đây là năm 2024).
def get_current_year():
    if datetime.now().month < 6:
        return datetime.now().year - 1
    return datetime.now().year






#Upload ảnh
def upload_to_cloudinary(file):
    try:
        upload_result = cloudinary.uploader.upload(file, folder="user_avatars/")
        return upload_result.get('secure_url')  # Trả về URL ảnh
    except Exception as e:
        print(f"Lỗi tải lên Cloudinary: {e}")
        return None
#Hiển thị chi tiết lỗi

def display_form_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Lỗi ở trường {field}: {error}", 'danger')  # Hiển thị lỗi lên giao diện

