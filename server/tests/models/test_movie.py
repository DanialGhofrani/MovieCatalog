from server.models.movie import Movie
from ..base import ModelTestCase


class TestMovie(ModelTestCase):

    def test_get_or_create_1(self):
        """test valid creation of movie with genre"""
        all_movies = Movie.select()
        self.assertEqual(0, len(all_movies))
        movie = Movie.get_or_create(
            title='batman',
            genre='action'
        )
        # check movie object returned:
        self.assertEqual('batman', movie.title)
        self.assertEqual('action', movie.genre)

        # fetch movie from database:
        # get implicitly asserts that there is exactly 1 movie:
        movie = Movie.get()
        self.assertEqual('batman', movie.title)
        self.assertEqual('action', movie.genre)

        # the title is treated as a primary key:
        movie = Movie.get_or_create(
            title='batman',
            genre='adventure'
        )
        self.assertEqual('batman', movie.title)
        self.assertEqual('action', movie.genre)

        movie = Movie.get()
        self.assertEqual('batman', movie.title)
        self.assertEqual('action', movie.genre)

        # creating another movie title will increase the number of movies:
        movie = Movie.get_or_create(
            title='minions',
            genre='comedy'
        )
        # check movie object returned:
        self.assertEqual('minions', movie.title)
        self.assertEqual('comedy', movie.genre)

        # 2 movies exist in database now:
        movies = Movie.select()
        self.assertEqual(len(movies), 2)
        # one of them is minions
        m = Movie.get(Movie.title == 'minions')
        self.assertEqual(m.title, 'minions')
        self.assertEqual(m.genre, 'comedy')

        # non existent genre is allowed
        movie = Movie.get_or_create(
            title='harry potter'
        )
        self.assertEqual(movie.title, 'harry potter')
        self.assertIsNone(movie.genre)

        movies = Movie.select()
        self.assertEqual(len(movies), 3)

    def test_get_or_create_2(self):
        """valid name should always be provided"""
        with self.assertRaises(ValueError):
            Movie.get_or_create(
                title=None,
                genre='action'
            )

        with self.assertRaises(ValueError):
            Movie.get_or_create(
                title=123,
                genre='action'
            )