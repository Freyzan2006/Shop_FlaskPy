from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from flask_restful import Api

from shop .config import SECRET_KEY, UPLOAD_FOLDER, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, MAX_CONTENT_LENGTH
from shop .config import URL_BACKAND




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.secret_key = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
db = SQLAlchemy(app)
manager = LoginManager(app)



# with app.app_context():
#     from shop .models import User
#     from werkzeug.security import generate_password_hash
#     import time

#     db.create_all()

#     hash_pwd = generate_password_hash("123")
#     new_admin = User(login = "admin", password = hash_pwd, isAdmin = True)

#     db.session.add(new_admin)
#     db.session.commit()



import shop.views