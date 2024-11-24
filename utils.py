from datetime import datetime
from app import app
# Nếu tháng 1-5: Học kỳ vẫn thuộc năm học trước (ví dụ: 2023-2024, thì đây vẫn là năm 2023).
# Nếu tháng 6-12: Năm học mới đã bắt đầu (ví dụ: 2024-2025, thì đây là năm 2024).
def get_academic_info(date=None):
    date = date or datetime.now()
    if date.month < 6:
        return {"Năm": date.year - 1, "Học kỳ": 2}
    return {"Năm": date.year, "Học kỳ": 1}

print(get_academic_info())  # {'year': 2023, 'semester': 2}

if __name__ == '__main__':
    with app.app_context():
        print(get_academic_info())