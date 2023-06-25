import time
from unittest.mock import MagicMock, patch

import pytest
from main.models import File
from users.models import User, Stats
from users.tasks import profile_stats_create, profile_stats_deletion


# @pytest.mark.django_db
# def test_user_with_jwt_gets_profile_data_should_succeed_with_200(
#     client, user, headers
# ):
#     response = client.get('/api/v1/users/me/', **headers)
#     assert response.status_code == 200
#     assert response.data["message"] == "Success"


# @pytest.mark.django_db
# @patch(
#     'users.views.id_token.verify_oauth2_token',
#     MagicMock(
#         return_value={
#             "email": 'testuser@gmail.com',
#             "picture": 'http://example.com/picture_test',
#             "given_name": 'test_user_firstname',
#             "family_name": 'test_user_lastname',
#         }
#     ),
# )
# def test_user_with_valid_google_token_authenticates_should_succeed_with_200(
#     client, invalid_token
# ):
#     response = client.post(
#         '/api/v1/users/google-login/',
#         data={'googleTokenId': invalid_token},
#     )
#     assert response.status_code == 200
#     assert response.data["message"] == "Success"
#     assert len(User.objects.all()) == 1


# @pytest.mark.django_db
# @patch(
#     'users.views.id_token.verify_oauth2_token',
#     MagicMock(side_effect=ValueError),
# )
# def test_user_without_google_token_id_authenticates_should_fail_with_400(
#     client,
# ):
#     response = client.post('/api/v1/users/google-login/')
#     assert response.exception == "Authorization has been denied, bad data"
#     assert response.status_code == 400


# @pytest.mark.django_db
# def test_user_without_jwt_gets_profile_should_fail_with_403(
#     client, headers_with_no_token
# ):
#     response = client.post('/api/v1/users/me/', **headers_with_no_token)
#     assert response.status_code == 403


# @pytest.mark.django_db
# def test_user_with_non_valid_jwt_gets_profile_should_fail_with_403(
#     client, headers_with_non_valid_token
# ):
#     response = client.post('/api/v1/users/me/', **headers_with_non_valid_token)
#     assert response.status_code == 403


# @pytest.mark.django_db
# def test_user_with_expired_jwt_gets_profile_should_fail_with_403(
#     client, headers_with_exp_jwt
# ):
#     time.sleep(1.5)
#     response = client.post('/api/v1/users/me/')
#     assert response.status_code == 403


# @pytest.mark.django_db
# def test_bg_job_stats_update_on_addition_should_succeed(
#     user, folder, file, celery_config
# ):
#     profile_stats_create.apply((user.id, file.id))
#     stats = Stats.objects.get(user_id=user.id)
#     folder = File.objects.get(pk=file.parent.id)
#     assert stats.files_ext_distribution == {'type': 1}
#     assert stats.used_storage == 20.2
#     assert stats.number_of_files == 1
#     assert folder.number_of_files == 1
#     assert folder.file_size == 20.2
#     assert folder.files_ext_distribution == {'type': 1}


# @pytest.mark.django_db
# def test_bg_job_stats_update_on_deletion_should_succeed(
#     user, file, stats, celery_config
# ):
#     file.delete()
#     profile_stats_deletion.apply((user.id, file.id))
#     stats = Stats.objects.get(user_id=user.id)
#     folder = File.objects.get(pk=file.parent.id)
#     assert stats.files_ext_distribution == {}
#     assert stats.used_storage == 0.0
#     assert stats.number_of_files == 0
#     assert folder.number_of_files == -1
#     assert folder.files_ext_distribution == {}
