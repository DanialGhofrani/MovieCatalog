from server.models.actor import Actor
from ..base import ModelTestCase


class TestActor(ModelTestCase):

    def test_get_or_create_1(self):
        """ test successful get or create"""
        all_actors = Actor.select()
        self.assertEqual(0, len(all_actors))
        actor = Actor.get_or_create(
            name='nicole kidman',
        )
        # check actor object returned:
        self.assertEqual('nicole kidman', actor.name)

        # fetch actor from database:
        # get implicitly asserts that there is exactly 1 actor:
        actor = Actor.get()
        self.assertEqual('nicole kidman', actor.name)

        # trying to insert the same actor will not create a new one:
        actor = Actor.get_or_create(
            name='nicole kidman',
        )
        self.assertEqual('nicole kidman', actor.name)
        actor = Actor.get()
        self.assertEqual('nicole kidman', actor.name)

        # but if the name is different, another actor is created:
        actor = Actor.get_or_create(
            name='tom cruise',
        )
        self.assertEqual('tom cruise', actor.name)

        # and now there are two actors:
        all_actors = Actor.select()
        self.assertEqual(len(all_actors), 2)

        Actor.get(Actor.name == 'nicole kidman')
        Actor.get(Actor.name == 'tom cruise')

    def test_get_or_create_2(self):
        """ test creation of actor with invalid name"""
        all_actors = Actor.select()
        self.assertEqual(0, len(all_actors))

        with self.assertRaises(ValueError):
            Actor.get_or_create(
                name=None,
            )

        # empty string will fail:
        with self.assertRaises(ValueError):
            Actor.get_or_create(
                name='',
            )

        # any non string will fail:
        with self.assertRaises(ValueError):
            Actor.get_or_create(
                name=123,
            )
