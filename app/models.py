from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# loading logged in user
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# association tables 
# track the user enrolment
enrolled_course = db.Table('enrolled_course',
    db.Column('course_id', db.Integer, db.ForeignKey('course.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

# User model
class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(128), index = True, unique = True) 
    # ONLY store hashed password
    password_hash = db.Column(db.String(128))

    # gained by complete quiz
    scores = db.Column(db.Integer)
    # user's enrolled courses
    courses = db.relationship('Course', secondary=enrolled_course, lazy = 'dynamic')
    # user's completed quiz
    quizes = db.relationship('Quiz', backref='user', lazy = 'dynamic')

     # hash plain password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # check hashed password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # enrol in a course
    def enrol(self, course):
        self.courses.append(course)

    # attempt a quiz
    def attempt(self, quiz):
        self.quizes.append(quiz)

    # check if user has already enrolled the course
    def is_enrolling(self, course):
        return self.courses.filter(
            enrolled_course.c.user_id == self.id).filter(
                enrolled_course.c.course_id == course.id).count() > 0
    
    # return a list of enrolled course entities
    def enrolled_course(self):
        return Course.query.join(
            enrolled_course, (enrolled_course.c.course_id == Course.id)).filter(
                enrolled_course.c.user_id == self.id)
    
    # return a list of completed quizes - only keep the newest version
    def completed_quiz(self):
        res = []
        quizname = []
        quizes = Quiz.query.order_by(
                    Quiz.timestamp.desc()).filter_by(
                        user_id=self.id).all()
        for quiz in quizes:
            if quiz.quizname not in quizname:
                res.append(quiz)
                quizname.append(quiz.quizname)
        return res

    # get the total user course points 
    def user_course_points(self):
        courses = self.enrolled_course()
        point = 0
        for course in courses:
            point += 10
        return point    

    # get the total user quiz points 
    def user_quiz_points(self):
        quizes = self.completed_quiz()
        point = 0
        for quiz in quizes:
            point += quiz.quiz_scoreoutofhundred / 5
        return point
    
    # represent data
    def __repr__ (self):
        return '<User {}>'.format(self.username)

# Course model
class Course(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    coursename = db.Column(db.String(128), index = True, unique = True)
    courseurl = db.Column(db.String(128), index = True, unique = True)
    
    def __repr__(self):
        return '<Course {} url {}>'.format(self.coursename, self.courseurl)

# Quiz model
class Quiz(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    quizname = db.Column(db.String(128), index = True)
    quizurl = db.Column(db.String(128), index = True)
    quiz_scoreoutofhundred = db.Column(db.Integer())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Quiz {} url {}>'.format(self.id, self.quizurl)

# check if the course has been added to database
def is_init_course():
    courses = Course.query.all()
    if not courses:
        return False
    return True

# return quiz score out of hundred
def quiz_score(questions, answers):
    correct = 0
    for i in range(5):
        if questions[i] == answers[i]:
            correct += 1
    return correct / 5 * 100


