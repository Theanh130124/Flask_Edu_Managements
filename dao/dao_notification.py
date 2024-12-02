from app.models import Notification

def load_all_notifications():
    return   Notification.query.all()