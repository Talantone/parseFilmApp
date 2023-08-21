from django.shortcuts import redirect
from django.urls import path

from movieSearch.views import home, search, ActorDetailView, MovieDetailView

urlpatterns = [
    path('', lambda req: redirect('/home')),
    path('home', home, name='home'),
    path('results', search, name="search"),
    path('actor-details/<int:pk>', ActorDetailView.as_view(), name='actor-details'),
    path('movie-details/<int:pk>', MovieDetailView.as_view(), name='movie-details')
]