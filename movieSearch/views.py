import logging

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from movieSearch.models import Movie, Actor


def search(request):
    query = request.GET.get('q')
    if query:
        actors = Actor.objects.filter(name__icontains=query)
        movies = Movie.objects.filter(title__icontains=query)
        context = {
            'actors': actors,
            'movies': movies
        }
        return render(request, 'results.html', context)
    else:

        return render(request, 'results.html')


class ActorDetailView(DetailView):
    model = Actor
    template_name = 'actor_details.html'


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movie_details.html'


def home(request):
    return render(request, 'index.html')
