from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_app.models import user

class Trail:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.city = data['city']
        self.state = data['state']
        self.difficulty = data['difficulty']
        self.what_type = data['what_type']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO trails (user_id, name, city, state, difficulty, what_type) VALUES (%(user_id)s, %(name)s, %(city)s, %(state)s, %(difficulty)s, %(what_type)s); "
        return connectToMySQL("project_db").query_db(query, data)
    
    @classmethod
    def update_trail(cls, data):
        query = "UPDATE trails SET name = %(name)s, city = %(city)s, state = %(state)s, difficulty = %(difficulty)s, what_type = %(what_type)s WHERE id = %(id)s;"
        connectToMySQL("project_db").query_db(query, data)
    
    @classmethod
    def delete_trail(cls, data):
        query = "DELETE FROM trails WHERE id = %(id)s;"
        connectToMySQL("project_db").query_db(query,data)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM trails JOIN users on trails.user_id = users.id WHERE trails.id = %(id)s;"
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
        query = "SELECT * FROM trails JOIN users on trails.user_id = users.id;"
        results = connectToMySQL("project_db").query_db(query)
        all_trails = []
        if results:
            for row in results:
                temp_trail = cls(row)
                user_data = {
                    "id" : row['users.id'],
                    "first_name" : row['first_name'],
                    "last_name" : row['last_name'],
                    "email" : row['email'],
                    "password" : row['password'],
                    "created_at" : row['users.created_at'],
                    "updated_at" : row['users.updated_at']
                }
                temp_trail.creator = user.User(user_data)
                all_trails.append(temp_trail)
        return all_trails

    @staticmethod
    def trail_validate(data):
        is_valid = True
        if len(data['name']) <= 3:
            flash("Name must be greater than one character." , "trail")
            is_valid = False
        if len(data['city']) == 0:
            flash("Choose a city", "trail")
            is_valid = False
        if len(data['state']) != 2:
            flash("State must be two characters." , "trail")
            is_valid = False
        if len(data['difficulty']) == "":
            flash("Please select a difficulty." , "trail")
            is_valid = False
        if "what_type" in data:
            if data['what_type'] not in ["Downhill", "X-Cross"]:
                flash("Please select a valid type." , "trail")
                is_valid = False
        else:
            flash("Please select a type." , "trail")
            is_valid = False
        return is_valid