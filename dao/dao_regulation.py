from app.models import Regulation , TYPE_REGULATION
from app import app




def get_regulations( page =1 ):
    regulations = Regulation.query
    page_size = app.config["PAGE_SIZE_REGULATIONS"]
    start = (page -1) * page_size
    regulations = regulations.slice(start , start + page_size)
    return regulations.all()

def get_regulation_by_type(my_type):
    return Regulation.query.filter_by(type=my_type).first()

def count_regulations():
    return Regulation.query.count()