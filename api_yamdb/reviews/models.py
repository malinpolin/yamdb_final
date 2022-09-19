from accounts.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import year_validator


class Category(models.Model):
    """
    The model creates instances of category.
    """

    name = models.CharField("Category name", help_text="Genre", max_length=256)
    slug = models.SlugField(
        "Short category name",
        help_text="Genre slug",
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Genre(models.Model):
    """
    The model creates instances of genre.
    """

    name = models.CharField(
        "Genre name",
        help_text="Genre",
        max_length=256,
    )
    slug = models.SlugField(
        "Genre slug",
        help_text="Enter a short genre name",
        unique=True,
        max_length=50,
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Genre"
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name


class Title(models.Model):
    """
    The model creates instances of title.
    """

    name = models.CharField(
        "Title name", help_text="Enter the title name", max_length=128
    )
    year = models.IntegerField("Release year", validators=[year_validator])
    description = models.TextField(
        "Title description",
        help_text="Enter a description of the title",
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name="Genre",
        related_name="titles"
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Category",
        on_delete=models.SET_NULL,
        null=True,
        related_name="titles",
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Title"
        verbose_name_plural = "Titles"

    def __str__(self):
        return self.name


class Review(models.Model):
    """
    The model creates instances of review.
    """

    title = models.ForeignKey(
        Title,
        verbose_name="Title",
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    text = models.TextField(
        "Review",
    )
    author = models.ForeignKey(
        User,
        verbose_name="Author",
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    score = models.PositiveSmallIntegerField(
        "Raiting",
        validators=[
            MinValueValidator(1, "Valid value from 1 to 10"),
            MaxValueValidator(10, "Valid value from 1 to 10"),
        ],
    )
    pub_date = models.DateTimeField(
        "Publication Date", auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ["pub_date"]
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        constraints = [
            models.UniqueConstraint(fields=["title", "author"],
                                    name="unique_review")
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """
    The model creates instances of comments.
    """

    review = models.ForeignKey(
        Review,
        verbose_name="Review",
        on_delete=models.CASCADE,
        related_name="comments"
    )
    text = models.TextField("Text")
    author = models.ForeignKey(
        User,
        verbose_name="Author",
        on_delete=models.CASCADE,
        related_name="comments"
    )
    pub_date = models.DateTimeField(
        "Publication date", auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ["pub_date"]
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return self.text
