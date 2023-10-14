from rest_framework.views import APIView, Request, Response, status
from .models import Movie
from .serializers import MovieSerializer
from .permissions import IsEmployeeOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404


class MovieView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployeeOrReadOnly]

    def get(self, req: Request) -> Response:
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, req: Request) -> Response:
        data = req.data
        data["user"] = req.user
        serializer = MovieSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        serializer.save(user=req.user)
        movie_return = serializer.data
        movie_return["added_by"] = req.user.email
        return Response(movie_return, status.HTTP_201_CREATED)


class MovieDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployeeOrReadOnly]

    def get(self, req: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, pk=movie_id)

        serializer = MovieSerializer(movie)
        print(movie.user)
        movie_return = serializer.data
        movie_return["added_by"] = movie.user.email

        return Response(movie_return, status.HTTP_200_OK)

    def delete(self, req: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, pk=movie_id)
        movie.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
