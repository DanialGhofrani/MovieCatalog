from flask import request, jsonify
from models import (
    Movie,
    Actor,
    MovieActor
)


def create_movie():
    data_json = request.get_json()
    title = data_json.get('title')
    genre = data_json.get('genre')
    if title is None:
        return 'valid title is required', 400
    if genre is None:
        return 'valid genre is required', 400
    m = Movie.get_or_create(
        title=title,
        genre=genre
    )
    actor_names = data_json.get('actors')
    if actor_names is not None:
        for actor_name in actor_names:
            a = Actor.get_or_create(actor_name)
            MovieActor.get_or_create(
                actor_uuid=a.uuid,
                movie_uuid=m.uuid
            )
    return jsonify(m.serialize_to_dict()), 200


def get_movies():
    genre_filter = request.args.get('genre')
    actor_filter = request.args.get('actor')

    movies = Movie.select()
    # performance improvement can be made by having slightly uglier code
    if actor_filter is not None:
        movies = movies.join(MovieActor).join(Actor).where(
            Actor.name == actor_filter
        )
    if genre_filter is not None:
        movies = movies.where(
            Movie.genre == genre_filter
        )
    return jsonify([movie.serialize_to_dict() for movie in movies])
