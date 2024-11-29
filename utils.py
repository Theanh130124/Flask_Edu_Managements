from datetime import datetime
from app import app
import cloudinary.uploader
from datetime import date


# Nếu tháng 1-5: Học kỳ vẫn thuộc năm học trước (ví dụ: 2023-2024, thì đây vẫn là năm 2023).
# Nếu tháng 6-12: Năm học mới đã bắt đầu (ví dụ: 2024-2025, thì đây là năm 2024).
def get_academic_info(date=None):
    date = date or datetime.now()
    if date.month < 6:
        return {"Năm": date.year - 1, "Học kỳ": 2}
    return {"Năm": date.year, "Học kỳ": 1}


print(get_academic_info())  # {'year': 2023, 'semester': 2}


# Thêm hàm kiểm tra User là Teacher


def upload_to_cloudinary(file):
    try:
        upload_result = cloudinary.uploader.upload(file, folder="user_avatars/")
        return upload_result.get('secure_url')  # Trả về URL ảnh
    except Exception as e:
        print(f"Lỗi tải lên Cloudinary: {e}")
        return None


if __name__ == '__main__':
    with app.app_context():
        print(get_academic_info())
