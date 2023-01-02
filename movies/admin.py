from django.contrib import admin
from .models import Genre, NowplayingMovie, UpcomingMovie
# Register your models here.

admin.site.register(Genre)
admin.site.register(NowplayingMovie)
admin.site.register(UpcomingMovie)