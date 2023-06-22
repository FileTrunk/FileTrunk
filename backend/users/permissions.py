import os

import jwt
from rest_framework import permissions


class IsAuthenticated(permissions.BasePermission):
    message = "You are not authenticated! Please, go to login page!"

    def has_permission(self, request, view):
        if request.user_id and request.META.get("HTTP_AUTHORIZATION"):
            return True
        return False


class DoesHaveJWTInLink(permissions.BasePermission):
    message = "No jwt in link!"

    def has_permission(self, request, view):
        if request.GET.get("token"):
            try:
                jwt.decode(
                    request.GET.get("token"),
                    os.environ.get("CLIENT_SECRET"),
                    algorithms="HS256",
                )
            except (jwt.exceptions.DecodeError):
                return False
            return True
        return False
