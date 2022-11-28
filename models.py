from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(35), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    date_added = db.Column(db.DateTime,default=datetime.utcnow())
    todos = db.relationship('ToDo', backref='User')
    
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self,password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User "{self.username}">'  

class ToDo(db.Model):
    __tablename__ = 'todos'
    todo_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.Text(500))
    date_due = db.Column(db.Date())
    in_progress = db.Column(db.Boolean, default=False)
    complete = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))



    def __repr__(self):
        return f'<ToDo "{self.text[:20]}...">'


