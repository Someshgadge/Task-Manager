from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

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

# Define login route
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
def protected_area():
    # Check if user is authenticated (username stored in session)
    if 'username' in session:
        return redirect(url_for('add_task'))
    else:
        return redirect(url_for('login'))

# Add Task route
@app.route('/add_task', methods=['GET', 'POST'])
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
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('view_tasks'))

# View Tasks route
@app.route('/view_tasks')
def view_tasks():
    tasks = Task.query.all()
    return render_template('view_tasks.html', tasks=tasks)

if __name__ == '__main__':
    with app.app_context():
        # Create SQLite database file and tables
        db.create_all()

    # Run the Flask app
    app.run(debug=True)
