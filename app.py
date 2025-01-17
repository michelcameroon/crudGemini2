# app.py

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, Student 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sokolo.db'  # Replace with your actual database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    students = Student.query.all()
    return render_template('list.html', students=students)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        age = request.form['age']
        new_student = Student(firstName=firstName, lastName=lastName, age=age)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.firstName = request.form['firstName']
        student.lastName = request.form['lastName']
        student.age = request.form['age']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', student=student)

@app.route('/delete/<int:id>')
def delete(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
