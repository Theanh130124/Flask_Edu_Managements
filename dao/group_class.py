#
#
#
#
#
# def get_class():
#     return db.session.query(Class).join(Teacher).filter(Class.year == utils.get_current_year()).all()
#
#
# def count_class(grade):
#     return Class.query.filter(Class.year == utils.get_current_year()).filter(Class.grade == grade).count()
#
#
# def create_class(form):
#     new_class = Class(grade=form.grade.data,
#                       year=utils.get_current_year(),
#                       count=count_class(form.grade.data)+1,
#                       teacher_id=form.teacher.data)
#     db.session.add(new_class)
#     db.session.commit()
#     temp_student = student.get_list_student_no_class_by_grade(form.class_size.data,form.grade.data)
#     for s in temp_student:
#         student_class = Students_Classes(student_id=s.id,class_id=new_class.id)
#         db.session.add(student_class)
#         db.session.commit()
#
#
# def get_info_class_by_name(grade, count):
#     return Class.query.filter_by(grade="K"+str(grade), count=count,year=utils.get_current_year()).first()
#
#
# def get_class_by_id(id):
#     return Class.query.get(id)
#
#
# def count_student_in_class(class_id):
#     return Students_Classes.query.filter_by(class_id=class_id).count()
#
