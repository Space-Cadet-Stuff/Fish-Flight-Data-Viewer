from flask import Flask, render_template, request, redirect, url_for, session as flask_session, flash, send_file, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from setup_db import engine, User, CSVFile
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os# last time someone imported this they bricked their computer
import csv
import io# Used to read the CSV file content
import random


app = Flask(__name__)
app.secret_key = 'Youkeepusingthatword.Idonotthinkitmeanswhatyouthinkitmeans'# INCONCIEVABLE!!!!


engine = create_engine('sqlite:///datalogger.db')
Session = sessionmaker(bind=engine)
db_session = Session()  # renamed to avoid conflict


UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')# Define the index route
def homepage():
    splash = None
    splash_url = None
    try:
        with open('static/other/splash.txt', 'r', encoding='utf-8') as f:
            raw_splashes = f.read().strip().split('\n\n')
            clean_splashes = [s.strip() for s in raw_splashes if s.strip()]
            chosen = random.choice(clean_splashes)

            if chosen.startswith("[LINK]"):
                _, rest = chosen.split("[LINK]", 1)
                text, url = rest.split("|", 1)
                splash = text.strip()
                splash_url = url.strip()
            else:
                splash = chosen
    except Exception as e:
        splash = "Error 404, Splash Message not found!"
        splash_url = None

    return render_template('index.html', splash=splash, splash_url=splash_url)# Render the index page with a random splash message

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

@app.route('/upload', methods=["GET", "POST"])  # Define the route for uploading files
def upload():
    if "user_id" not in flask_session:  # Check if the user is logged in
        flash("You need to login to upload files.", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":  # Handle file upload
        title = request.form.get("title")
        launch_date = request.form.get("launchDate")
        engine_class = request.form.get("engineClass")
        file = request.files.get("csvFile")

        if not file or not file.filename.endswith('.csv'):  # Check if the file is a valid CSV
            flash("Please upload a valid CSV file.", "error")
            return redirect(request.url)

        filename = secure_filename(file.filename)  # Secure the filename using werkzeug utils

        # Attempt to read the CSV content before saving
        try:
            stream = io.StringIO(file.stream.read().decode("utf-8"))
            csv_reader = csv.reader(stream)
            test_row = next(csv_reader)  # Try to read at least one row
            if not test_row:
                raise ValueError("CSV appears to be empty or malformed.")
            stream.seek(0)  # Reset stream for saving later
            file.stream.seek(0)
        except Exception as e:
            flash("Uploaded CSV file is corrupted or unreadable. Error: " + str(e), "error")
            return redirect(request.url)

        existing_file = db_session.query(CSVFile).filter_by(filename=filename, user_id=flask_session["user_id"]).first()
        if existing_file:
            flash("You have already uploaded a document with this same filename", "error")
            return redirect(request.url)

        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(flask_session["user_id"]))
        os.makedirs(user_folder, exist_ok=True)
        filepath = os.path.join(user_folder, filename)
        file.save(filepath)  # Save the file

        csv_file = CSVFile(
            filename=filename,
            title=title,
            launch_date=launch_date,
            engine_class=engine_class,
            user_id=flask_session["user_id"]
        )
        db_session.add(csv_file)
        db_session.commit()

        flash("File uploaded successfully!", "success")
        return redirect(url_for("dashboard"))

    return render_template("upload.html")

@app.route('/download/<int:file_id>')# Define the route for downloading files
def download_file(file_id):
    csv_file = db_session.query(CSVFile).get(file_id)# Get the CSVFile instance by ID
    if not csv_file or csv_file.user_id != flask_session.get("user_id"):# Check if the file exists and if the user has permission to access it
        flash("You don't have permission to access that file.", "error")
        return redirect(url_for("dashboard"))

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], str(csv_file.user_id), csv_file.filename)# Get the file path
    return send_file(filepath, as_attachment=True)# Send the file as an attachment for download

@app.route('/delete/<int:file_id>', methods=["POST"])# Define the route for deleting files
def delete_file(file_id):
    csv_file = db_session.query(CSVFile).get(file_id)# Get the CSVFile instance by ID
    if not csv_file or csv_file.user_id != flask_session.get("user_id"):# Check if the file exists and if the user has permission to delete it
        flash("You don't have permission to delete that file.", "error")
        return redirect(url_for("dashboard"))

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], str(csv_file.user_id), csv_file.filename)# Delete the file from the filesystem
    try:# Attempt to remove the file
        os.remove(filepath)
    except FileNotFoundError:
        pass  # file might already be gone

    db_session.delete(csv_file)# Remove the database entry
    db_session.commit()# Commit the session to save the changes

    flash("File deleted successfully.", "success")
    return redirect(url_for("dashboard"))

