from .forms import SignUpForm, UserProfileForm
from .models import UserProfile, Movie
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from rest_framework import generics
from .models import Movie
from .serializers import MovieSerializer


def signup(request):
    """
    Handle user signup.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with the rendered signup page or a redirect to the home page.
    """
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


def profile(request):
    """
    Handle user profile view and update.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with the rendered profile page.
    """
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, "profile.html", {"form": form})


def recommend_movies(user):
    """
    Recommend movies to the user based on their preferred genre.

    Args:
        user (User): The user object.

    Returns:
        QuerySet: A queryset of recommended movies.
    """
    recommended_movies = []
    try:
        preferred_genre = user.userprofile.preferred_genre
        if preferred_genre:
            recommended_movies = Movie.objects.filter(genre=preferred_genre).order_by("?")[:10]
        else:
            recommended_movies = Movie.objects.order_by("?")[:10]  # Random movies if no preferred genre
    except UserProfile.DoesNotExist:
        recommended_movies = Movie.objects.order_by("?")[:10]  # Random movies if no user profile
    return recommended_movies


def home(request):
    """
    Render the home page with recommended movies.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with the rendered home page.
    """
    if request.user.is_authenticated:
        recommended_movies = recommend_movies(request.user)
    else:
        recommended_movies = Movie.objects.order_by("?")[:10]  # Películas aleatorias
    return render(request, "home.html", {"movies": recommended_movies})


def search(request):
    """
    Handle movie search.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with the rendered search results page.
    """
    query = request.GET.get("q")
    if query:
        movies = Movie.objects.filter(title__icontains(query))
    else:
        movies = Movie.objects.none()  # Return an empty queryset if query is None or empty
    return render(request, "search.html", {"movies": movies})


def login_view(request):
    """
    Handle user login.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with the rendered login page or a redirect to the home page.
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenido, {username}!")
                return redirect("home")
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    """
    Handle user logout.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object with a redirect to the home page.
    """
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect("home")


def movie_detail(request, movie_id):
    """
    Render the movie detail page.

    Args:
        request (HttpRequest): The HTTP request object.
        movie_id (int): The ID of the movie.

    Returns:
        HttpResponse: The HTTP response object with the rendered movie detail page.
    """
    movie = get_object_or_404(Movie, id=movie_id)  # Obtiene la película o devuelve un error 404
    return render(request, "movie_detail.html", {"movie": movie})


class MovieListAPIView(generics.ListAPIView):
    """
    API view to list all movies.

    Attributes:
        queryset (QuerySet): The queryset of all movies.
        serializer_class (Serializer): The serializer class for the movies.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer