from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token
from functools import wraps

app = Flask(__name__)
app.secret_key = '6PKLIKZHbTB5Be27YCRNasYj1xROl-eQC2mvlgXV4JY'  

# Configure JWT settings
app.config['JWT_SECRET_KEY'] = 'super-secret'  
jwt = JWTManager(app)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Define login route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', message='Welcome to Task Management Portal')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', message='Click here to login')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':
            session['username'] = username
            return redirect(url_for('protected_area'))
        else:
            return render_template('login.html', message='Invalid credentials. Please try again.')

# Protected area route
@app.route('/protected')
@login_required
def protected_area():
    return redirect(url_for('add_task'))

# ADD Task route
@app.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        task = Task(title=title, description=description)
        db.session.add(task)
        db.session.commit()
        
        return redirect(url_for('view_tasks'))

    return render_template('add_task.html')

# EDIT Task route
@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get(task_id)

    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        db.session.commit()

        return redirect(url_for('view_tasks'))

    return render_template('edit_task.html', task=task)

# DELETE Task route
@app.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('view_tasks'))

# VIEW Tasks route
@app.route('/view_tasks')
@login_required
def view_tasks():
    tasks = Task.query.all()
    return render_template('view_tasks.html', tasks=tasks)

# API endpoint to get JWT token
@app.route('/api/login', methods=['POST'])
def api_login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if username == 'admin' and password == 'password':
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message='Invalid credentials'), 401

if __name__ == '__main__':
    with app.app_context():
        
        db.create_all()

    app.run(debug=True, host='0.0.0.0', port=8039)