@app.route('/visualiser')# Define the route for the visualiser
def visualiser():
    if "user_id" not in flask_session:
        flash("You need to login to access the visualiser.", "warning")
        return redirect(url_for("login"))

    user_id = flask_session["user_id"]
    user_csvs = db_session.query(CSVFile).filter_by(user_id=user_id).all()

    def get_csv_headers(filepath):# Helper function to get CSV column headers
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.readline().strip().split(",")
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return ["<error reading file>"]
        
    csv_data = []# Build the list of file data with headers
    for csv in user_csvs:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], str(user_id), csv.filename)
        headers = get_csv_headers(filepath)
        csv_data.append({# Store the CSV file metadata and headers in a dictionary
            "id": csv.id,
            "title": csv.title,
            "filename": csv.filename,
            "launch_date": csv.launch_date,
            "engine_class": csv.engine_class,
            "headers": headers
        })

    return render_template("visualiser.html", csv_data=csv_data)

@app.route('/account_settings', methods=['GET', 'POST'])# Define the route for account settings
def account_settings():
    if "user_id" not in flask_session:
        flash("You need to login to access account settings.", "warning")
        return redirect(url_for("login"))

    user = db_session.query(User).get(flask_session["user_id"])

    if request.method == "POST":# Handle form submission for updating account settings or deleting the account
        if "username" in request.form and "email" in request.form:
            new_username = request.form.get("username").strip()
            new_email = request.form.get("email").strip()
            new_password = request.form.get("password")
            confirm_password = request.form.get("confirm_password")

            # Check for username/email conflicts
            existing_user = db_session.query(User).filter(
                ((User.username == new_username) | (User.email == new_email)) & (User.id != user.id)
            ).first()
            if existing_user:# If a user with the same username or email exists, flash an error message
                flash("Username or email already taken.", "error")
                return redirect(url_for("account_settings"))

            user.username = new_username
            user.email = new_email

            if new_password:
                if new_password != confirm_password:
                    flash("Passwords do not match.", "error")
                    return redirect(url_for("account_settings"))
                user.password = generate_password_hash(new_password)

            db_session.commit()
            flask_session["username"] = user.username
            flash("Account updated successfully.", "success")
            return redirect(url_for("account_settings"))
        else:
            user_files = db_session.query(CSVFile).filter_by(user_id=user.id).all()# Handle account deletion and delete the user's files
            for csv_file in user_files:
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], str(user.id), csv_file.filename)
                try:
                    os.remove(filepath)
                except FileNotFoundError:
                    pass
                db_session.delete(csv_file)
            db_session.delete(user)
            db_session.commit()
            flask_session.clear()
            flash("Your account and all associated files have been deleted.", "info")
            return redirect(url_for("index"))

    return render_template("account_settings.html", current_user=user)

@app.route('/get_csv_data/<int:file_id>')# Allow the user to get the data from a CSV file for the graph
def get_csv_data(file_id):
    csv_file = db_session.query(CSVFile).get(file_id)
    if not csv_file or csv_file.user_id != flask_session.get("user_id"):
        return jsonify({"error": "Unauthorized or file not found"}), 403

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], str(csv_file.user_id), csv_file.filename)# Get the file path
    try:
        with open(filepath, newline='') as f:
            reader = csv.DictReader(f)
            rows = [row for row in reader]

        if rows:# Remove columns that don't contain any data
            columns = list(rows[0].keys())
            columns_with_data = [
                col for col in columns
                if any(row.get(col, "").strip() != "" for row in rows)
            ]
            filtered_rows = [# Filter out empty columns from each row
                {col: row[col] for col in columns_with_data}
                for row in rows
            ]
        else:
            filtered_rows = []

        return jsonify(filtered_rows)# Return the filtered rows as JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/florp', methods=['GET', 'POST'])
def florp():
    if "user_id" not in flask_session:
        flash("You need to login first", "warning")
        return redirect(url_for('login'))

    picked_up = False
    if "florp_picked_up" in flask_session:
        picked_up = flask_session["florp_picked_up"]

    if request.method == "POST" and request.form.get("pick_up") == "1":
        flask_session["florp_picked_up"] = True
        picked_up = True

    return render_template("florp.html", picked_up=picked_up)

@app.route('/jakito', methods=['GET', 'POST'])
def jakito():
    if "user_id" not in flask_session:
        flash("You need to login first", "warning")
        return redirect(url_for('login'))

    sacrificed = flask_session.get("jakito_sacrificed", False)
    has_florp = flask_session.get("florp_picked_up", False)

    if request.method == "POST" and has_florp and not sacrificed and request.form.get("sacrifice") == "1":
        flask_session["jakito_sacrificed"] = True
        sacrificed = True

    return render_template("jakito.html", sacrificed=sacrificed, has_florp=has_florp)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)