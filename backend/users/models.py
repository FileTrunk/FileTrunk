from django.contrib.auth.models import AbstractUser
from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel


class User(AbstractUser, SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    email = models.EmailField(("email address"), unique=True)
    picture = models.CharField(max_length=300, default=None, null=True)
    groups = None

    def __str__(self):
        return f"{self.email}"


class Stats(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    number_of_files = models.IntegerField(default=0)
    used_storage = models.FloatField(default=0)
    files_ext_distribution = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.user} - {self.used_storage} MB"
