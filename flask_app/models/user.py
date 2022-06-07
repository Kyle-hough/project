from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_user(cls, data):
        hashed = bcrypt.generate_password_hash(data['password'])
        hashed_dict = {
            "first_name": data['first_name'],
            "last_name" : data['last_name'],
            "email" : data['email'],
            "password" : hashed
        }
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s , %(last_name)s , %(email)s , %(password)s);"
        return connectToMySQL("project_db").query_db(query, hashed_dict)

    @classmethod
    def get_email(cls ,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("project_db").query_db(query, data)
        if results:
            return cls(results[0])
    
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        results = connectToMySQL("project_db").query_db(query, data)
        if results:
            return cls(results[0])

    @staticmethod
    def login_validate(data):
        user = User.get_email(data)
        if not user:
            return False
        if not bcrypt.check_password_hash(user.password, data['password']):
            return False
        return True

    @staticmethod
    def registry_validate(data):
        is_valid = True
        
        if len(data['first_name']) <= 1:
            flash("First Name must be greater than one character." , "register")
            is_valid = False

        if len(data['last_name']) <= 1:
            flash("Last Name must be greater than one character." , "register")
            is_valid = False
        
        user = User.get_email(data)
        if user:
            flash("Email is taken" , "register")
            is_valid = False
        
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid Email" , "register")
            is_valid = False

        if len(data['password']) < 7:
            flash("Password must be greater than 7 characters." , "register")
            is_valid= False
        
        if data['password'] != data['confirm_password']:
            flash("Password does not match" , "register")
            is_valid = False
        
        return is_valid