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
    blogs = db.relationship('Blog',backref="user_blogs")
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
##BLOG MODEL
class Blog(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    created_date = db.Column(db.DateTime,default=datetime.utcnow)
    comments = db.relationship('Comment',backref="blog_comments",lazy="dynamic")
##COMMENTS
class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    description = db.Column(db.Text)
    blog_id = db.Column(db.Integer,db.ForeignKey('blog.id'))
    created_date = db.Column(db.DateTime,default=datetime.utcnow)
###INDEX & LOGIN PAGE
@app.route('/index',methods=['GET','POST'])
@app.route('/',methods=['GET','POST'])
def index():
    blogs = Blog.query.order_by(Blog.created_date.desc()).all()
    return render_template("home.html",blogs=blogs)
###GET INDIVIDUAL BLOG DETAILS
@app.route('/blog/<int:id>',methods=['GET','POST'])
def blog_details(id):
    blog = Blog.query.get_or_404(id)
    comments = blog.comments.all()
    if blog:
        user = User.query.get_or_404(blog.user_id)
        return render_template('blog_details.html',blog=blog,user=user,comments=comments)
    return redirect(url_for('index'))
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
    return render_template("/dashboard/dashboard.html")

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
##LOGOUT PAGE
@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    # flash("You have successfully logged out!")
    return redirect(url_for('login'))
##BLOGS PAGE
@app.route('/my-blogs/<int:id>',methods=['POST','GET'])
def my_blogs(id):
    blogs = Blog.query.order_by(Blog.created_date.desc()).filter_by(user_id=id)
    return render_template("/dashboard/blog.html",blogs=blogs)
##NEW BLOG
@app.route('/new-blog')
def new_blog():
    return render_template("/dashboard/new_blog.html")
##CREATE BLOG
@app.route('/create-blog',methods=['POST','GET'])
def create_blog():
    if request.method == 'POST':
        # categories = PitchCategory.query.
        title = request.form['title']
        description = request.form['description']
        user_id = request.form['user']
        blog = Blog(title=title,description=description,user_id=user_id)
        db.session.add(blog)
        db.session.commit()
        return ('Blog created successfully')
##VIEW BLOB
##EDIT BLOG
@app.route('/my-blogs/edit/<int:id>',methods=['POST','GET'])
def edit_blog(id):
    blog = Blog.query.get_or_404(id)
    if blog:
        blog.title = request.form['title']
        blog.description = request.form['description']
        blog.user_id = request.form['user']
        db.session.add(blog)
        db.session.commit()
    return redirect(url_for('my-blogs',id=blog.user_id))
##POST COMMENTS
##########REGISTER USER
@app.route('/blog/comments',methods=['POST','GET'])
def comments():
    if request.method == 'POST':
        description = request.form['description']
        blog = request.form['blog']
        comment = Comment(description=description,blog_id=blog)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('index'))
#######BLOG COMMENTS
@app.route('/blog-comments/<int:id>',methods=['POST','GET'])
def blog_comments(id):
    blog = Blog.query.get_or_404(id)
    comments = blog.comments.all()
    return render_template("/dashboard/blog_comments.html",blog=blog,comments=comments)
########DELETE COMMENTS
@app.route('/blog-comments/delete-comments/<int:id>',methods=['POST','GET'])
def delete_comments(id):
    comment = Comment.query.get_or_404(id)
    try:
        db.session.delete(comment)
        db.session.commit()
        return('success')
    except:
        return('error')
######DELETE BLOG
@app.route('/my-blogs/delete-blog/<int:id>',methods=['POST','GET'])
def delete_blog(id):
    blog = Blog.query.get_or_404(id)
    try:
        db.session.delete(blog)
        db.session.commit()
        return('success')
    except:
        return('error')
#####MY PROFILE
@app.route('/profile')
def profile():
    return render_template('/dashboard/user_profile.html')