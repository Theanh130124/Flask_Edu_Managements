from flask import Flask
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

import cloudinary
import cloudinary.api
import cloudinary.uploader


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:123456@localhost/edudb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['SECRET_KEY'] = '@#$@#$!#$!@#$!@%@#%$@##$TheAnh'
app.config['BABEL_DEFAULT_LOCALE'] = 'vi'
app.config['BABEL_SUPPOTED_LOCALES'] = ['en' ,'vi']
app.config['PAGE_SIZE_NOTIFICATIONS'] = 3
app.config['PAGE_SIZE_REGULATIONS'] = 5 #1 trang 5 quy định
app.config['PAGE_SIZE_LIST_CLASS'] = 5
app.config['PAGE_SIZE_DETAIL_CLASS'] = 5
app.config['PAGE_SIZE_VIEW_SCORE_SUBJECT'] = 8


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'theanhtran13012004@gmail.com'
app.config['MAIL_PASSWORD'] = 'kmui vkff bpwd wyke'


mail = Mail(app)

babel = Babel(app)
cloudinary.config(
   cloud_name="dp9lw5n5g",
    api_key="794682182282692",
    api_secret="QKmsUnjc9uwBfY9VYb4dxoyWDcw",
    api_proxy ='http://proxy.server:3128'
)
db = SQLAlchemy(app)
login = LoginManager(app)

