from server.models import Movie, Actor, MovieActor
from ..base import ModelTestCase


class TestMovieActor(ModelTestCase):
    def test_bad_movie(self):
        """ cannot create MovieActor record when movie does not exist"""
        actor = Actor.get_or_create(name='nicole kidman')
        with self.assertRaises(ValueError):
            MovieActor.get_or_create(
                movie_uuid='bad uuid',
                actor_uuid=actor.uuid
            )

    def test_bad_actor(self):
        """ cannot create MovieActor record when actor does not exist"""
        movie = Movie.get_or_create(title='lion king', genre='drama')
        with self.assertRaises(ValueError):
            MovieActor.get_or_create(
                movie_uuid=movie.uuid,
                actor_uuid='badvalue'
            )

    def test_create(self):
        """ new MovieActor will be created when no match already exists"""
        movie = Movie.get_or_create(title='lion king', genre='drama')
        actor = Actor.get_or_create(name='nicole kidman')
        ma = MovieActor.get_or_create(
            movie_uuid=movie.uuid,
            actor_uuid=actor.uuid
        )

        # implicitly assert that only one record is in the database
        ma_from_db = MovieActor.get()
        self.assertEqual(ma_from_db.uuid, str(ma.uuid))

        # confirm that trying to get or create with the same movies
        # will not create a duplicate:
        ma = MovieActor.get_or_create(
            movie_uuid=movie.uuid,
            actor_uuid=actor.uuid
        )
        ma_from_db = MovieActor.get()
        self.assertEqual(ma_from_db.uuid, str(ma.uuid))