from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Movie


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserProfileForm(forms.ModelForm):
    preferred_genre = forms.ChoiceField(
        choices=[(genre, genre) for genre in Movie.objects.values_list('genre', flat=True).distinct()], required=False)

    class Meta:
        model = UserProfile
        fields = ["favorite_movies", "preferred_genre"]
