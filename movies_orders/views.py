from rest_framework.views import APIView, Request, Response, status
from movies.models import Movie
from .serializers import MovieOrderSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class MovieOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, req: Request, movie_id: int) -> Response:
        serializer = MovieOrderSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)

        movie = get_object_or_404(Movie, id=movie_id)

        serializer.save(movie=movie, user=req.user)

        movie_order = serializer.data
        movie_order["title"] = movie.title
        movie_order["purchased_by"] = req.user.email

        return Response(movie_order, status.HTTP_201_CREATED)
