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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nabuusu:12345@localhost/blog'
db = SQLAlchemy(app)
migrate = Migrate(app,db)

#Flask login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'LOGIN'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
##User model
class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    full_name = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(200),nullable=False,unique=True)
    password_hash = db.Column(db.String(200))
    created_date = db.Column(db.DateTime,default=datetime.utcnow)
    
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)
    def __repr__(self):
        return '<Name %r>' % self.full_name
###INDEX & LOGIN PAGE
@app.route('/index',methods=['GET','POST'])
@app.route('/',methods=['GET','POST'])
def index():
    return render_template("home.html")

###ERROR 4O4
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

###ERROR 500
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"),500

##USER REGISTRATION
@app.route('/register')
def register():
    return render_template("register.html")

####DASHBOARD
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

##########REGISTER USER
@app.route('/users',methods=['POST'])
def users():
    full_name = request.form['full_name']
    email = request.form['email']
    hashed_password = generate_password_hash(request.form['password'],"sha256")
    user = User(full_name=full_name,email=email,password_hash=hashed_password)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('register'))
####LOGIN FORM
class LoginForm(FlaskForm):
    email = StringField("Email address", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

###INDEX & LOGIN PAGE
@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if(request.method == 'POST'):
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                try:
                    print(user.password_hash)
                    print(form.password.data)
                    login_user(user)
                    return redirect(url_for('dashboard'))
                    # if check_password_hash(user.password_hash,form.password.data):
                    #     print(user.password_hash)
                    #     login_user(user)
                    #     # flash("Login successfully")
                    #     print(user)
                    #     print('success')
                    #     # return jsonify({'name':user.full_name,'email':user.email})
                    #     return redirect(url_for('dashboard'))
                    # else:
                    #     flash("Wrong password - Try again")
                except Exception as e:
                    raise(e)
            else:
                flash("That user does not exist, try again!")
    return render_template("login.html",form=form)