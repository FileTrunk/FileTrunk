from main.models import File, ShareLink
from rest_framework import serializers


class FileSerializer(serializers.ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(
        queryset=File.objects.all(),
        source="parent",
        allow_null=True,
        required=False,
    )

    class Meta:
        model = File
        fields = [
            "id",
            "filename",
            "file_type",
            "parent_id",
            "is_folder",
            "file_size",
            "updated_at",
        ]
        read_only_fields = ["parent", "user"]


class LinkDataSerializer(serializers.ModelSerializer):
    time = serializers.IntegerField()

    class Meta:
        model = ShareLink
        fields = ["file_id", "time"]
