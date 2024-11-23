from flask_login import login_required

from app import app
from flask import  render_template

@app.route("/")
def index():
    return render_template("login.html")
@app.route('/home')
# @login_required
# @role_only([UserRole.STAFF, UserRole.TEACHER])
def home():
    # profile = auth.get_info_by_id(current_user.id)
    # notifications = notification.load_all_notifications()
    return render_template("index.html") #profile=profile, notifications=notifications)
if __name__ == '__main__':
    app.run(debug=True) #Lên pythonanywhere nhớ để Falsse