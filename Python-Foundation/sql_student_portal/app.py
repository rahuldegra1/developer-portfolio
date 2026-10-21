from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "studentportalsecret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"

db = SQLAlchemy(app)

# Many-to-Many Association Table for Enrollments & Grades
enrollments = db.Table(
    "enrollments",
    db.Column("student_id", db.Integer, db.ForeignKey("student.id"), primary_key=True),
    db.Column("course_id", db.Integer, db.ForeignKey("course.id"), primary_key=True),
    db.Column("grade", db.String(5), nullable=True),
)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    major = db.Column(db.String(100), nullable=False)
    courses = db.relationship(
        "Course",
        secondary=enrollments,
        lazy="subquery",
        backref=db.backref("students", lazy=True),
    )


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    instructor = db.Column(db.String(100), nullable=False)


@app.route("/")
def index():
    students = Student.query.all()
    courses = Course.query.all()
    return render_template("index.html", students=students, courses=courses)


@app.route("/add_student", methods=["POST"])
def add_student():
    name = request.form.get("name")
    email = request.form.get("email")
    major = request.form.get("major")
    if name and email:
        new_student = Student(name=name, email=email, major=major)
        db.session.add(new_student)
        db.session.commit()
    return redirect(url_for("index"))


@app.route("/add_course", methods=["POST"])
def add_course():
    title = request.form.get("title")
    instructor = request.form.get("instructor")
    if title and instructor:
        new_course = Course(title=title, instructor=instructor)
        db.session.add(new_course)
        db.session.commit()
    return redirect(url_for("index"))


@app.route("/enroll", methods=["POST"])
def enroll():
    student_id = request.form.get("student_id")
    course_id = request.form.get("course_id")
    student = Student.query.get(student_id)
    course = Course.query.get(course_id)
    if student and course and course not in student.courses:
        student.courses.append(course)
        db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
