from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import stripe
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

#loadfile .env
load_dotenv() 

app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mssql+pyodbc://<USERNAME>:<PASSWORD>@<SERVER_NAME>\\<INSTANCE>/<DB_NAME>'
    '?driver=ODBC+Driver+17+for+SQL+Server'
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = os.getenv('SECRET_KEY')
# Stripe keys
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
# JWT_SECRET
jwt_secret = os.getenv('JWT_SECRET')
# Cấu hình Flask-Mail dùng Gmail + App Password
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)



from store.models import Users

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Users, int(user_id))     

from store import routes
