from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.trail import Trail
from flask_app.models.bike import Bike

# Display------------------------------------------------------------------------
@app.route('/dashboard')
def dashboard():
    user = User.get_one({"id": session["user_id"]})
    trails = Trail.get_all()
    bikes = Bike.get_all()
    return render_template("dashboard.html", user = user, all_trails = trails, all_bikes = bikes)

@app.route('/create_trail')
def create():
    user = User.get_one({"id": session["user_id"]})
    return render_template("create_trail.html" , user = user)

@app.route('/trail_show/<int:id>')
def show_trail(id):
    user = User.get_one({"id": session["user_id"]})
    trail = Trail.get_one({"id":id})
    return render_template("show_trail.html", user = user, trail = trail)

@app.route('/edit/trail/<int:id>')
def edit_trail(id):
    user = User.get_one({"id": session["user_id"]})
    trail = Trail.get_one({"id":id})
    return render_template("edit_trail.html", user = user, trail = trail)

@app.route('/delete/trail/<int:id>')
def delete_trail(id):
    Trail.delete_trail({"id": id})
    return redirect('/dashboard')

# Action ----------------------------------------------------------------
@app.route('/create/trail' , methods = ['POST'])
def create_trail():
    if not Trail.trail_validate(request.form):
        return redirect('/create_trail')
    Trail.create(request.form)
    return redirect('/dashboard')

@app.route('/update/trail' , methods = ['POST'])
def update_trail():
    if not Trail.trail_validate(request.form):
        return redirect(f'/edit/trail/{request.form["id"]}')
    Trail.update_trail(request.form)
    return redirect('/dashboard')