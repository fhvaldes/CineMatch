from django.core.management.base import BaseCommand
import requests
from movies.models import Movie
from config import api_key

class Command(BaseCommand):
    """
    Django management command to fetch popular movies from TMDB and save them to the database.
    """
    help = "Fetch movies from TMDB and save them to the database"

    def handle(self, *args, **kwargs):
        """
        Main method to handle the fetching and saving of movies.
        """
        base_url = "https://api.themoviedb.org/3"
        endpoint = "/movie/popular"
        params = {
            "api_key": api_key,
            "language": "es-ES",
            "page": 1,
        }

        # Fetch popular movies
        response = requests.get(base_url + endpoint, params=params).json()
        total_pages = response["total_pages"]

        # Iterate through all pages of results
        for page in range(1, total_pages + 1):
            params["page"] = page
            response = requests.get(base_url + endpoint, params=params).json()

            for movie_data in response["results"]:
                # Fetch additional movie details
                details_url = f"{base_url}/movie/{movie_data['id']}"
                details_params = {"api_key": api_key, "language": "es-ES"}
                details_response = requests.get(details_url, params=details_params).json()

                # Fetch the director (if available)
                credits_url = f"{base_url}/movie/{movie_data['id']}/credits"
                credits_response = requests.get(credits_url, params={"api_key": api_key}).json()
                director = next(
                    (crew["name"] for crew in credits_response["crew"] if crew["job"] == "Director"),
                    None,
                )

                # Create or update the movie in the database
                Movie.objects.update_or_create(
                    tmdb_id=movie_data["id"],
                    defaults={
                        "title": movie_data["title"],
                        "overview": movie_data["overview"],
                        "release_date": movie_data["release_date"],
                        "genre": ", ".join(
                            [genre["name"] for genre in details_response.get("genres", [])]
                        ),
                        "director": director,
                        "poster_url": f"https://image.tmdb.org/t/p/w500{movie_data['poster_path']}",
                    },
                )

            self.stdout.write(self.style.SUCCESS(f"Página {page} de {total_pages} procesada"))

        self.stdout.write(self.style.SUCCESS("Películas actualizadas correctamente"))