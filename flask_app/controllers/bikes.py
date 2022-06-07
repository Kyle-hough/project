from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.bike import Bike

# Display ------------------------------
@app.route('/create_bike')
def new():
    user = User.get_one({"id": session["user_id"]})
    return render_template("create_bike.html", user = user)

@app.route('/bike_show/<int:id>')
def show_bike(id):
    user = User.get_one({"id": session["user_id"]})
    bike = Bike.get_one({"id":id})
    return render_template("show_bike.html", user = user, bike = bike)

@app.route('/edit/bike/<int:id>')
def edit_bike(id):
    user = User.get_one({"id": session["user_id"]})
    bike = Bike.get_one({"id":id})
    return render_template("edit_bike.html", user = user, bike = bike)

@app.route('/delete/bike/<int:id>')
def delete_bike(id):
    Bike.delete_bike({"id" : id})
    return redirect('/dashboard')

# Action ------------------------------
@app.route('/create/bike' , methods = ["POST"])
def create_bike():
    if not Bike.bike_validate(request.form):
        return redirect('/create_bike')
    Bike.create(request.form)
    return redirect('/dashboard')

@app.route('/update/bike' , methods = ['POST'])
def update_bike():
    if not Bike.bike_validate(request.form):
        return redirect(f'/edit/bike/{request.form["id"]}')
    Bike.update_bike(request.form)
    return redirect('/dashboard')