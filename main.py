from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
import requests
from dotenv import load_dotenv
import os

load_dotenv(".env")  # loads the environment file
MOVIEDB_API_KEY = os.getenv("MOVIEDB_API_KEY")
MOVIE_DB_IMG_URL = "https://image.tmdb.org/t/p/w500/"

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
Bootstrap(app)

# CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(300), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)


db.create_all()

# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
#
# db.session.add(new_movie)
# db.session.commit()


class MovieForm(FlaskForm):
    rating = FloatField('Your Rating Out of 10 e.g. 7.5', validators=[DataRequired()])
    review = StringField('Your Review ', validators=[DataRequired()])
    submit = SubmitField('Submit')


class AddMovieForm(FlaskForm):
    title = StringField('Movie Title ', validators=[DataRequired()])
    submit = SubmitField('Add Movie')


@app.route("/")
def home():
    # This line creates a list of all the movies sorted by rating
    all_movies = Movie.query.order_by(Movie.rating).all()

    # This line loops through all the movies
    for i in range(len(all_movies)):
        # This line gives each movie a new ranking reversed from their order in all_movies
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", movies=all_movies)


@app.route("/edit", methods=['GET', 'POST'])
def edit():
    form = MovieForm()
    movie_id = request.args.get('id')
    if form.validate_on_submit():
        new_rating = form.rating.data
        new_review = form.review.data
        movie_to_update = Movie.query.get(movie_id)
        movie_to_update.rating = new_rating
        movie_to_update.review = new_review
        db.session.commit()
        return redirect(url_for('home'))

    movie_to_edit = Movie.query.get(movie_id)

    return render_template("edit.html", form=form, movie=movie_to_edit)


@app.route("/add", methods=['GET', 'POST'])
def add():
    form = AddMovieForm()
    if form.validate_on_submit():
        parameters = {
            'api_key': MOVIEDB_API_KEY,
            'query': form.title.data
        }
        response = requests.get(url="https://api.themoviedb.org/3/search/movie", params=parameters)
        data_response = response.json()
        results = data_response['results']
        print(data_response)
        return render_template('select.html', choices=results)
    return render_template('add.html', form=form)


@app.route("/delete")
def delete():
    movie_id = request.args.get('id')  # gets the id from the query parameters
    movie_to_delete = Movie.query.get(movie_id)  # get the movie to be deleted
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/find")
def find():
    movie_id = request.args.get('id')
    if movie_id:
        parameters = {
            'api_key': MOVIEDB_API_KEY
        }
        response = requests.get(url=f"https://api.themoviedb.org/3/movie/{movie_id}", params=parameters)
        data_response = response.json()
        title = data_response['original_title']
        image_url = f"{MOVIE_DB_IMG_URL}{data_response['poster_path']}"
        # The data in release_date includes month and day, we will want to get rid of.
        year = data_response['release_date'].split("-")[0]
        description = data_response['overview']

        new_movie = Movie(title=title, year=year, img_url=image_url, description=description)
        db.session.add(new_movie)
        db.session.commit()
        movie = Movie.query.filter_by(title=title).first()
        db_id = movie.id
        return redirect(url_for('edit', id=db_id))


if __name__ == '__main__':
    app.run(debug=True)
