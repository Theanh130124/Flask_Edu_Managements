from flask import Flask
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import cloudinary
#


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:123456@localhost/edudb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['SECRET_KEY'] = '@#$@#$!#$!@#$!@%@#%$@##$TheAnh'
app.config['BABEL_DEFAULT_LOCALE'] = 'vi'
app.config['BABEL_SUPPOTED_LOCALES'] = ['en' ,'vi']

babel = Babel(app)
cloudinary.config(
    cloud_name="dxiawzgnz",
    api_key="916324835836949",
    api_secret="it9HP_2TUJjIHLSshkbm0BYA5qE"
)
db = SQLAlchemy(app)
login = LoginManager(app)

