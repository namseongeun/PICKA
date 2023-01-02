from django.db import models
from django.conf import settings


class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class NowplayingMovie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    overview = models.TextField()
    poster_path = models.CharField(max_length=200)
    backdrop_path = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre, related_name='nowplaying_movies')
    # like_users = models.ManyToManyField(
    #     settings.AUTH_USER_MODEL, related_name='like_nowplaying_movies'
    # )

    def __str__(self):
        return self.title


class UpcomingMovie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    overview = models.TextField()
    poster_path = models.CharField(max_length=200)
    backdrop_path = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre, related_name='upcoming_movies')
    #like_users = models.ManyToManyField(
    #    settings.AUTH_USER_MODEL, related_name='like_upcoming_movies'
    #)

    def __str__(self):
        return self.title


class PaletteMovie(models.Model):
    title = models.CharField(max_length=100)
    R = models.TextField()
    G = models.TextField()
    B = models.TextField()
    path = models.TextField()
