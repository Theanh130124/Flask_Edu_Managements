from app.models import Regulation , TYPE_REGULATION
from app import app




def get_regulations( page =1 ):

    return Regulation.query.all()

def get_regulation_by_type(my_type):
    return Regulation.query.filter_by(type=my_type).first()

