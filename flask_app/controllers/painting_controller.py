from flask_app import app
from flask import render_template, redirect, session, request, flash

from flask_app.models.painting import Painting

from flask_app.models.artist import Artist

#============================================
# 1. Add painting route
#============================================

@app.route("/paintings/new")
def add_painting():
    # artists = Artist.get_all()

    # print(artists)

    # for artist in artists:
    #     print(artist.first_name)
    if "artist_id" not in session:
        flash("Please login or register before entering the site")
        return redirect("/")


    return render_template("new_painting.html", artist_id = session["artist_id"])

@app.route("/paintings/create_painting", methods=["POST"])
def create_painting():
    
    #1 validate form data
    data = {
        "title" : request.form['title'],
        "description" : request.form['description'],
        "price" : request.form['price'],
        "artist_id" : request.form['artist_id']
    }

    if not Painting.validate_painting(data):
        return redirect("/paintings/new")
    
    #2 save new painting to database
    Painting.create_painting(data)
        
    #3 if successful, redirect to render route
    return redirect("/paintings")

#============================================
# 2. Show painting route
#============================================

@app.route("/paintings/<int:painting_id>")
def show_painting(painting_id):
    if "artist_id" not in session:
        flash("Please login or register before entering the site")
        return redirect("/")
    # query info w/ info of artist
    data = {
        "painting_id" : painting_id
    }

    painting = Painting.get_painting_with_artist(data)
    # send to show page

    return render_template("show_painting.html", painting = painting)

#============================================
# 3. Edit painting route
#============================================

@app.route("/painting/<int:painting_id>/edit")
def edit_painting(painting_id):
    data = {
        "painting_id" : painting_id
    }
    painting = Painting.get_painting_with_artist(data)

    return render_template("edit_painting.html", painting = painting)

@app.route("/painting/<int:painting_id>/update", methods=['POST'])
def update_painting(painting_id):
    data = {
        "title" : request.form["title"],
        "description" : request.form["description"],
        "price" : request.form["price"],
        "painting_id" : painting_id
    }
    if not Painting.validate_painting(data):
        return redirect(f"/painting/{painting_id}/edit")

    Painting.update_painting_info(data)

    return redirect("/paintings")

#============================================
# 4. Delete painting route
#============================================

@app.route("/painting/delete/<int:painting_id>")
def delete_painting(painting_id):
    data = {
        "painting_id" : painting_id
    }
    Painting.delete_painting(data)
    return redirect("/paintings")