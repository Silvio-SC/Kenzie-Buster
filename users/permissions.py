from rest_framework import permissions
from .models import User
from rest_framework.views import Request, View


class IsUserOwner(permissions.BasePermission):
    def has_object_permission(self, req: Request, view: View, obj: User):
        return obj == req.user
