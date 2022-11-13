from flask import Flask, redirect, url_for, render_template, request
from models import db, User, ToDo
from flask_sqlalchemy import SQLAlchemy


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
    todo = ToDo(text=request.form['item'], complete=False)
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(port=3000)
