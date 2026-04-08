import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
import jwt
import datetime
from functools import wraps
from models import db, User, StudentData

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Configuration
app.config['SECRET_KEY'] = 'super-secret-eduai-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# --- JWT Middleware ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'message': 'Token is missing!'}), 401
        token = auth_header.split(' ')[1]
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(username=data['user']).first()
            if not current_user:
                raise Exception("User not found")
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorated


# --- ROUTING (HTML Pages) ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login.html')
def login_page():
    return render_template('login.html')

@app.route('/teacher.html')
def teacher_page():
    return render_template('teacher.html')

@app.route('/student.html')
def student_page():
    return render_template('student.html')


# --- API ENDPOINTS ---
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    role = data.get('role')
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username, role=role).first()
    if not user or not user.check_password(password):
        return jsonify({'message': 'Invalid Credentials'}), 401
    
    token = jwt.encode({
        'user': user.username,
        'role': user.role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({'token': token, 'role': user.role})


@app.route('/api/students', methods=['GET', 'POST'])
@token_required
def api_students(current_user):
    if current_user.role != 'teacher':
        return jsonify({'message': 'Unauthorized'}), 403

    if request.method == 'GET':
        students = StudentData.query.all()
        return jsonify([s.to_dict() for s in students])
    
    if request.method == 'POST':
        data = request.get_json()
        roll = data.get('roll')
        
        # Check if student exists, update if they do
        student = StudentData.query.filter_by(roll_number=roll).first()
        if not student:
            student = StudentData(roll_number=roll)
            db.session.add(student)
        
        student.name = data.get('name')
        student.attendance = int(data.get('attendance', 0))
        student.tamil = int(data.get('tamil', 0))
        student.english = int(data.get('english', 0))
        student.maths = int(data.get('maths', 0))
        student.physics = int(data.get('physics', 0))
        student.chemistry = int(data.get('chemistry', 0))
        
        db.session.commit()
        return jsonify({'message': 'Student saved successfully!', 'student': student.to_dict()})


@app.route('/api/students/<roll>', methods=['GET', 'DELETE'])
@token_required
def api_student_single(current_user, roll):
    if request.method == 'DELETE':
        if current_user.role != 'teacher':
            return jsonify({'message': 'Unauthorized'}), 403
        student = StudentData.query.filter_by(roll_number=roll).first()
        if student:
            db.session.delete(student)
            db.session.commit()
            return jsonify({'message': 'Deleted'})
        return jsonify({'message': 'Not found'}), 404

    # Only allow students to query themselves, or teachers to query anyone
    if current_user.role == 'student' and current_user.username != 'student': # For demo, generic student user handles all
        pass 
        
    student = StudentData.query.filter_by(roll_number=roll).first()
    if not student:
        return jsonify({'message': 'Student not found'}), 404
        
    return jsonify(student.to_dict())


# --- SEEDING DATABASE ---
def seed_db():
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='teacher').first():
            teacher = User(username='teacher', role='teacher')
            teacher.set_password('1234')
            db.session.add(teacher)
        
        if not User.query.filter_by(username='student').first():
            student = User(username='student', role='student')
            student.set_password('1234')
            db.session.add(student)
            
        db.session.commit()
        print("Database Initialized and Seeded.")

# Initialize database and seed on startup (for Render/Gunicorn)
seed_db()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
