#write a simple test to check if the movie model is working correctly
from django.test import TestCase
from .models import Movie



class MovieModelTest(TestCase):
    def setUp(self):
        Movie.objects.create(
            title="The Shawshank Redemption",
            overview="Two imprisoned",
            release_date="1994-09-23",  # Add the release_date field
            genre="Drama",
            director="Frank Darabont",
            poster_url="https://image.tmdb.org/t/p/w500/9O7gLzmreU0nGkIB6K3BsJbzvNv.jpg",
            tmdb_id=278
        )

    def test_movie_title(self):
        movie = Movie.objects.get(title="The Shawshank Redemption")
        self.assertEqual(movie.title, "The Shawshank Redemption")
        self.assertEqual(movie.overview, "Two imprisoned")
        self.assertEqual(str(movie), movie.title)

