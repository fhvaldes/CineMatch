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
    if request.user.is_authenticated:
        recommended_movies = recommend_movies(request.user)
    else:
        recommended_movies = Movie.objects.order_by("?")[:10]  # Películas aleatorias
    return render(request, "home.html", {"movies": recommended_movies})


def search(request):
    query = request.GET.get("q")
    if query:
        movies = Movie.objects.filter(title__icontains=query)
    else:
        movies = Movie.objects.none()  # Return an empty queryset if query is None or empty
    return render(request, "search.html", {"movies": movies})


# Vista de login
def login_view(request):
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


# Vista de logout
def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect("home")


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)  # Obtiene la película o devuelve un error 404
    return render(request, "movie_detail.html", {"movie": movie})


class MovieListAPIView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
