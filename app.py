from flask import Flask, redirect, url_for, render_template, request
from models import db, User, ToDo
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '\x14B~^\x07\xe1\x197\xda\x18\xa6[[\x05\x03QVg\xce%\xb2<\x80\xa4\x00'
app.config['DEBUG'] = True

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db.init_app(app)

# db.create_all()


@app.route("/")
def index():
    '''
    Home page
    '''
    todos = ToDo.query.all()
    return render_template('index.html',todos=todos)

@app.route("/add", methods=['POST'])
def add():
    datetime_str = request.form['date']
    datetime_obj = datetime.strptime(datetime_str,
    "%Y-%m-%d")
    date = datetime_obj.date()
    todo = ToDo(title=request.form['title'], complete=False, date_due =date, description=request.form['description'], in_progress=False )
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/show/<int:id>", methods=['GET'])
def show(id):
    todo = ToDo.query.filter_by(todo_id=id).first()
    print(id)

    return render_template('show.html', todo = todo)
     

if __name__ == "__main__":
    app.run(port=3000)
