from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Movie


class SignUpForm(UserCreationForm):
    """
    A form for creating new users. Inherits from Django's UserCreationForm.
    """
    class Meta:
        """
        Meta class to specify the model and fields to be used in the form.
        """
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserProfileForm(forms.ModelForm):
    """
    A form for updating user profiles. Inherits from Django's ModelForm.
    """
    preferred_genre = forms.ChoiceField(
        choices=[(genre, genre) for genre in Movie.objects.values_list('genre', flat=True).distinct()], required=False,
        help_text="Select your preferred genre from the available options."
    )

    class Meta:
        """
        Meta class to specify the model and fields to be used in the form.
        """
        model = UserProfile
        fields = ["favorite_movies", "preferred_genre"]
