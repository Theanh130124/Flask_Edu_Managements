from flask import Flask
# from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
#


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:123456@localhost/edudb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# app.config['BABEL_DEFAULT_LOCALE'] = 'vi'
# app.config['BABEL_SUPPOTED_LOCALES'] = ['en' ,'vi']
# babel = Babel(app)
db = SQLAlchemy(app)
