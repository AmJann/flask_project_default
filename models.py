from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(35), unique=True)
    password = db.Column(db.String(35))
    authenticated = db.Column(db.Boolean, default=False)
    todos = db.relationship('ToDo', backref='User')
    def is_active(self):
        return True
            
    def get_id(self):
        return self.username
    
    def is_authenticated(self):
        return self.authenticated  

    def __repr__(self):
        return f'<User "{self.username}">'  

class ToDo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    date_due = db.Column(db.Date())
    in_progress = db.Column(db.Boolean, default=False)
    complete = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    def __repr__(self):
        return f'<ToDo "{self.text[:20]}...">'
