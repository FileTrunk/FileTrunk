import os
import uuid

from django.db import models
from django.utils.timezone import now
from safedelete.config import HARD_DELETE
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel
from users.models import User


def get_file_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join(f"users/{instance.user_id}", filename)


class File(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    filename = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self", default=None, null=True, blank=True, on_delete=models.CASCADE
    )
    file_type = models.CharField(max_length=15, default="")
    is_folder = models.BooleanField(null=False, default=False)
    file_size = models.FloatField(default=0)
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None, null=False
    )
    storaged_file = models.FileField(upload_to=get_file_path, null=True)
    number_of_files = models.IntegerField(default=0)
    files_ext_distribution = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.id} - {self.filename}.{self.file_type} - {self.user}"


class ShareLink(SafeDeleteModel):
    _safedelete_policy = HARD_DELETE

    share_token = models.CharField(max_length=120, null=False, unique=True)
    file = models.ForeignKey(File, null=False, on_delete=models.CASCADE)
    authentication = models.BooleanField(default=False)
    number_of_clicks = models.IntegerField(default=0)
    expire_at = models.DateTimeField(null=False, default=now)

    def __str__(self):
        return (
            f"Link to | {self.file} | by | {self.file.user} | {self.expire_at}"
        )
