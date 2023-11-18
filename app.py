from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, UserMixin, login_required, logout_user, current_user
import os
from werkzeug.utils import secure_filename  #for secure_filename

from models import User, User_data

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

UPLOAD_FOLDER = 'static/css/upload'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """
    Load a user by its ID from the database.

    Args:
    - user_id: The ID of the user

    Returns:
    - User object if found, otherwise None
    """
    user = User_data(user_id)
    user_data = user.query_user_by_id()
    if user_data:
        return User(user_data)
    return None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['POST', 'GET'])
def home(): 
    """
    Handle requests to the home page.

    POST Method:
    - Validates user registration or message submission.

    GET Method:
    - Renders the home page.
    """
    if current_user.is_authenticated:
            return redirect(url_for("dashboard"))
    if request.method == 'POST':
        user_data = request.form.to_dict()
        user = User(user_data)
        check_user = user.check_email()
        if not check_user and user_data['submit'] != 'Send Message':
            user.save_to_db()
            message = "User has been registered, please kindly login"
        elif user_data["submit"] == 'Send Message':
            user.save_to_db()
            message = "Your message has been sent, thank you for contacting us! We will respond ASAP!"
        else:
            message = "User already exists, please login"
        return render_template("index.html", message=message)
    return render_template('index.html')
    

@app.route('/login', methods=['POST', 'GET'])
def login():
    """
    Handle user login.

    POST Method:
    - Validates user credentials and logs in if successful.
    """
    if request.method == 'POST':
        user_data = request.form.to_dict()
        user = User(user_data)
        user_checked = user.pw_compare()
        if isinstance(user_checked, User):
            login_user(user_checked)
            return redirect(url_for("dashboard"))
        else:
            return render_template('index.html', message=user_checked)
    return redirect(url_for('home'))

"""
    Trying to Upload Profile picture
"""
@app.route('/static/css/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File uploaded successfully'
    else:
        return 'Invalid file'


@app.route('/logout')
@login_required
def logout():
    """
    Handle user logout.
    """
    logout_user()
    return redirect(url_for('home'))

"""
    Render the dashboard accessible only to logged-in users.
"""
@app.route('/dashboard')
@login_required
def dashboard():

    # Access the current user's ID using current_user
    user_id = current_user.get_id()
    
    # Get the User_data object
    user_data = User_data(user_id)
    
    # Access the full name from the database
    full_name = user_data.get_full_name()
    # Access the email from the database
    email = user_data.get_email()
    # Access the phone_number from the database
    phone_number = user_data.get_phone_number()

    # Access the profile picture filename from the database
    profile_picture_filename = current_user.profile_picture
   
    return render_template("dashboard/index.html", full_name=full_name, email=email, phone_number=phone_number, profile_picture_filename=profile_picture_filename)

@app.route('/upload_profile_picture', methods=['POST'])
@login_required
def upload_profile_picture():
    if 'profile_picture' in request.files:
        file = request.files['profile_picture']
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
            current_user.profile_picture = secure_filename(file.filename)
            current_user.save_to_db()

    return redirect(url_for('dashboard'))

@app.route('/timetable')
@login_required
def timetable():
    """
    Render the dashboard accessible only to logged-in users.
    """
    return render_template("dashboard/timetable.html")

@app.route('/events')
@login_required
def events():
    """
    Render the dashboard accessible only to logged-in users.
    """
    return render_template("dashboard/events.html")
    
@app.route('/password')
@login_required
def password():
    """
    Render the dashboard accessible only to logged-in users.
    """
    return render_template("dashboard/password.html")
    
@app.route('/exam')
@login_required
def exam():
    """
    Render the dashboard accessible only to logged-in users.
    """
    return render_template("dashboard/exam.html")
    

@app.route('/index_ds')
@login_required
def index_ds():
    """
    Render the dashboard accessible only to logged-in users.
    """
    return redirect(url_for("dashboard"))

if __name__ == '__main__':
    app.run(debug=True)
