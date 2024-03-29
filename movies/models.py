from django.db import models
from users.models import User


class RatingChoices(models.TextChoices):
    G = 'G'
    PG = 'PG'
    PG_13 = 'PG-13'
    R = 'R'
    NC_17 = 'NC-17'


class Movie(models.Model):
    title = models.CharField(max_length=127)
    duration = models.CharField(max_length=10, blank=True, default='')
    rating = models.CharField(
        max_length=20,
        choices=RatingChoices.choices,
        default=RatingChoices.G
        )
    synopsis = models.TextField(blank=True, default='')
    user = models.ForeignKey(
        "users.user",
        on_delete=models.CASCADE,
        related_name="movies",
        null=True
        )
    movie_order = models.ManyToManyField(
        User,
        through="movies_orders.movieorder",
        related_name="movie_order"
        )
