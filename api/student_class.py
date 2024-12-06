from  flask import request,jsonify
from sqlalchemy.exc import NoResultFound

from app import app , db
from app.models import Students_Classes , Class
from app.dao import dao_student


@app.route('/api/add_student_to_class/<int:class_id>', methods=['POST'])
def add_student_to_class(class_id):
    list_student = request.json.get('list_student', [])
    class_info = Class.query.filter_by(id=class_id).first()
    for s in list_student:
        student_class = Students_Classes(student_id=s, class_id=class_id)
        db.session.add(student_class)
    class_info.amount += len(list_student)
    db.session.commit()
    return jsonify({'status': 200})


@app.route('/api/delete_student_from_class/<int:class_id>', methods=['DELETE'])
def delete_student_from_class(class_id):
    list_student = request.json['list_student']
    class_info = Class.query.filter_by(id=class_id).first()
    for s in list_student:
        tmp = dao_student.check_student_in_class(student_id=s, class_id=class_id)
        db.session.delete(tmp)
    class_info.amount = max(0, class_info.amount - len(list_student))
    db.session.commit()
    return jsonify({'status': 200})


@app.route('/api/get_class_amount/<int:class_id>', methods=['GET'])
def get_class_amount(class_id):
    try:
        class_info = Class.query.filter_by(id=class_id).first()
        if not class_info:
            return jsonify({"error": "Lớp không tồn tại"}), 404

        # Trả về sĩ số của lớp học
        return jsonify({"amount": class_info.amount}), 200
    except NoResultFound:
        return jsonify({"error": "Lớp không tồn tại"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500