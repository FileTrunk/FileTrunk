from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import User, Stats
from .permissions import IsAuthenticated
from .serializers import UserSerializer


class GoogleLogin(ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def create(self, request):
        try:
            token = request.data["googleTokenId"]
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), settings.CLIENT_ID
            )
        except (
            ValueError,
            MultiValueDictKeyError,
        ):
            return Response(
                exception="Authorization has been denied, bad data", status=400
            )
        user, created = User.objects.update_or_create(
            email=idinfo["email"],
            username=idinfo["email"],
            picture=idinfo.get("picture"),
            first_name=idinfo.get("given_name", idinfo.get('name', "")),
            last_name=idinfo.get("family_name", ""),
        )
        if created:
            user.save()
        server_side_jwt = jwt.encode(
            payload={
                "exp": datetime.utcnow() + timedelta(days=14),
                "user_id": user.pk,
            },
            key=settings.CLIENT_SECRET,
            algorithm="HS256",
        )
        return Response({"jwt": server_side_jwt, "message": "Success"})


class Profile(ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = User.objects.get(pk=request.user_id)
        serializer = UserSerializer(user)
        return Response({"message": "Success", "data": serializer.data})


class StatsViewSet(ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        stats, created = Stats.objects.get_or_create(user_id=request.user_id)
        stats = {
            'used_storage': stats.used_storage,
            'number_of_files': stats.number_of_files,
            'files_ext_distribution': stats.files_ext_distribution,
        }
        return Response({"message": "Success", "data": stats})
