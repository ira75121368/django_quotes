from django.contrib import admin
from .models import Quotes, Categories, Source


@admin.register(Quotes)
class QuotesAdmin(admin.ModelAdmin):
    list_display = ['id', 'text_quotes', 'time_created', 'weight', 'likes', 'dislikes', 'views', 'source']
    list_display_links = ['id', 'text_quotes']
    list_per_page = 5


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_per_page = 10


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_per_page = 10
