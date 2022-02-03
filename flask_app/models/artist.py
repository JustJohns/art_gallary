from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Artist:
    db = "artist_paintings_schema"
    def __init__(self, data):
        self.id = data["id"]

        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]

        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @staticmethod
    def validate_register(data):
        is_valid = True
        if len(data["first_name"]) < 2:
            flash("First Name must be at least 2 characters long!")
            is_valid = False
        if len(data["last_name"]) < 2:
            flash("Last Name must be at least 2 characters long!")
            is_valid = False

        if not EMAIL_REGEX.match(data["email"]):
            flash("Invalid Email")
            is_valid = False
        if Artist.get_by_email(data):
            flash("Email already in use! Try new email/login")
            is_valid = False

        if len(data["password"]) < 8:
            flash("Password must be at least 8 characters long!")
            is_valid = False
        if data["password"] != data["pass_conf"]:
            flash("Password and Password Confirmation must match!")
            is_valid = False

        return is_valid


    @staticmethod
    def validate_login(data):
        is_valid = True

        artist_in_db = Artist.get_by_email(data)
        # user is not registered in the db
        if not artist_in_db:
            flash("Invalid Email")
            is_valid = False
        elif not bcrypt.check_password_hash(artist_in_db.password, data['password']):
            # if we get False after checking the password
            flash("Invalid Password")
            is_valid = False

        return is_valid



    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM artists WHERE id = %(artist_id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM artists WHERE email = %(email)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def create_artist(cls, data):
        query = """
            INSERT INTO artists (first_name, last_name, email, password, created_at) 
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW());"""
        results = connectToMySQL(cls.db).query_db(query,data)
        return results

    #============================================
    # Get all Users from database
    #============================================
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM artists;"
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        # Create an empty list to append our instances of friends
        artists = []
        # Iterate over the db results and create instances of friends with cls.
        for artist_data in results:
            artists.append( cls(artist_data) )
        return artists