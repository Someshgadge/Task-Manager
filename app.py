from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# Configure JWT settings
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this to a secure key in production
jwt = JWTManager(app)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
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
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Example authentication logic (replace with your actual authentication mechanism)
        if username == 'admin' and password == 'password':
            # Store user session information (e.g., username) in session
            session['username'] = username
            return redirect(url_for('protected_area'))
        else:
            return render_template('login.html', message='Invalid credentials. Please try again.')

    return render_template('login.html')

# Protected area route
@app.route('/protected')
@login_required
def protected_area():
    return redirect(url_for('add_task'))

# Add Task route
@app.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']

        # Create new task and add it to the database
        task = Task(title=title, description=description)
        db.session.add(task)
        db.session.commit()
        
        return redirect(url_for('view_tasks'))

    return render_template('add_task.html')

# Edit Task route
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

# Delete Task route
@app.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('view_tasks'))

# View Tasks route
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

    # Example authentication logic (replace with your actual authentication mechanism)
    if username == 'admin' and password == 'password':
        # Create access token
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message='Invalid credentials'), 401

if __name__ == '__main__':
    with app.app_context():
        # Create SQLite database file and tables
        db.create_all()

    # Run the Flask app
    app.run(debug=True)
