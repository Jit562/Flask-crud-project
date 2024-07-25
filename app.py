from flask import Flask, request, redirect, url_for, flash
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime


app = Flask(__name__)
app.debug = True

# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Creating an SQLAlchemy instance
db = SQLAlchemy(app)


# Models
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Name : {self.first_name}, Age: {self.age}"
    


class Todo(db.Model):
    sn = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), unique=False, nullable=False)
    desc = db.Column(db.String(500), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f"S_n : {self.sn}, Title: {self.title}"    

#automatic create table using this command 
with app.app_context():
    db.create_all()



@app.route('/' , methods=['POST','GET'])
def Home():
    if request.method == 'POST':

        if not request.form['title'] or not request.form['desc']:

            flash('Please enter all the fields', 'error')

        else:
            title = request.form['title']
            desc = request.form['desc']

            todo = Todo(title=title, desc=desc)

            db.session.add(todo)
            db.session.commit()
            
    
    quer = Todo.query.all()     
    return render_template('index.html', quer=quer)    


@app.route('/delete/<int:sn>')
def delete(sn):
    todo = Todo.query.filter_by(sn=sn).first()
    db.session.delete(todo)
    db.session.commit()

    return redirect("/")


@app.route('/update/<int:sn>', methods = ['POST','GET'])
def update(sn):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sn=sn).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()

        return redirect('/')
    
    todo = Todo.query.filter_by(sn=sn).first()
    return render_template('update.html', todo=todo) 


    
if __name__ == '__main__':

    app.run()



