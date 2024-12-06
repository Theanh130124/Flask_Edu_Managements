from crypt import methods

from flask import request, jsonify
from app import app , db
from app.models import  Exam , Score
from app.dao import dao_subject


@app.route('/api/<teach_plan_id>/score', methods=['POST'])
def add_score(teach_plan_id):
    list_student = request.json['list_score']
    for s in list_student:
        tmp_exam = Exam.query.filter_by(teach_plan_id=teach_plan_id,student_id=s.get('id').first())
        if tmp_exam is None:
            tmp_exam = Exam(teach_plan_id=teach_plan_id, student_id=s.get("id"))
            db.session.add(tmp_exam)
            db.session.commit()
        new_score = Score(Exam_id=tmp_exam.id, score=s.get("points"), type=s.get("type"), count=s.get("count"))
        db.session.add(new_score)
        db.session.commit()
    return   jsonify({'status':200})

@app.route('/api/<teach_plan_id>/score', methods=['PUT'])
def edit_score(teach_plan_id):
    list_edit = request.json['list_score']
    for s in list_edit:
        e = Exam.query.filter_by(teach_plan_id=teach_plan_id, student_id=s.get("id")).first()
        tmp = db.session.query(Score).filter(Score.Exam_id == e.id).filter(Score.type == s.get("type")).filter(
            Score.count == s.get("count")).first()
        tmp.score = s.get("points")
        db.session.commit()
    return jsonify({'status': 200})

@app.route("/api/<int:semester_id>/<int:class_id>/<int:subject_id>/avg_score", methods=['GET'])
def get_avg_score(semester_id, class_id, subject_id):
    avg_scores = dao_subject.avg_score_student(semester_id, class_id, subject_id)
    result = [
        {
            'student_id': score[0],
            'student_name': score[1],
            'avg_score': score[2],
        } for score in avg_scores
    ]

    return jsonify(result)
