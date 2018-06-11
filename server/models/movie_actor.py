from uuid import uuid4
from .base import BaseModel
from datetime import datetime
from .movie import Movie
from .actor import Actor
from peewee import (
    TextField,
    DateTimeField,
    ForeignKeyField
)


class MovieActor(BaseModel):
    """ used to capture the many to many relationship between movies and actors"""
    actor = ForeignKeyField(Actor)
    movie = ForeignKeyField(Movie)
    created = DateTimeField(null=False)

    @classmethod
    def get_or_create(
        cls,
        movie_uuid=None,
        actor_uuid=None,
    ):
        if movie_uuid is None or actor_uuid is None:
            raise ValueError('valid movie and actor ids required')
        with cls._meta.database.atomic():
            # TODO: are these reqd?
            actor = None
            movie = None
            try:
                movie = Movie.get(Movie.uuid == movie_uuid)
            except Movie.DoesNotExist:
                raise ValueError('movie was not found')

            try:
                actor = Actor.get(Actor.uuid == actor_uuid)
            except Actor.DoesNotExist:
                raise ValueError('actor was not found')

            try:
                # here we are forced to use the int ids due to peewee Foreign Key magic
                return MovieActor.get(
                    (MovieActor.movie == movie) &
                    (MovieActor.actor == actor)
                )
            except MovieActor.DoesNotExist:
                ma = MovieActor()
                ma.created = datetime.utcnow()
                ma.uuid = uuid4()
                ma.movie = movie
                ma.actor = actor
                ma.save()
                return ma

