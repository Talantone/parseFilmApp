from django.core.management import BaseCommand
from movieSearch.models import Movie, Actor
from bs4 import BeautifulSoup
from parseFilmApp.settings import CSFD_URL
import requests

base_url = CSFD_URL
top_url = "https://www.csfd.cz/zebricky/filmy/nejlepsi/"

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0",
}


class Command(BaseCommand):
    help = "Parses movie top-300 from CSFD website and adds it to database"

    def handle(self, *args, **options):
        req = requests.get(top_url, headers=headers)
        srcs = [req.text]
        for i in range(100, 301, 100):
            modified_url = top_url + "?from=" + str(i)
            req = requests.get(modified_url, headers=headers)
            srcs.append(req.text)

        with open("main.html", "w") as file:
            file.write('<html>')
            for src in srcs:
                src = src.replace('<html>', '')
                src = src.replace('</html>', '')
                file.write(src)
            file.write('</html>')

        with open("main.html") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        all_films_hrefs = soup.find_all(class_="film-title-name")
        i = 0

        for film in all_films_hrefs:
            if not Movie.objects.filter(title=film.get("title")).exists():
                movie = Movie(title=film.get("title"))
                movie.save()
                req = requests.get(base_url + film.get("href"), headers=headers)
                detail = req.text
                film_detail_soup = BeautifulSoup(detail, "lxml")
                film_actors = film_detail_soup.find("h4", string="Hrají:").findNextSiblings("a")
                if film_detail_soup.find("h4", string="Hrají:").findNextSibling("span") is not None:
                    not_so_necessary_actors = film_detail_soup.find("h4", string="Hrají:").findNextSibling("span").findAll("a")
                    film_actors += not_so_necessary_actors
                for actor in film_actors:
                    person = Actor(name=actor.text)
                    if not Actor.objects.filter(name=person.name).exists():
                        person.save()
                        movie.actors.add(person)
                        movie.save()
                    else:
                        movie.actors.add(Actor.objects.get(name=person.name))
                        movie.save()
            else:
                raise Exception("movies from the csfd website are already in database")
            i += 1
            if i == 300:
                break
