from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self,data_dict):
        self.id=data_dict['id']
        self.first_name=data_dict['first_name']
        self.last_name=data_dict['last_name']
        self.email=data_dict['email']
        self.phone_number=data_dict['phone_number']
        self.password=data_dict['password']



    @classmethod
    def create(cls,data):
        query="""INSERT INTO users (first_name,last_name,email,phone_number,password)
            VALUES (%(first_name)s,%(last_name)s,%(email)s,%(phone_number)s,%(password)s);"""
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def get_by_id(cls,data):
        query="""SELECT * FROM users WHERE id=%(id)s;"""
        result=connectToMySQL(DATABASE).query_db(query,data)
        if result:
            return cls(result[0])
        return None

    @classmethod
    def get_by_email(cls,data):
        query="""SELECT * FROM users WHERE email=%(email)s;"""
        result=connectToMySQL(DATABASE).query_db(query,data)
        if result:
            return cls(result[0])
        return False
    
    @staticmethod
    def validate(data):
        is_valid=True
        if len(data['phone_number'])<8:
            is_valid=False
            flash('Phone Number must be greater than 8 digits',"reg")
        if len(data['first_name'])<2:
            is_valid=False
            flash('First Name must be greater than 2 characters',"reg")
        if len(data['last_name'])<2:
            is_valid=False
            flash('Last Name must be greater than 2 characters',"reg")
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False
        if User.get_by_email({'email':data['email']}):
            flash('Email already in use,hope by you 😊','reg')
            is_valid=False
            # PASSWORD VALIDATION:
                # LENGTH:
        if len(data['password'])<8:
            flash('Password too short','reg')
            is_valid=False
                # Confirm password:
        elif data['password']!=data['confirm_pw']:
            flash('Password must match','reg')
            is_valid=False
        return is_valid