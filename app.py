from flask import Flask, render_template

app = Flask(__name__, static_url_path='/static')

@app.route("/")
def home():
    return render_template('index.html')
    
@app.route("/login")
def login():
    return render_template('login.html')
    
@app.route("/signup")
def signup():
    return render_template('signup.html')
    
@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/aboutus")
def aboutus():
    return render_template('aboutus.html')

if __name__ == "__main__":
    app.run()
