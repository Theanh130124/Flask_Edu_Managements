from app.models import Regulation

def get_regulation_by_name(name):
    return Regulation.query.filter_by(name=name).first()