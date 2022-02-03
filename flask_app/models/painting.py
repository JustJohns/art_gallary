from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

from flask_app.models import artist

class Painting:
    db = "artist_paintings_schema"

    def __init__(self, data):
        self.id = data['id']

        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        self.artist_id = data['artist_id']

        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.artist = {}

    @staticmethod
    def validate_painting(data):
        is_valid = True
        if len(data["title"]) < 2:
            flash("Painting Title must be at least 2 characters long!")
            is_valid = False
        if len(data["description"]) < 10:
            flash("Description must be at least 10 characters!")
            is_valid = False

        if data["price"] == "":
            flash("Please input price!")
        elif int(data["price"]) < 0:
            flash("Painting price must be at least 1 dollar!")
            is_valid = False

        return is_valid

    # ============================================
    # 1. Creat one painting in database
    # ============================================

    @classmethod
    def create_painting(cls, data):
        query = """
        INSERT INTO paintings (title, description, price, artist_id, created_at) 
        VALUES (%(title)s, %(description)s, %(price)s, %(artist_id)s, NOW());
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)
        return results

    # ============================================
    # 2. Get all paintings from database
    # ============================================
    # Now we use class methods to query our database
    @classmethod
    def get_all(cls):
        query = """SELECT * FROM paintings
                LEFT JOIN artists 
                ON paintings.artist_id = artists.id;"""
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        # Create an empty list to append our instances of friends
        all_paintings = []
        # Iterate over the db results and create instances of friends with cls.
        for painting_data in results:
            painting = cls(painting_data)

            artist_data = {
                "id" : painting_data["artists.id"],

                "first_name" : painting_data["first_name"],
                "last_name" : painting_data["last_name"],
                "email" : painting_data["email"],
                "password" : painting_data["password"],

                "created_at" : painting_data["artists.created_at"],
                "updated_at" : painting_data["artists.updated_at"]
            }
            painting.artist = artist.Artist(artist_data)
            all_paintings.append(painting)
        return all_paintings


    @classmethod
    def get_painting_with_artist(cls, data):
        query = """SELECT * FROM paintings
                LEFT JOIN artists 
                ON paintings.artist_id = artists.id
                WHERE paintings.id = %(painting_id)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)

        painting = cls(results[0])
        artist_data = {
                "id" : results[0]["artists.id"],

                "first_name" : results[0]["first_name"],
                "last_name" : results[0]["last_name"],
                "email" : results[0]["email"],
                "password" : results[0]["password"],

                "created_at" : results[0]["artists.created_at"],
                "updated_at" : results[0]["artists.updated_at"]
            }
        painting.artist = artist.Artist(artist_data)
        return painting

    @classmethod
    def update_painting_info(cls, data):
        query = """UPDATE paintings 
            SET title = %(title)s, description = %(description)s, price = %(price)s, updated_at = NOW()
            WHERE id = %(painting_id)s"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return

    @classmethod
    def delete_painting(cls, data):
        query = "DELETE FROM paintings WHERE id = %(painting_id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return
        