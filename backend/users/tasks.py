from collections import defaultdict

from django.db import transaction
from celery import shared_task

from users.models import Stats
from main.models import File


@shared_task(ignore_result=True)
@transaction.atomic
def profile_stats_deletion(user_id, deleted_id):
    stats = Stats.objects.get(user_id=user_id)
    deleted = File.all_objects.get(pk=deleted_id)
    if not deleted.is_folder:
        deleted.number_of_files = 1
        deleted.files_ext_distribution = {deleted.file_type: 1}
    stats.used_storage -= deleted.file_size
    stats.number_of_files -= deleted.number_of_files
    files_ext_distribution = defaultdict(int, stats.files_ext_distribution)
    for ext, n_of_files in deleted.files_ext_distribution.items():
        files_ext_distribution[ext] -= n_of_files
    stats.files_ext_distribution = dict(
        [
            (ext, n_of_files)
            for ext, n_of_files in files_ext_distribution.items()
            if n_of_files > 0
        ]
    )
    stats.save()
    parent = deleted.parent
    while parent:
        parent.file_size -= deleted.file_size
        parent.number_of_files -= deleted.number_of_files
        files_ext_distribution = defaultdict(
            int, parent.files_ext_distribution
        )
        for ext, n_of_files in deleted.files_ext_distribution.items():
            files_ext_distribution[ext] -= n_of_files
        parent.files_ext_distribution = dict(
            [
                (ext, n_of_files)
                for ext, n_of_files in files_ext_distribution.items()
                if n_of_files > 0
            ]
        )
        parent.save()
        parent = parent.parent


@shared_task(ignore_result=True)
@transaction.atomic
def profile_stats_create(user_id, file_id):
    stats, created = Stats.objects.get_or_create(user_id=user_id)
    file = File.objects.get(pk=file_id)
    stats.used_storage += file.file_size
    stats.number_of_files += 1
    files_ext_distribution = defaultdict(int, stats.files_ext_distribution)
    files_ext_distribution[file.file_type] += 1
    stats.files_ext_distribution = files_ext_distribution
    stats.save()
    parent = file.parent
    while parent:
        parent.file_size += file.file_size
        parent.number_of_files += 1
        files_ext_distribution = defaultdict(
            int, parent.files_ext_distribution
        )
        files_ext_distribution[file.file_type] += 1
        parent.files_ext_distribution = files_ext_distribution
        parent.save()
        parent = parent.parent
