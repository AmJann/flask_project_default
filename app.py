from flask import Flask, redirect, url_for, render_template, request, flash, session, jsonify
from models import db, User, ToDo
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField,DateField ,ValidationError
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from wtforms.widgets import TextArea


# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['DEBUG'] = True

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db.init_app(app)

# db.create_all()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


@app.route("/", methods=['POST', 'GET'])
def index():
    form = AddForm()
    if current_user.is_authenticated:
        id = current_user.id
        todos = ToDo.query.filter_by(user_id=id).all()
        return render_template('index.html',todos=todos, form=form)     
    else:
        flash('Must be logged in to view your to-do list')
        return render_template('index.html',form=form)        

class AddForm(FlaskForm):
    title=StringField("title",validators=[DataRequired()])
    date_due=DateField("date_due",validators=[DataRequired()])
    description=StringField("description",validators=[DataRequired()], widget=TextArea())
    submit=SubmitField("Submit") 

@app.route("/add/", methods=['POST','GET'])
def add():
    form = AddForm()

    if form.validate_on_submit():
        poster = current_user.id
        # ToDo(date_due = request.form.data)
        # datetime_obj = datetime.strptime(date_due,
        # "%Y-%m-%d")
        # date = datetime_obj.date()
        todo = ToDo(title=form.title.data,date_due =form.date_due.data, user_id=poster, description=form.description.data,)
  
        form.title.data = ''
        form.date_due.data = ''
        form.description.data = ''
        db.session.add(todo)
        db.session.commit()
        flash("Task Added successfully")
    return redirect(url_for('index', form=form))

@app.route("/show/<int:id>/", methods=['GET'])
def show(id):
    todo = ToDo.query.filter_by(todo_id = id).first()
    return render_template('show.html', todo = todo)

@app.route("/update/<int:id>/", methods=['POST', 'GET'])  
def update(id): 
    todo = ToDo.query.get_or_404(id)
    if request.method == "POST":
        todo.title = request.form['title']
        todo.description = request.form['description']
        datetime_str = request.form['date']
        datetime_obj = datetime.strptime(datetime_str,
        "%Y-%m-%d")
        date = datetime_obj.date()
        todo.date_due = date
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem updating your task."  
    else:
        return render_template('update.html', todo=todo)          
  

@app.route('/delete/<int:id>')
@login_required 
def delete(id):
    task_delete = ToDo.query.get_or_404(id)

    try:
        db.session.delete(task_delete)
        db.session.commit()
        return redirect('/')
    except:
        return'issue deleting the task'

@app.route("/updateUser/<int:id>/",methods=['POST','GET'])  
def updateUser(id): 
    user = User.query.get_or_404(id)
    if request.method == "POST":
        user.username = request.form['username']
        try:
            db.session.commit()
            return redirect(url_for('dashboard'))
        except:
            return "There was a problem updating your task."  
    else:
        return render_template('updateUser.html', user=user)   

@app.route('/deleteUser/<int:id>')
@login_required 
def deleteUser(id):
    user_delete = User.query.get_or_404(id)

    try:
        db.session.delete(user_delete)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return'issue deleting user'

@app.route('/admin/deleteUser/<int:id>')
@login_required 
def adminDeleteUser(id):
    user_delete = User.query.get_or_404(id)

    try:
        db.session.delete(user_delete)
        db.session.commit()
        return redirect(url_for('admin'))
    except:
        return'issue deleting user'        
    

@app.route("/progress/<int:id>/", methods=['GET','POST'])
@login_required    
def progress(id):
    todo = ToDo.query.filter_by(todo_id = id).first()
    todo.in_progress = not todo.in_progress
    db.session.commit()
    return redirect(url_for('index'))  

