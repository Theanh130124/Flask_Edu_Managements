
from app import dao, login , app
from flask import render_template, redirect,  request
from flask_login import current_user, login_required, logout_user, login_user








# Tải người dùng lên

@login.user_loader
def user_load(user_id):
    return dao.load_user(user_id)

@app.route('/')
def index():
    return redirect('/login')

@app.route('/home')
@login_required #Có cái này để gom user vào -> home
def home():
    profile = dao.get_info_by_id(current_user.id)
    return render_template('index.html',  profile=profile)  # Trang home (index.html)


@app.route('/login', methods=['GET', 'POST'])
def login_my_user():
        err_msg = ''
        if request.method.__eq__('POST'):
            username = request.form.get('username')
            password = request.form.get('password')
            # Truyền cả profile và user của người đó vào
            user = dao.auth_user(username=username, password=password)
            if user:
                login_user(user)
                return redirect('/home' )


        return render_template('login.html', err_msg=err_msg)

@app.route('/logout', methods=['get'])
def logout_my_user():
    logout_user()
    return redirect('/login')




if __name__ == '__main__':
    app.run(debug=True) #Lên pythonanywhere nhớ để Falsse