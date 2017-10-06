from flask import Flask, request, redirect, render_template
import cgi
import os
import jinja2
import re

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    template = jinja_env.get_template('index.html')
    return template.render()

@app.route("/validate-signup", methods = ['POST'])
def validate_signup():
    username = request.form['username']
    password = request.form['password']
    verifypword = request.form['verifypword']
    email = request.form['email']

    user_error = ""
    pass_error = ""
    verifypass_error = ""
    email_error = ""    
    
    if not re.match("^[A-Za-z0-9_-]*$", username):
        user_error = "Must be between 3 and 25 characters"

    if not password.isalpha():
        pass_error = "Please enter Password"
   
    if not verifypword.isalpha():
        verifypass_error = "Please enter password"
    
    elif verifypword != password:
        verifypass_error = "Passwords do not match"
        
    if not re.match("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
        email_error = "Email must contain @ . and 3-20 characters"
    elif not email:
        email_error = "Please enter an email"
    elif email:
        email = request.form['email']

    if not pass_error and not user_error and not verifypass_error:
        template = jinja_env.get_template('welcome.html')
        return template.render(username=username)

    else:
        template = jinja_env.get_template('index.html')
        return template.render(user_error = user_error, 
                                pass_error = pass_error,
                                verifypass_error = verifypass_error,
                                email_error = email_error,
                                username = username,
                                email = email)


@app.route("/welcome", methods = ['POST'])
def welcome():
    username = request.form['username']
    template = jinja_env.get_template('welcome.html')
    return template.render(username=username)



app.run()
