from uuid import uuid4
from .base import BaseModel
from datetime import datetime
from peewee import (
    TextField,
    DateTimeField,
)


class Movie(BaseModel):
    title = TextField(null=False)
    genre = TextField(null=True)
    created = DateTimeField(null=False)

    @classmethod
    def get_or_create(
        cls,
        title=None,
        genre=None
    ):
        if title == '' or not type(title) is str:
            raise ValueError('valid title is required')
        with cls._meta.database.atomic():
            try:
                return Movie.get(Movie.title == title)
            except Movie.DoesNotExist as ex:
                m = Movie()
                m.created = datetime.utcnow()
                m.uuid = uuid4()
                m.title = title
                m.genre = genre
                m.save()
                return m

    def serialize_to_dict(self):
        return {
            'title': self.title,
            'genre': self.genre,
            'created': self.created.timestamp(),
            'uuid': self.uuid
        }
