from django.apps import AppConfig


class MoviesConfig(AppConfig):
    """
    Configuration class for the 'movies' application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'

    def ready(self):
        """
        Method to import signals when the application is ready.
        """
        import movies.signals