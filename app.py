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


@app.route("/", methods=['POST', 'GET'])
def index():
    '''
    Home page
    '''
    todos = ToDo.query.all()
    return render_template('index.html',todos=todos)

@app.route("/add", methods=['POST','GET'])
def add():
    datetime_str = request.form['date']
    datetime_obj = datetime.strptime(datetime_str,
    "%Y-%m-%d")
    date = datetime_obj.date()
    todo = ToDo(title=request.form['title'], complete=False, date_due =date, description=request.form['description'], in_progress=False )
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('index'))

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

    # todo = ToDo.query.filter_by(todo_id = id).first() 
    # print(todo.title)

    # if request.method == 'POST':
    #     todo.title = request.form.get['title']
    #     todo.description = request.form.get['description']
    #     datetime_str = request.form.get['date']
    #     datetime_obj = datetime.strptime(datetime_str,
    #     "%Y-%m-%d")
    #     date = datetime_obj.date()
    #     todo.date_due = date
    #     todo.complete = todo.complete
    #     todo.in_progress = todo.in_progress

    #     db.session.commit()
    #     return redirect('/')

    # else:
    #     todo = ToDo.query.filter_by(todo_id = id).first() 
    #     return render_template('update.html', todo = todo)

# @app.route("/submit_update/<int:id>/", methods=['GET','POST'])  
# def submit_update(id):  
#     if request.method == 'GET':
#         todo = ToDo.query.filter_by(todo_id = id).first()
#         datetime_str = request.form['date']
#         datetime_obj = datetime.strptime(datetime_str,
#         "%Y-%m-%d")
#         date = datetime_obj.date()
#         todo = ToDo(title=request.form['title'], date_due =date, description=request.form['description'])
#         db.session.commit()
#         return redirect(url_for('index'))    
@app.route("/updated/<int:id>/", methods=['POST', 'GET'])  
def updated(id): 
    todo = ToDo.query.get_or_404(id)
    todo.title = request.form['title']
    todo.description = request.form['description']
    datetime_str = request.form['date']
    datetime_obj = datetime.strptime(datetime_str,
    "%Y-%m-%d")
    date = datetime_obj.date()
    todo.date_due = date

    db.session.commit()
    return redirect('/') 

@app.route('/delete/<int:id>')
def delete(id):
    task_delete = ToDo.query.get_or_404(id)

    try:
        db.session.delete(task_delete)
        db.session.commit()
        return redirect('/')
    except:
        return'issue deleting the task'

@app.route("/progress/<int:id>/", methods=['GET'])    
def progress(id):
    todo = ToDo.query.filter_by(todo_id = id).first()
    todo.in_progress = not todo.in_progress
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/complete/<int:id>/", methods=['GET'])    
def complete(id):
    todo = ToDo.query.filter_by(todo_id = id).first()
    todo.in_progress = True
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for('index'))  

@app.route('/filter_complete/<string:key>/', methods=['GET']) 
def filter_complete(key):
    todos = ToDo.query.order_by(ToDo.complete.asc()).all() 
    # filter_rule = request.args.get('filter') 
    if key == 'A-Z':
        todos = ToDo.query.order_by(ToDo.complete.desc()).all()
    return render_template('index.html', todos = todos)

@app.route('/sort/', methods=['GET'])    
def sort():
    todos =ToDo.query.all()
    todos.sorted()

    return render_template('index', todos=todos)    

if __name__ == "__main__":
    app.run(port=3000)
