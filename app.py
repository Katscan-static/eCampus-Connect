from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, UserMixin, login_required, logout_user


from models import User, User_data

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

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


@app.route('/', methods=['POST', 'GET'])
def home(): 
    """
    Handle requests to the home page.

    POST Method:
    - Validates user registration or message submission.

    GET Method:
    - Renders the home page.
    """
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
    return render_template('index.html', message=user_checked)


@app.route('/logout')
@login_required
def logout():
    """
    Handle user logout.
    """
    logout_user()
    return "Logged out"


@app.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard accessible only to logged-in users.
    """
    return "Dashboard - Only accessible to logged-in users"


if __name__ == '__main__':
    app.run(debug=True)
