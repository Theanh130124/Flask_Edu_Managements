from app.models import Notification
from app import app

def load_all_notifications(page=1):
    notifications = Notification.query
    page_size = app.config["PAGE_SIZE_NOTIFICATIONS"]
    start = (page -1) * page_size
    notifications = notifications.slice(start, start + page_size)
    return   notifications.all()
def count_notifications():
    return Notification.query.count()