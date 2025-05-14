from flask import Flask, render_template, request, redirect, url_for, session as flask_session, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from setup_db import engine, User, CSVFile
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os# last time someone imported this they 


app = Flask(__name__)
app.secret_key = 'Youkeepusingthatword.Idonotthinkitmeanswhatyouthinkitmeans'


engine = create_engine('sqlite:///datalogger.db')
Session = sessionmaker(bind=engine)
db_session = Session()  # renamed to avoid conflict


UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')# Define the index route
def index():
    return render_template('index.html')# Renders the index page

@app.route('/login', methods=["GET", "POST"])# Define the login route. Also yoinked from pervious assessment
def login():
    if request.method == "POST":# Get form data
        username = request.form.get('username')
        password = request.form.get('password')

        user = db_session.query(User).filter_by(username=username).first()# Check if the user exists and/or password is correct
        if user and check_password_hash(user.password, password):# If correct, begins session with user id and username
            flask_session["user_id"] = user.id
            flask_session["username"] = user.username
            flash("Logged in successfully", "success")
            return redirect(url_for('dashboard'))# Redirects to the dashboard
        else:# If incorrect, flashes an error message
            flash("Invalid username or password", "error")

    return render_template('login.html')# Renders the login page

@app.route('/signup', methods=["GET", "POST"])# Define the signup route
def signup():
    if request.method == "POST":# Get form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        existing_user = db_session.query(User).filter((User.username == username) | (User.email == email)).first()# Check if username or email already exists
        if existing_user:
            flash("Username or email already exists. Please choose another.", "error")
            return redirect(url_for('signup'))
        
        password = generate_password_hash(password)# Hash the password for security
        
        new_user = User(username = username, email = email, password = password)# Create a new user instance
        
        db_session.add(new_user)# Add and commit the new user to the database
        db_session.commit()
        
        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for('login'))# Redirect to the login page after successful signup
    
    return render_template('signup.html')# Render the signup page

@app.route('/dashboard')# Define the dashboard route
def dashboard():
    if "user_id" not in flask_session:# Check if the user is logged in
        flash("You need to login first", "warning")
        return redirect(url_for('index'))  # Redirect to the index page if the user is not logged in
    
    if 'first_login' in flask_session and flask_session['first_login']:# Check if it's the first time visiting the dashboard after login or logout
        flash("Welcome back, {}!".format(flask_session["username"]), "info")
        flask_session['first_login'] = False  # Set 'first_login' to False after showing the message

    user_id = flask_session["user_id"]# Get the current user's ID from the session
    files = db_session.query(CSVFile).filter_by(user_id=user_id).all()# Query the database for files uploaded by the current user
    
    return render_template('dashboard.html', user_id=flask_session["user_id"], username=flask_session["username"], files=files)# Render the dashboard page and store the current user's id and username in the session

@app.route('/logout')# Defines the logout route
def logout():
    flask_session.clear()# Clears the session
    flash("You have been logged out", "info")
    return redirect(url_for('index'))# Redirects to the index page

@app.route('/set_theme', methods=['POST'])# Define the route allowing the user to choose a theme
def set_theme():
    selected_theme = request.form.get('theme')# Get the selected theme from the form
    flask_session['theme'] = selected_theme# Store the selected theme in the session
    return redirect(request.referrer or url_for('index'))

@app.route('/upload', methods=["GET", "POST"])# Define the route for uploading files
def upload():
    if "user_id" not in flask_session:# Check if the user is logged in
        flash("You need to login to upload files.", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":# Handle file upload
        title = request.form.get("title")
        launch_date = request.form.get("launchDate")
        engine_class = request.form.get("engineClass")
        file = request.files.get("csvFile")

        if not file or not file.filename.endswith('.csv'):# Check if the file is a valid CSV
            flash("Please upload a valid CSV file.", "error")
            return redirect(request.url)

        filename = secure_filename(file.filename)# Secure the filename using werkzeug utils
        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(flask_session["user_id"]))# Create a user-specific folder
        os.makedirs(user_folder, exist_ok=True)# Create the folder if it doesn't exist
        filepath = os.path.join(user_folder, filename)# Save the file to the user-specific folder
        file.save(filepath)# Save the file

        csv_file = CSVFile(# Create a new CSVFile instance
            filename=filename,
            title=title,
            launch_date=launch_date,
            engine_class=engine_class,
            user_id=flask_session["user_id"]
        )
        db_session.add(csv_file)# Add the new CSVFile instance to the session
        db_session.commit()# Commit the session to save the file information to the database

        flash("File uploaded successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("upload.html")


if __name__ == '__main__':
    app.run(debug=True)