@app.route("/complete/<int:id>/", methods=['GET', 'POST'])
@login_required    
def complete(id):
    clicked=None
    todos = ToDo.query.filter_by(todo_id = id).first()
    clicked = request.data
    todos.complete = not todos.complete
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/filter_incomplete/', methods=['GET', 'POST']) 
def filter_incomplete():
    form = AddForm()
    if current_user.is_authenticated:
        id = current_user.id
        todos = ToDo.query.filter_by(user_id=id).order_by(ToDo.complete.asc()).order_by(ToDo.in_progress.asc()).all() 
        return render_template('index.html', todos=todos,form=form)    
    else:
        flash('Must be logged in to view your to-do list')
        return render_template('index.html',form=form)  

@app.route('/filter_complete/', methods=['GET', 'POST'])
def filter_complete():
    form = AddForm()
    if current_user.is_authenticated:
        id = current_user.id
        todos = ToDo.query.filter_by(user_id=id).order_by(ToDo.complete.desc()).order_by(ToDo.in_progress.desc()).all() 
        return render_template('index.html', todos=todos,form=form)    
    else:
        flash('Must be logged in to view your to-do list')
        return render_template('index.html',form=form)  

class RegistrationForm(FlaskForm):
    username=StringField("Username",validators=[DataRequired(),Length(min=4,max=25,message="Username must be between 4 and 25 characters")])
    password_hash=PasswordField("Password",validators=[DataRequired(), EqualTo('password_hash2', message='Passwords Must Match'), Length(min=4,max=25,message="Username must be between 4 and 25 characters")])
    password_hash2=PasswordField("Confirm Password",validators=[DataRequired(), Length(min=4,max=25,message="Username must be between 4 and 25 characters")])
    submit=SubmitField("Submit")

    def validate_username(self,username):
        user_object = User.query.filter_by(username=username.data).first()
        if user_object:
            raise ValidationError("Username already exists")

@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    username = None
    password_hash = None
    form = RegistrationForm()
    if form.validate_on_submit():
        username =form.username.data
        password_hash =form.password_hash.data
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data, password_hash=form.password_hash.data).first()
              
            if user is None:
                hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
                user = User(username=form.username.data, password_hash=hashed_pw)
                db.session.add(user)
                db.session.commit()
            username = form.username.data
            form.username.data = ''
            form.password_hash.data = ''
            flash("Sign-up Successful")
        else:
            flash('user already exists')
            redirect(url_for('registration'))
      
    our_users = User.query.all()
    return render_template('registration.html',
    username=username,
    password_hash=password_hash,
    form=form,
    our_users=our_users
    )   
class PasswordForm(FlaskForm):
    username=StringField("Username",validators=[DataRequired()])
    password_hash=PasswordField("Password",validators=[DataRequired()])
    submit=SubmitField("Submit")

class LoginForm(FlaskForm):
    username =StringField("Username",validators=[DataRequired()])
    password =PasswordField("Password",validators=[DataRequired()])
    submit =SubmitField("Submit")


@app.route('/login/', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user:
			# Check the hash
			if check_password_hash(user.password_hash, form.password.data):
				login_user(user)
				flash("Login Succesfull!!")
				return redirect(url_for('dashboard'))        
			else:
				flash("Wrong Password - Try Again!")
		else:
			flash("That User Doesn't Exist! Try Again...")


	return render_template('login.html', form=form) 

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You are Logged Out.")
    return redirect(url_for('login'))

@app.route('/dashboard/', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')       

@app.route('/test_pw/', methods=['GET','POST'])
def test_pw():
    username = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password_hash.data
        form.username.data = ''
        form.password_hash.data = ''

        pw_to_check = User.query.filter_by(username=username).first()
        passed =check_password_hash(pw_to_check.password_hash, password)

    return render_template("test_pw.html",
        username = username,
        password = password,
        pw_to_check=pw_to_check,
        passed=passed,
        form = form
        )

@app.route('/admin/')
@login_required
def admin():
    username = current_user.username
    if username == 'Admin':
        users = User.query.all()
        return render_template('admin.html', users=users)
    else:
        flash("Sorry only Admin can access this Page") 
        return redirect(url_for('index'))   

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500 

   

    
    
    

if __name__ == "__main__":
    app.run(port=3000)
