from django import forms
from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    title = models.CharField(max_length=255)
    overview = models.TextField()
    release_date = models.DateField()
    genre = models.CharField(max_length=100)
    director = models.CharField(max_length=255, blank=True, null=True)
    poster_url = models.URLField()
    tmdb_id = models.IntegerField(unique=True)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_movies = models.ManyToManyField(Movie, blank=True)
    preferred_genre = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username
