from rest_framework.views import APIView, Request, Response, status
from .serializers import UserSerializer
from .models import User


class UserView(APIView):
    def post(self, req: Request) -> Response:
        serializer = UserSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        find_username = User.objects.filter(
            username__exact=req.data.get("username")
        )
        find_email = User.objects.filter(
            email__iexact=req.data.get("email")
        )
        if find_username:
            if find_email:
                return Response(
                    {
                        "email": ["email already registered."], 
                        "username": ["username already taken."]
                    },
                    status.HTTP_400_BAD_REQUEST
                )
            else:
                return Response(
                    {"username": ["username already taken."]},
                    status.HTTP_400_BAD_REQUEST
                )
        elif find_email:
            return Response(
                    {"email": ["email already registered."]},
                    status.HTTP_400_BAD_REQUEST
                )
        
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
