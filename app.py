from flask import Flask, render_template, request
from data_handler import DataHandler

app = Flask(__name__, static_url_path='/static')

@app.route("/")
def home():
    return render_template('index.html')
    
@app.route("/login",methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        login = request.form.to_dict()
        login_DH = DataHandler(login)
        test = login_DH.pw_compare()
        return test
    return render_template('login.html')
    
@app.route("/signup", methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':
        signup = request.form.to_dict()
        signup_DH = DataHandler(signup)
        if signup_DH.check_email():
            return render_template('signup.html', message = "User Already Exists Please login")
        signup_DH.insert()
        return render_template('signup_confirm.html', signup = signup)
    return render_template('signup.html')
    
@app.route("/contact",methods = ['POST','GET'])
def contact():
    if request.method == "POST":
        contact = request.form
        print(contact)
        return render_template('thankyou.html', contact = contact)
       
    return render_template('contact.html')

@app.route("/aboutus")
def aboutus():
    return render_template('aboutus.html')
    
@app.route("/contact_us",methods = ['POST','GET'])
def contact_us():
    if request.method == "POST":
        contact = request.form
        print(contact)
    

if __name__ == "__main__":
    app.run()
