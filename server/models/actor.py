from uuid import uuid4
from .base import BaseModel
from datetime import datetime
from peewee import (
    TextField,
    DateTimeField,
)


class Actor(BaseModel):
    name = TextField(null=True)
    created = DateTimeField(null=False)

    @classmethod
    def get_or_create(
        cls,
        name=None,
    ):
        if name == '' or not type(name) is str:
            raise ValueError('valid name is required')
        with cls._meta.database.atomic():
            try:
                return Actor.get(Actor.name == name)
            except Actor.DoesNotExist as ex:
                a = Actor()
                a.created = datetime.utcnow()
                a.uuid = uuid4()
                a.name = name
                a.save()
                return a

    def serialize_to_dict(self):
        return {
            'name': self.name,
            'created': self.created.timestamp(),
            'uuid': self.uuid
        }
