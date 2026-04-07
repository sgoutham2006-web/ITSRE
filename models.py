from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class StudentData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    attendance = db.Column(db.Integer, default=0)
    tamil = db.Column(db.Integer, default=0)
    english = db.Column(db.Integer, default=0)
    maths = db.Column(db.Integer, default=0)
    physics = db.Column(db.Integer, default=0)
    chemistry = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'roll': self.roll_number,
            'name': self.name,
            'attendance': self.attendance,
            'tamil': self.tamil,
            'english': self.english,
            'maths': self.maths,
            'physics': self.physics,
            'chemistry': self.chemistry
        }
