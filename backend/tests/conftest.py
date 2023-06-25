from time import sleep
from django.utils import timezone
from datetime import datetime, timedelta
from collections import defaultdict

import pytest
import jwt
from django.test import Client
from django.conf import settings
from main.models import File, ShareLink
from users.models import User, Stats


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user():
    user = User.objects.create(
        email='testuser@gmail.com',
        picture='http://example.com/picture_test',
        first_name='test_user_firstname',
        last_name='test_user_lastname',
    )
    user.save()
    return user


@pytest.fixture
def user_jwt(user):
    enc_jwt = jwt.encode(
        payload={
            "exp": datetime.utcnow() + timedelta(days=14),
            "user_id": user.id,
        },
        key=settings.CLIENT_SECRET,
    )
    return enc_jwt


@pytest.fixture
def folder(user):
    folder = File.objects.create(filename='folder', is_folder=True, user=user)
    folder.save()
    return folder


@pytest.fixture
def file(user, folder):
    file = File.objects.create(
        filename='file',
        file_type='type',
        is_folder=False,
        user=user,
        parent=folder,
        file_size=20.2,
    )
    file.save()
    return file


@pytest.fixture
def file_download_jwt(file, user):
    payload = {
        "exp": datetime.utcnow() + timedelta(minutes=1),
        "file_id": file.id,
        "type": "download",
        "user_id": user.id,
    }
    token = jwt.encode(payload, settings.CLIENT_SECRET)
    return token


@pytest.fixture
def expired_user_jwt(user):
    enc_jwt = jwt.encode(
        payload={
            "exp": datetime.utcnow() + timedelta(seconds=1),
            "user_id": user.id,
        },
        key=settings.CLIENT_SECRET,
    )
    return enc_jwt


@pytest.fixture
def share_link(file):
    share_link = ShareLink(share_token="share_token", file=file)
    share_link.save()
    return share_link


@pytest.fixture
def expired_share_link(file):
    expired_share_link = ShareLink(share_token="share_token", file=file)
    expired_share_link.save()
    sleep(1)
    return expired_share_link


@pytest.fixture
def stats(user, file):
    stats, created = Stats.objects.get_or_create(user_id=user.id)
    stats.used_storage += file.file_size
    stats.number_of_files += 1
    files_ext_distribution = defaultdict(int, stats.files_ext_distribution)
    files_ext_distribution[file.file_type] += 1
    stats.files_ext_distribution = files_ext_distribution
    stats.save()
    return stats


@pytest.fixture(scope='session')
def celery_config():
    return {'broker_url': 'amqp://', 'result_backend': 'rpc://'}


@pytest.fixture
def headers(user_jwt):
    return {'HTTP_AUTHORIZATION': f'Bearer : {user_jwt}'}


@pytest.fixture
def headers_with_no_token():
    return {'HTTP_AUTHORIZATION': f'Bearer : '}


@pytest.fixture
def headers_with_non_valid_token():
    return {'HTTP_AUTHORIZATION': f'Bearer : Non valid token'}


@pytest.fixture
def headers_with_exp_jwt(expired_user_jwt):
    return {'HTTP_AUTHORIZATION': f'Bearer : {expired_user_jwt}'}


@pytest.fixture
def invalid_token():
    return 'Non valid jwt/token, which causes error'
