import json
from django.shortcuts import render
from django.shortcuts import redirect, render
from django.views.decorators.http import require_safe, require_http_methods
from .models import Genre, NowplayingMovie, UpcomingMovie, PaletteMovie

import os

# from django.core.paginator import Paginator
import requests
import cv2
import numpy as np

# TMBD API 받아오기 위한 경로와 파라미터들
TMDB_API_KEY =os.environ.get('TMDB_API_KEY')
KAKAO_API_KEY =os.environ.get('KAKAO_API_KEY')

BASE_URL = 'https://api.themoviedb.org/3'
params = {
    'api_key': TMDB_API_KEY,
    'region': 'KR',
    'language': 'ko',
}


# 메인 화면
@require_safe
def nowplaying(request):
    if request.user.is_authenticated:
        path = '/movie/now_playing'
        data = requests.get(BASE_URL + path, params=params).json()
        nowplaying_movies = data.get("results")
        # nowplaying_movies = sorted(nowplaying_movies, key=lambda movie: movie['popularity'], reverse=True)

        genres = Genre.objects.all()
        first_movie = nowplaying_movies[0]
        first_movie_genres = []
        first_movie_genre_ids = first_movie['genre_ids']
        for genre_id in first_movie_genre_ids:
            for genre in genres:
                if genre_id == genre.pk:
                    first_movie_genres.append(genre)

        last_movies = nowplaying_movies[1:10]
        for last_movie in last_movies:

            last_movie_id = last_movie['id']
            last_video_path = f'/movie/{last_movie_id}/videos'
            last_video_data = requests.get(
                BASE_URL + last_video_path, params=params
            ).json()
            if last_video_data['results'] != []:
                last_video_id = last_video_data['results'][0]['key']
            else:
                last_video_id = None
            last_movie['video_id'] = last_video_id

            last_movie['genres'] = []
            last_movie_genre_ids = last_movie['genre_ids']
            for genre_id in last_movie_genre_ids:
                for genre in genres:
                    if genre_id == genre.pk:
                        last_movie['genres'].append(genre)

        context = {
            'first_movie': first_movie,
            'first_movie_genres': first_movie_genres,
            'last_movies': last_movies,
            'KAKAO_API_KEY': KAKAO_API_KEY,
            'TMDB_API_KEY': TMDB_API_KEY,
        }
        return render(request, 'movies/nowplaying.html', context)
    else:
        return redirect('accounts:login')


# 개봉 예정작 탭
@require_safe
def upcoming(request):
    if request.user.is_authenticated:
        path = '/movie/upcoming'
        data = requests.get(BASE_URL + path, params=params).json()
        upcoming_movies = data.get("results")

        genres = Genre.objects.all()

        first_movie = upcoming_movies[0]
        first_movie_id = first_movie['id']
        first_video_path = f'/movie/{first_movie_id}/videos'
        first_video_data = requests.get(
            BASE_URL + first_video_path, params=params
        ).json()
        if first_video_data['results'] != []:
            first_video_id = first_video_data['results'][0]['key']
        else:
            first_video_id = None
        first_movie['video_id'] = first_video_id

        first_movie_genres = []
        first_movie_genre_ids = first_movie['genre_ids']
        for genre_id in first_movie_genre_ids:
            for genre in genres:
                if genre_id == genre.pk:
                    first_movie_genres.append(genre)

        last_movies = upcoming_movies[1:]
        for last_movie in last_movies:
            last_movie_id = last_movie['id']
            last_video_path = f'/movie/{last_movie_id}/videos'
            last_video_data = requests.get(
                BASE_URL + last_video_path, params=params
            ).json()
            if last_video_data['results'] != []:
                last_video_id = last_video_data['results'][0]['key']
            else:
                last_video_id = None
            last_movie['video_id'] = last_video_id

            last_movie['genres'] = []
            last_movie_genre_ids = last_movie['genre_ids']
            for genre_id in last_movie_genre_ids:
                for genre in genres:
                    if genre_id == genre.pk:
                        last_movie['genres'].append(genre)

        context = {
            'first_movie': first_movie,
            'first_movie_genres': first_movie_genres,
            'last_movies': last_movies,
        }
        return render(request, 'movies/upcoming.html', context)
    else:
        return redirect('accounts:login')


