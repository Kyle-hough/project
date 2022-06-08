from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app.models import user

class Bike:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.price = data['price']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO bikes (user_id, name, price, description) VALUES (%(user_id)s, %(name)s, %(price)s, %(description)s); "
        return connectToMySQL("project_db").query_db(query, data)

    @classmethod
    def update_bike(cls, data):
        query = "UPDATE bikes SET name = %(name)s, price = %(price)s, description = %(description)s WHERE id = %(id)s;"
        connectToMySQL("project_db").query_db(query, data)

    @classmethod
    def delete_bike(cls, data):
        query = "DELETE FROM bikes WHERE id = %(id)s;"
        connectToMySQL("project_db").query_db(query,data)
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM bikes JOIN users ON bikes.user_id = users.id WHERE bikes.id = %(id)s;"
        results = connectToMySQL("project_db").query_db(query, data)
        if results:
            for row in results:
                temp_trail = cls(results[0])
                user_data = {
                    "id" : row['users.id'],
                    "first_name" : row['first_name'],
                    "last_name" : row['last_name'],
                    "email" : row['email'],
                    "password" : row['password'],
                    "created_at" : row['users.created_at'],
                    "updated_at" : row['users.updated_at']
                }
            temp_trail.creator= user.User(user_data)
            return temp_trail
        

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM bikes JOIN users on bikes.user_id = users.id;"
        results = connectToMySQL("project_db").query_db(query)
        all_bikes = []
        if results:
            for row in results:
                temp_bike = cls(row)
                user_data = {
                    "id" : row['users.id'],
                    "first_name" : row['first_name'],
                    "last_name" : row['last_name'],
                    "email" : row['email'],
                    "password" : row['password'],
                    "created_at" : row['users.created_at'],
                    "updated_at" : row['users.updated_at']
                }
                temp_bike.creator = user.User(user_data)
                all_bikes.append(temp_bike)
        return all_bikes


    @staticmethod
    def bike_validate(data):
        is_valid = True
        if len(data['name']) <= 3:
            flash("Name must be greater than one character." , "bike")
            is_valid = False
        if data['price'].isnumeric():
            if int(data['price']) < 1000:
                is_valid = False
                flash("Enter a price", "bike")
        else:
            is_valid = False
            flash("Must be a number")
        if len(data['description']) <= 3:
            flash("Description must be three characters." , "bike")
            is_valid = False
        return is_valid