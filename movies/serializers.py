from rest_framework import serializers
from .models import RatingChoices, Movie
from users.serializers import UserSerializer
from users.models import User


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(
        max_length=10,
        allow_blank=True,
        default=''
        )
    rating = serializers.ChoiceField(
        choices=RatingChoices.choices,
        default=RatingChoices.G
        )
    synopsis = serializers.CharField(allow_blank=True, default='')
    added_by = serializers.EmailField(read_only=True)

    def create(self, validated_data):
        movie = Movie.objects.create(
            **validated_data
            )
        return movie
