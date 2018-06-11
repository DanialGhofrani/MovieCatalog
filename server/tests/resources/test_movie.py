from server.models import (
    Movie,
    Actor,
    MovieActor
)
from ..base import EndpointTestCase


#  TODO: all of these urls should be fetched from settings file
class TestMovies(EndpointTestCase):
    """test the movie endpoint"""
    def test_get_empty(self):
        """test GET all movies when database is empty"""
        all_movies = Movie.select()
        self.assertEqual(0, len(all_movies))
        res = self.test_client.get('http://localhost:5555/movie/')
        self.assertEqual(res.status_code, 200)

    def test_get_1(self):
        """test GET all movies"""
        alice = Movie.get_or_create(
            title='alice in wonderland',
            genre='mystery'
        )
        minions = Movie.get_or_create(
            title='minions',
            genre='comedy'
        )
        res = self.test_client.get('http://localhost:5555/movie/')
        self.assertEqual(res.status_code, 200)
        all_movies = res.json

        # sort movies by title
        all_movies.sort(
            key=lambda t: t.get('title')
        )

        self.assertEqual(len(all_movies), 2)
        self.assertEqual(
            all_movies[0].get('title'), 'alice in wonderland'
        )
        self.assertEqual(
            all_movies[0].get('genre'), 'mystery'
        )
        self.assertEqual(
            all_movies[0].get('uuid'), str(alice.uuid)
        )

        self.assertEqual(
            all_movies[1].get('title'), 'minions'
        )
        self.assertEqual(
            all_movies[1].get('genre'), 'comedy'
        )
        self.assertEqual(
            all_movies[1].get('uuid'), str(minions.uuid)
        )

    def test_get_2(self):
        """test GET movies filtered by genre"""
        Movie.get_or_create(
            title='alice in wonderland',
            genre='mystery'
        )
        minions = Movie.get_or_create(
            title='minions',
            genre='comedy'
        )
        res = self.test_client.get('http://localhost:5555/movie/?genre=comedy')
        self.assertEqual(res.status_code, 200)
        all_movies = res.json
        self.assertEqual(len(all_movies), 1)

        self.assertEqual(
            res.json[0].get('title'), 'minions'
        )
        self.assertEqual(
            res.json[0].get('genre'), 'comedy'
        )
        self.assertEqual(
            res.json[0].get('uuid'), str(minions.uuid)
        )

    def test_get_3(self):
        """test GET movies filtered by genre if none match the genre"""
        Movie.get_or_create(
            title='alice in wonderland',
            genre='mystery'
        )
        Movie.get_or_create(
            title='minions',
            genre='comedy'
        )
        res = self.test_client.get('http://localhost:5555/movie/?genre=action')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json), 0)

    def test_get_4(self):
        """test GET movies filtered by actor"""
        alice_in_wonderland = Movie.get_or_create(
            title='alice in wonderland',
            genre='mystery'
        )

        # this one has the actor we want
        minions = Movie.get_or_create(
            title='minions',
            genre='comedy'
        )
        bob = Actor.get_or_create(name='Bob dyllan')
        alice = Actor.get_or_create(name='Alice')

        MovieActor.get_or_create(
            movie_uuid=alice_in_wonderland.uuid,
            actor_uuid=alice.uuid
        )
        MovieActor.get_or_create(
            movie_uuid=minions.uuid,
            actor_uuid=bob.uuid
        )
        res = self.test_client.get('http://localhost:5555/movie/?actor=Bob%20dyllan')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json), 1)
        self.assertEqual(res.json[0].get('title'), 'minions')
        self.assertEqual(res.json[0].get('genre'), 'comedy')

    def test_get_5(self):
        """test GET movies filtered by actor AND genre"""
        alice_in_wonderland = Movie.get_or_create(
            title='alice in wonderland',
            genre='mystery'
        )

        # this one has the actor we want
        minions = Movie.get_or_create(
            title='minions',
            genre='comedy'
        )

        mission_impossible = Movie.get_or_create(
            title='Mission Impossible',
            genre='action'
        )

        bob = Actor.get_or_create(name='Bob')
        alice = Actor.get_or_create(name='Alice')

        MovieActor.get_or_create(
            movie_uuid=alice_in_wonderland.uuid,
            actor_uuid=alice.uuid
        )
        MovieActor.get_or_create(
            movie_uuid=minions.uuid,
            actor_uuid=bob.uuid
        )

        MovieActor.get_or_create(
            movie_uuid=mission_impossible.uuid,
            actor_uuid=bob.uuid
        )

        res = self.test_client.get('http://localhost:5555/movie/?actor=Bob&genre=action')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json), 1)
        self.assertEqual(res.json[0].get('title'), 'Mission Impossible')
        self.assertEqual(res.json[0].get('genre'), 'action')

    def test_post_1(self):
        """ create a movie with no actors"""
        payload = {
            'title': 'test_title',
            'genre': 'test_genre'
        }
        res = self.post_json('http://localhost:5555/movie/', payload)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json.get('genre'), 'test_genre')
        self.assertEqual(res.json.get('title'), 'test_title')
        movie_uuid = res.json.get('uuid')

        # fetch from db:
        m = Movie.get(Movie.uuid == movie_uuid)
        self.assertEqual(m.title, 'test_title')
        self.assertEqual(m.genre, 'test_genre')

    def test_post_2(self):
        """ create a movie with actors"""
        payload = {
            'title': 'pirates of the caribbean',
            'genre': 'action',
            'actors': [
                'Johnny Depp',
                'Orlando Bloom'
            ]
        }
        res = self.post_json('http://localhost:5555/movie/', payload)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json.get('genre'), 'action')
        self.assertEqual(res.json.get('title'), 'pirates of the caribbean')
        movie_uuid = res.json.get('uuid')

        # fetch from db:
        m = Movie.get(Movie.uuid == movie_uuid)
        self.assertEqual(m.title, 'pirates of the caribbean')
        self.assertEqual(m.genre, 'action')

        # implicitly the actors should be created:
        actors = Actor.select()
        self.assertEqual(len(actors), 2)

        johnny = Actor.get(name='Johnny Depp')
        orlando = Actor.get(name='Orlando Bloom')

        # there should also be two records for MovieActor:

        all_movie_actors = MovieActor.select()
        self.assertEqual(len(all_movie_actors), 2)

        MovieActor.get(
            (MovieActor.movie == m)
            & (MovieActor.actor == johnny)
        )
        MovieActor.get(
            (MovieActor.movie == m)
            & (MovieActor.actor == orlando)
        )

    def test_post_3(self):
        """ POST with missing title"""
        payload = {
            'genre': 'test_genre'
        }
        res = self.post_json('http://localhost:5555/movie/', payload)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            len(Movie.select()),
            0
        )

    def test_post_4(self):
        """ POST with missing genre"""
        payload = {
            'title': 'gone with the wind'
        }
        res = self.post_json('http://localhost:5555/movie/', payload)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            len(Movie.select()),
            0
        )
