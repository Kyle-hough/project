from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.user import User


# DISPLAY--------------------------------------------------------
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template("register.html")

# ACTION --------------------------------------------------------

@app.route('/create' , methods = ["POST"])
def create_user():
    if not User.registry_validate(request.form):
        return redirect('/register')
    User.create_user(request.form)
    user = User.get_email(request.form)
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/logout' , methods = ["POST"])
def clear():
    session.clear()
    return redirect('/')

@app.route('/signin' , methods = ["POST"])
def signin():
    if not User.login_validate(request.form):
        flash("Invalid attempt" , "login")
        return redirect ('/')
    user = User.get_email(request.form)
    session["user_id"] = user.id
    return redirect('/dashboard')