# 팔레트 로딩 탭
@require_http_methods(['GET', 'POST'])
def loading(request):
    if request.user.is_authenticated:

        return render(request, 'movies/loading.html')

    else:
        return redirect('account:intro')


# 팔레트 탭
@require_http_methods(['GET', 'POST'])
def palette(request):
    if request.user.is_authenticated:
        movies = PaletteMovie.objects.all()
        context = {
            'movies': movies,
        }
        return render(request, 'movies/palette.html', context)
    else:
        return redirect('accounts:intro')


# 페르소나
@require_http_methods(['GET', 'POST'])
def persona(request):
    if request.method == 'GET':
        path = '/movie/now_playing'
        data = requests.get(BASE_URL + path, params=params).json()
        nowplaying_movies = data.get("results")

        context = {
            'nowplaying_movies': nowplaying_movies,
        }
        return render(request, 'movies/persona.html', context)


# ------------------------------------------------------------------------------
# API 가져오기
# 장르데이터 가져오기
def get_genre():
    path = '/genre/movie/list'
    data = requests.get(BASE_URL + path, params=params).json()
    genres = data.get("genres")

    for genre in genres:
        genre_data = Genre(
            id=genre['id'],
            name=genre['name'],
        )
        genre_data.save()


# 현재상영작
def get_nowplaying():
    path = '/movie/now_playing'
    data1 = requests.get(BASE_URL + path, params=params).json()
    now_playing_movies = data1.get("results")

    for now_playing_movie in now_playing_movies:
        if (
            now_playing_movie['release_date']
            and now_playing_movie['backdrop_path']
            and now_playing_movie['poster_path']
        ):
            now_playing_movie_data = NowplayingMovie(
                id=now_playing_movie['id'],
                title=now_playing_movie['title'],
                release_date=now_playing_movie['release_date'],
                popularity=now_playing_movie['popularity'],
                vote_count=now_playing_movie['vote_count'],
                vote_average=now_playing_movie['vote_average'],
                overview=now_playing_movie['overview'],
                poster_path=now_playing_movie['poster_path'],
                backdrop_path=now_playing_movie['backdrop_path'],
            )
            now_playing_movie_data.save()

            genres = now_playing_movie['genre_ids']
            now_playing_movie_data.genres.add(*genres)
        else:
            continue


# 개봉예정작
def get_upcoming():
    path = '/movie/upcoming'
    data = requests.get(BASE_URL + path, params=params).json()
    upcoming_movies = data.get("results")

    for upcoming_movie in upcoming_movies:
        if (
            upcoming_movie['release_date']
            and upcoming_movie['backdrop_path']
            and upcoming_movie['poster_path']
        ):
            upcoming_movie_data = UpcomingMovie(
                id=upcoming_movie['id'],
                title=upcoming_movie['title'],
                release_date=upcoming_movie['release_date'],
                popularity=upcoming_movie['popularity'],
                vote_count=upcoming_movie['vote_count'],
                vote_average=upcoming_movie['vote_average'],
                overview=upcoming_movie['overview'],
                poster_path=upcoming_movie['poster_path'],
                backdrop_path=upcoming_movie['backdrop_path'],
            )
            upcoming_movie_data.save()

            genres = upcoming_movie['genre_ids']
            upcoming_movie_data.genres.add(*genres)
        else:
            continue


# 팔레트
def get_palette():
    for i in range(1, 20):
            API_KEY = params['api_key']
            request_url = (
                f'{BASE_URL}/movie/top_rated?api_key={API_KEY}&language=ko-KR&page={i}'
            )
            original_movies = requests.get(request_url).json()

            for movie in original_movies['results']:
                poster = movie['poster_path']
                src_img = cv2.imdecode(
                    np.asarray(
                        bytearray(
                            requests.get(
                                f'https://www.themoviedb.org/t/p/original/{poster}'
                            ).content
                        ),
                        dtype=np.uint8,
                    ),
                    cv2.IMREAD_COLOR,
                )
                average_color_row = np.average(src_img, axis=0)
                average_color = np.average(average_color_row, axis=0)
                palette_movie_data = PaletteMovie(
                    title = movie['title'],
                    R = average_color[2],
                    G = average_color[1],
                    B = average_color[0],
                    path = movie['poster_path']
                )
                palette_movie_data.save()

# get_palette()                
# get_genre()
# get_nowplaying()
# get_upcoming()
