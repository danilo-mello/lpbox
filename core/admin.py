from django.contrib import admin
from .models import Lp

@admin.register(Lp)
class LpAdmin(admin.ModelAdmin):
    list_display = ('album_title', 'artist', 'year')
