from flask import Flask,render_template,flash,request,jsonify,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
import os

app = Flask(__name__)
app.config['SECRET_KEY']="Abcd1234!@#$%^&*()EFGH"