from app.models import Class, Subject, Semester, Teaching, User, UserRole , Exam
from app import db
from datetime import date , datetime



#Phân công
def load_class_by_grade(grade):
    return Class.query.filter_by(grade=grade)

def load_subject_of_class(grade):
    return Subject.query.filter_by(grade=grade)


def load_all_teacher_subject(subject_id):
    return User.query.join(Teaching).filter(Teaching.subject_id == subject_id).all()


def get_semester(semester_id):
    return db.session.get(Semester, semester_id)

def load_assignments_of_class(class_id):
    return Teaching.query.filter_by(class_id=class_id)

def get_id_teacher_subject(teacher_id, subject_id):
    return Teaching.query.filter_by(teacher_id=teacher_id, subject_id=subject_id).first()


def save_subject_assignment(class_id, semester_id, teacher_subject_id):
    if isinstance(semester_id, int):
        plan, created = get_or_create(class_id=class_id, semester_id=semester_id, teacher_subject_id=teacher_subject_id)
        if created:
            plan.class_id = class_id
            plan.semester_id = semester_id
            plan.teacher_subject_id = teacher_subject_id
            db.session.commit()
        another = Teaching.query.filter_by(class_id=class_id, semester_id=3 - semester_id,
                                                teacher_subject_id=teacher_subject_id).first()
        if another:
            db.session.delete(another)
            db.session.commit()

    else:
        for s in semester_id:
            plan, created = get_or_create(class_id=class_id, semester_id=s, teacher_subject_id=teacher_subject_id)
            if created:
                plan.class_id = class_id
                plan.semester_id = s
                plan.teacher_subject_id=teacher_subject_id
                db.session.commit()



def get_or_create(class_id, semester_id, teacher_subject_id):
    plan = Teaching.query.filter_by(class_id=class_id, semester_id=semester_id, teacher_subject_id=teacher_subject_id).first()
    if plan:
        return plan, True
    else:
        score_dl = None
        if semester_id == 1:
            score_dl = datetime(year=date.today().year - 1, month=12, day=31)
        else:
            score_dl = datetime(year=date.today().year, month=6, day=29)

        create_plan = Teaching(
            class_id=class_id,
            semester_id=semester_id,
            teacher_subject_id=teacher_subject_id,
            score_deadline=score_dl
        )

        db.session.add(create_plan)
        db.session.commit()
        return create_plan, False
def delete_assignments(class_id):
    try:
        # Tìm các bài thi liên quan đến lớp học
        exams = Exam.query.join(Teaching).filter(Teaching.class_id == class_id).all()

        # Kiểm tra nếu không có bài thi nào, tránh việc cập nhật
        if exams:
            # Tìm phân công giảng dạy mặc định (hoặc phân công giảng dạy khác hợp lệ)
            default_teach_plan = Teaching.query.first()  # Hoặc chọn phân công giảng dạy phù hợp

            for exam in exams:
                if default_teach_plan:
                    exam.teach_plan_id = default_teach_plan.id  # Gán teach_plan_id hợp lệ
                else:
                    # Nếu không có phân công giảng dạy hợp lệ, tạo phân công mặc định hoặc xử lý tình huống này
                    raise ValueError("Không có phân công giảng dạy hợp lệ để thay thế teach_plan_id.")

                db.session.add(exam)

        # Xóa các phân công giảng dạy
        assignments_to_delete = Teaching.query.filter_by(class_id=class_id).all()
        for assignment in assignments_to_delete:
            db.session.delete(assignment)

        # Commit các thay đổi
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Lỗi khi xóa phân công: ")





