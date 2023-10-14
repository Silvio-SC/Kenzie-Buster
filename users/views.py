from rest_framework.views import APIView, Request, Response, status
from .serializers import UserSerializer
from .models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from .permissions import IsUserOwner


class UserView(APIView):
    def post(self, req: Request) -> Response:
        serializer = UserSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        find_username = User.objects.filter(
            username__exact=req.data.get('username')
        )
        find_email = User.objects.filter(
            email__iexact=req.data.get('email')
        )
        if find_username:
            if find_email:
                return Response(
                    {
                        'email': ['email already registered.'], 
                        'username': ['username already taken.']
                    },
                    status.HTTP_400_BAD_REQUEST
                )
            else:
                return Response(
                    {'username': ['username already taken.']},
                    status.HTTP_400_BAD_REQUEST
                )
        elif find_email:
            return Response(
                    {'email': ['email already registered.']},
                    status.HTTP_400_BAD_REQUEST
                )

        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsUserOwner]

    def get(self, req: Request, user_id: int):
        user = get_object_or_404(User, pk=user_id)

        if not req.user.is_employee:
            self.check_object_permissions(req, user)

        serializer = UserSerializer(user)

        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, req: Request, user_id):
        user = get_object_or_404(User, pk=user_id)

        if not req.user.is_employee:
            self.check_object_permissions(req, user)

        serializer = UserSerializer(user, req.data, partial=True)
        serializer.is_valid()

        if req.data["password"]:
            user.set_password(req.data["password"])

        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)

# class UserLoginView(APIView):
#     def post(self, req: Request) -> Response:
#         serializer = UserLoginSerializer(data=req.data)
#         serializer.is_valid(raise_exception=True)

#         user = authenticate(
#             username=serializer.validated_data['username'],
#             password=serializer.validated_data['password'],
#         )

#         if not user:
#             return Response(
#                 {"detail": "No active account was found."},
#                 status.HTTP_403_FORBIDDEN
#             )

#         refresh = RefreshToken.for_user(user)

#         token = {
#             "refresh": str(refresh),
#             "access": str(refresh.access_token)
#         }

#         return Response(token)
