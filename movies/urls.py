from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('nowplaying/', views.nowplaying, name='nowplaying'),
    path('upcoming/', views.upcoming, name='upcoming'),
    path('palette/', views.palette, name='palette'),
    path('palette/loading', views.loading, name='loading'),
    path('persona/', views.persona, name='persona'),
]
