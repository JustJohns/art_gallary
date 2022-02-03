from flask_app import app
from flask import render_template, redirect, request, session, flash

from flask_app.models.artist import Artist
from flask_app.models.painting import Painting

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")


# ===========================================
# Register / Login Routes
# ===========================================

@app.route("/register", methods=['POST'])
def register():
    # 1 validating form information
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : request.form["password"],
        "pass_conf" : request.form["pass_conf"]
    }

    if not Artist.validate_register(data):
        return redirect("/")
    # 2 bcrypt password
    data["password"] = bcrypt.generate_password_hash(request.form['password'])

    # 3 save new owner to db
    new_artist_id = Artist.create_artist(data)

    # 4 enter owner id into session and redirect to dashboatd
    session["artist_id"] = new_artist_id
    return redirect("/paintings")

@app.route("/login", methods=["POST"])
def login():
    # 1 validate Login info
    data = {
        "email" : request.form["email"],
        "password" : request.form["password"]
    }

    if not Artist.validate_login(data):
        return redirect("/")
    # 2 query for artist info based on email
    artist = Artist.get_by_email(data)


    # 3 put artist id into session and redirect to dashboard
    session["artist_id"] = artist.id
    return redirect("/paintings")

# ===========================================
# Render Dashboard Route
# ===========================================

@app.route("/paintings")
def dashboard():
    if "artist_id" not in session:
        flash("Please login or register before entering the site")
        return redirect("/")

    data = {
        "artist_id" : session["artist_id"]
    }
    artist = Artist.get_by_id(data)
    all_paintings = Painting.get_all()

    return render_template("dashboard.html", artist = artist, all_paintings = all_paintings)

# ===========================================
# Show artist Route
# ===========================================

@app.route('/paintings')
def get_all():

    artists = Artist.get_all()

    print(artists)

    for artist in artists:
        print(artist.name)

    return render_template('dashboard.html', artists = artists)

# ===========================================
# Logout Route
# ===========================================

@app.route("/logout")
def logout():
    session.clear()
    flash("Successfully logged out")
    return redirect("/")

