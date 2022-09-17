from django.conf import settings
from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class TitleAdmin(admin.ModelAdmin):
    """
    The class configures the admin panel interface
    for the title model.
    """

    list_display = ("pk", "name", "year", "category")
    search_fields = ("name",)
    list_filter = ("year",)
    list_editable = ("category",)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


class CategoryAdmin(admin.ModelAdmin):
    """
    The class configures the admin panel interface
    for the category model.
    """

    list_display = ("pk", "name", "slug")
    search_fields = ("name",)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


class GenreAdmin(admin.ModelAdmin):
    """
    The class configures the admin panel interface
    for the genre model.
    """

    list_display = ("pk", "name", "slug")
    search_fields = ("name",)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


class ReviewAdmin(admin.ModelAdmin):
    """
    The class configures the admin panel interface
    for the review model.
    """

    list_display = ("title", "text", "author", "score", "pub_date")
    list_filter = ("author", "score", "pub_date")
    search_fields = ("text",)


class CommentAdmin(admin.ModelAdmin):
    """
    The class configures the admin panel interface
    for the comment model.
    """

    list_display = ("review", "text", "author", "pub_date")
    list_filter = ("author", "pub_date")
    search_fields = ("text",)


admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
