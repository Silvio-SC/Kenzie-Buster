from django.db import models


class MovieOrder(models.Model):
    purchased_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    user = models.ForeignKey("users.user", on_delete=models.CASCADE)
    movie = models.ForeignKey("movies.movie", on_delete=models.CASCADE)
