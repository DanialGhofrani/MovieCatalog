from flask import Flask
from views.index import indexGet
from api.movie import create_movie, get_movies
from models import Movie, Actor, MovieActor
from databases import PostgresDB


def init():
    PostgresDB.initialize_postgres()
    if not Movie.table_exists():
        Movie.create_table()
    if not Actor.table_exists():
        Actor.create_table()
    if not MovieActor.table_exists():
        MovieActor.create_table()


app = Flask(__name__, static_folder="../static/dist", template_folder="../static/templates")
app.secret_key = 'super secret key goes here blah blah'

# API URLS:
app.add_url_rule(
    '/movie/',
    'createMovie',
    create_movie,
    methods=['POST'],
    strict_slashes=True,
)

app.add_url_rule(
    '/movie/',
    'getMovies',
    get_movies,
    methods=['GET'],
    strict_slashes=True,
)

# View layer URLS:
app.add_url_rule(
    '/',
    'index',
    indexGet,
    methods=['GET'],
    strict_slashes=True,
)

if __name__ == "__main__":
    init()
    app.run(host='0.0.0.0', port=5555)
