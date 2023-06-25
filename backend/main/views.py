from datetime import datetime, timedelta

import jwt
import uuid

from django.utils import timezone
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.response import Response

from main.models import File, ShareLink
from main.forms import UploadFileForm
from main.serializers import FileSerializer, LinkDataSerializer
from users.permissions import DoesHaveJWTInLink, IsAuthenticated
from users.tasks import profile_stats_create, profile_stats_deletion


class FileSystemViewSet(viewsets.ViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        files = File.objects.filter(user_id=request.user_id, parent=None)
        serializer = FileSerializer(files, many=True)
        return Response({"message": "Success", "data": serializer.data})

    def create(self, request):
        data = FileSerializer(data=request.data)
        if not data.is_valid():
            return Response({"message": "Your data is problematic!"})
        validated_data = data.validated_data
        if File.objects.filter(
            user_id=request.user_id, **validated_data
        ).exists():
            return Response(
                {
                    "message": "Folder with such name already exists in current directory"
                }
            )
        file = File(user_id=request.user_id, **validated_data)
        file.save()
        return Response({"message": "Success"})

    def destroy(self, request, pk=None):
        parent_file = File.objects.get(pk=pk, user_id=request.user_id)
        parent_file.delete()
        profile_stats_deletion.apply_async((request.user_id, pk))
        return Response({"message": "Success"})

    def retrieve(self, request, pk=None):
        files = File.objects.filter(user_id=request.user_id, parent_id=pk)
        serializer = FileSerializer(files, many=True)
        return Response({"message": "Success", "data": serializer.data})


class FileUploadViewSet(viewsets.ViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        form.full_clean()
        if not form.is_valid():
            return Response({"message": "Your data is problematic!"})
        validated_data = form.cleaned_data
        file = File(is_folder=False, user_id=request.user_id, **validated_data)
        file.save()
        profile_stats_create.apply_async((request.user_id, file.id))
        return Response({"message": "Success"})

    def retrieve(self, request, pk=None):
        payload = {
            "exp": datetime.utcnow() + timedelta(minutes=1),
            "file_id": pk,
            "type": "download",
            "user_id": request.user_id,
        }
        token = jwt.encode(payload, settings.CLIENT_SECRET, algorithm="HS256")
        return Response({"message": "Success", "token": token})


class DownloadInitializationViewSet(viewsets.ViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [DoesHaveJWTInLink]
    parser_classes = [MultiPartParser, FormParser]

    def list(self, request):
        decoded_jwt = jwt.decode(
            request.GET.get("token"),
            settings.CLIENT_SECRET,
            algorithms="HS256",
        )
        file_obj = File.objects.get(pk=decoded_jwt["file_id"])
        storage = FileSystemStorage()
        file = storage.open(str(file_obj.storaged_file), mode="br")
        response = HttpResponse(
            file,
            content_type="multipart/form-data",
            headers={
                "Content-Disposition": f"attachment; filename={file_obj.filename}.{file_obj.file_type}"
            },
        )
        return response


class FileSharingViewSet(viewsets.ViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = []

    def retrieve(self, request, pk):
        file_id = get_object_or_404(ShareLink, share_token=pk).file.id
        file_obj = File.objects.get(pk=file_id)
        storage = FileSystemStorage()
        file = storage.open(str(file_obj.storaged_file), mode="br")
        response = HttpResponse(
            file,
            content_type="multipart/form-data",
            headers={
                "Content-Disposition": f"attachment; filename={file_obj.filename}.{file_obj.file_type}"
            },
        )
        return response

    def create(self, request):
        file_id, time = request.data['file_id'], request.data['time']
        file_share_link = uuid.uuid4().hex
        share_link_token = ShareLink(
            share_token=file_share_link,
            file_id=int(file_id),
            expire_at=timezone.now() + timedelta(minutes=int(time)),
        )
        share_link_token.save()
        return Response(
            {"message": "Success", "share_link_token": file_share_link}
        )

    def destroy(self, request, pk=None):
        ShareLink.objects.filter(file_id=pk).delete()
        return Response({"message": "Success"})
