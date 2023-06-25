from celery import shared_task

from django.utils import timezone

from safedelete.models import HARD_DELETE

from main.models import File, ShareLink


@shared_task(ignore_result=True)
def db_clean_up():
    for file in File.deleted_objects.get_queryset():
        file.storaged_file.delete()
        File.delete(file, force_policy=HARD_DELETE)


@shared_task(ignore_result=True)
def delete_expired_share_links():
    now = timezone.now()
    ShareLink.all_objects.filter(expire_at__lte=now).delete()
