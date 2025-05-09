from flask import Flask, render_template, request, redirect, url_for, session as flask_session
from sqlalchemy.orm import sessionmaker
from setup_db import engine, User
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.secret_key = 'some_random_secret'  # Needed for Flask sessions to work

Session = sessionmaker(bind=engine)
db_session = Session()  # renamed to avoid conflict

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db_session.query(User).filter_by(username=username).first()
        if user and user.check_password(password):
            return render_template('dashboard.html', username=username, message="Login successful!")
        else:
            return "Invalid username or password", 401

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match", 400

        if db_session.query(User).filter_by(username=username).first() or db_session.query(User).filter_by(email=email).first():
            return "Username or email already exists", 400

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db_session.add(new_user)
        db_session.commit()

        return render_template('login.html', message="User created successfully! Please log in.")

    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    username = request.args.get('username')
    if not username:
        return render_template('index.html')
    return render_template('dashboard.html', username=username)

@app.route('/logout')
def logout():
    return render_template('index.html')

@app.route('/set_theme', methods=['POST'])
def set_theme():
    selected_theme = request.form.get('theme')
    flask_session['theme'] = selected_theme
    return redirect(request.referrer or url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)