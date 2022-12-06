## Use

* Flask
* Flask-SQLAlchemy

## Install

```
In Terminal:
pip (or pip3) install -r requirements.txt (this depends on how your system is set up)
```
## Run

```
In Terminal:
python (or python3) app.py (this depends on how your system is set up)
```

**Overview**

1. wtforms is used in most form instances
2. Custom JS/CSS/HTML modal used and a Bootstrap modal used.
3. Admin page available and only viewable by 'Admin' user.
4. Mostly custom todo table (except scrollbar)

**Models**

```

 ## Todo

    todo_id - primary key unique id
    title - todo title text
    description - todo info text
    date_due = YY-MM-DD date
    in_progress = shows whether the task is started or not Boolean
    complete = shows whether the task is complete or not Boolean
    user_id = unique user id from User model

```

## User  

    id = primary key unique id
    username = unique required text
    password_hash = hashed password required
    date_added = datetime 
    todos = backref to User


**Routes**
```

http://localhost:3000/

index homepage todo list
```

http://localhost:3000/add/

modal add task 
```

http://localhost:3000/show/<int:id>/

view details of todo
```

http://localhost:3000/update/<int:id>/

update task
```

http://localhost:3000/delete/<int:id>/

delete task
```

http://localhost:3000/updateUser/<int:id>/

update username
```

http://localhost:3000/deleteUser/<int:id>/

delete user
```

http://localhost:3000/admin/deleteUser/<int:id>

delete user with different redirect
```

http://localhost:3000/progress/<int:id>

updates progress boolean
```

http://localhost:3000/complete/<int:id>

updates complete boolean
```

http://localhost:3000/filter_incomplete/

orders todos by incomplete first
```

http://localhost:3000/filter_complete/

orders todos by complete first
```

http://localhost:3000/filter_date/

orders tasks by date ascending
```

http://localhost:3000/filter_date2/

orders tasks by date descending
```

http://localhost:3000/registration/

sign up form adds user to db
```

http://localhost:3000/login/

logs user in
```

http://localhost:3000/logout/

logs user out
```

http://localhost:3000/admin/

admin page only accessible to admin
```

@app.errorhandler(404)

@app.errorhandler(500)
```
**Improvements**
```
1. add AJAX with prevent default to keep table from reloading
2. could add more columns to User model
