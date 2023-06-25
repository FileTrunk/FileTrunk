import pytest
import json
import time
from time import sleep
from unittest.mock import MagicMock, patch


from users.models import Stats
from main.models import ShareLink, File
from main.tasks import (
    delete_expired_share_links,
    db_clean_up,
)
from users.tasks import profile_stats_create, profile_stats_deletion


@pytest.mark.django_db
def test_user_with_jwt_gets_list_of_files_should_succeed_with_200(
    client, headers, folder
):
    response = client.get('/api/v1/files/', **headers)
    assert response.status_code == 200
    assert response.json()['message'] == 'Success'
    assert response.json()['data'][0]['filename'] == 'folder'


@pytest.mark.django_db
def test_user_with_jwt_deletes_file_should_succeed_with_200(
    client,
    folder,
    headers,
    celery_config,
):
    response = client.delete(f'/api/v1/files/{folder.id}/', **headers)
    assert response.status_code == 200
    assert response.content == b'{"message":"Success"}'


# @pytest.mark.django_db
# def test_user_with_jwt_creates_folder_should_succeed_with_200(client, headers):
#     response = client.post(
#         '/api/v1/files/',
#         **headers,
#         data={
#             'filename': 'folder_with_non_existing_name',
#             'is_folder': True,
#             'parent_id': "",
#         },
#     )
#     assert response.status_code == 200
#     assert response.content == b'{"message":"Success"}'


# @pytest.mark.django_db
# def test_user_with_jwt_gets_all_child_files_should_succeed_with_200(
#     client, folder, headers, file
# ):
#     response = client.get(
#         f'/api/v1/files/{folder.id}/',
#         **headers,
#     )
#     assert response.status_code == 200
#     assert response.json()['message'] == 'Success'
#     assert len(response.json()['data']) == 1


# @pytest.mark.django_db
# def test_user_with_jwt_creates_file_should_succeed_with_200(
#     client,
#     folder,
#     headers,
#     celery_config,
# ):
#     filedata = {
#         'filename': 'file',
#         'file_type': 'type',
#         'parent_id': folder.id,
#         'file_size': 20.2,
#     }
#     response = client.post(
#         f'/api/v1/files/file-load/',
#         **headers,
#         data=filedata,
#     )
#     assert response.status_code == 200


# @pytest.mark.django_db
# def test_user_with_jwt_gets_download_link_should_succeed_with_200(
#     client, file, headers
# ):
#     response = client.get(
#         f'/api/v1/files/file-load/{file.id}/',
#         **headers,
#     )
#     assert response.status_code == 200
#     assert response.json()['message'] == 'Success'
#     assert isinstance(response.json()['token'], str) is True


# @pytest.mark.django_db
# @patch(
#     'main.views.FileSystemStorage.open',
#     MagicMock(return_value="Mock file"),
# )
# def test_user_with_jwt_downloads_file_should_succeed_with_200(
#     client, file_download_jwt
# ):
#     response = client.get(f'/api/v1/files/download/?token={file_download_jwt}')
#     assert response.status_code == 200
#     assert (
#         response.headers['Content-Disposition']
#         == 'attachment; filename=file.type'
#     )
#     assert response.headers['Content-Type'] == 'multipart/form-data'


# @pytest.mark.django_db
# def test_user_with_valid_data_creates_file_share_link_should_succeed_with_200(
#     client,
#     file,
#     headers,
#     celery_config,
# ):
#     response = client.post(
#         f'/api/v1/files/share-load/',
#         **headers,
#         data={'file_id': file.id, 'time': 60},
#     )
#     assert response.status_code == 200
#     assert response.data['message'] == "Success"
#     assert len(response.data['share_link_token']) > 0


# @pytest.mark.django_db
# @patch(
#     'main.views.FileSystemStorage.open',
#     MagicMock(return_value="Mock file"),
# )
# def test_user_without_authorization_downloads_public_file_with_share_link_should_succeed_with_200(
#     client,
#     file,
#     headers,
#     celery_config,
#     share_link,
# ):
#     response = client.get(
#         f'/api/v1/files/share-load/{share_link.share_token}/'
#     )
#     assert response.status_code == 200
#     assert (
#         response.headers['Content-Disposition']
#         == 'attachment; filename=file.type'
#     )
#     assert response.headers['Content-Type'] == 'multipart/form-data'


# @pytest.mark.django_db
# def test_user_with_valid_jwt_disables_all_share_links_for_specific_file_should_succeed_with_200(
#     client,
#     file,
#     headers,
#     celery_config,
#     share_link,
# ):
#     response = client.delete(f'/api/v1/files/share-load/{file.id}/', **headers)
#     assert response.status_code == 200
#     assert ShareLink.objects.count() == 0


# @pytest.mark.django_db
# def test_user_with_jwt_creates_already_existing_folder_with_200(
#     client,
#     headers,
#     folder,
# ):
#     response = client.post(
#         '/api/v1/files/',
#         **headers,
#         data={'filename': 'folder', 'is_folder': True, 'parent_id': ""},
#     )
#     assert response.status_code == 200
#     assert (
#         response.content
#         == b'{"message":"Folder with such name already exists in current directory"}'
#     )


# @pytest.mark.parametrize(
#     'url',
#     (
#         ('/api/v1/files/'),
#         ('/api/v1/files/1/'),
#         ('/api/v1/files/file-load/1/'),
#     ),
# )
# @pytest.mark.django_db
# def test_user_without_headers_connects_to_any_restricted_viewset_should_fail_with_403(
#     client, url
# ):
#     response = client.get(url)
#     assert response.status_code == 403


# @pytest.mark.django_db
# def test_user_without_jwt_in_headers_connects_to_any_viewset_should_fail_with_403(
#     client, headers_with_no_token
# ):
#     response = client.get('/api/v1/files/', **headers_with_no_token)
#     assert response.status_code == 403


# @pytest.mark.django_db
# def test_user_with_expired_jwt_in_headers_connects_to_any_viewset_should_fail_with_403(
#     client, headers_with_exp_jwt
# ):
#     time.sleep(2)
#     response = client.get('/api/v1/files/', **headers_with_exp_jwt)
#     assert response.status_code == 403


# @pytest.mark.django_db
# def test_user_with_non_valid_jwt_in_headers_connects_to_any_viewset_should_fail_with_403(
#     client, headers_with_non_valid_token
# ):
#     response = client.get('/api/v1/files/', **headers_with_non_valid_token)
#     assert response.status_code == 403


# @pytest.mark.django_db
# def test_user_with_jwt_creates_folder_with_non_valid_data_should_fail_with_200(
#     client,
#     headers,
# ):
#     response = client.post(
#         '/api/v1/files/',
#         **headers,
#         data={
#             'is_folder': True,
#             'parent_id': "",
#         },
#     )
#     assert response.status_code == 200
#     assert response.content == b'{"message":"Your data is problematic!"}'


# @pytest.mark.django_db
# def test_user_with_jwt_create_file_with_non_valid_data_should_fail_with_200(
#     client,
#     folder,
#     headers,
#     celery_config,
# ):
#     filedata = {
#         'parent_id': folder.id,
#     }
#     response = client.post(
#         f'/api/v1/files/file-load/',
#         **headers,
#         data=filedata,
#     )
#     assert response.status_code == 200
#     assert response.content == b'{"message":"Your data is problematic!"}'


# @pytest.mark.django_db
# def test_bg_job_file_addition_changes_root_folder_size_should_succeed(
#     celery_config,
#     client,
#     folder,
#     file,
#     headers,
#     user,
# ):
#     profile_stats_create.apply((user.id, file.id))
#     parent_file_size = (
#         File.objects.all_with_deleted().get(pk=file.id).parent.file_size
#     )
#     assert parent_file_size == 20.2


# @pytest.mark.django_db
# def test_bg_job_file_deletion_changes_root_folder_size_should_succeed(
#     celery_config,
#     client,
#     folder,
#     file,
#     headers,
#     user,
# ):
#     profile_stats_deletion.apply((user.id, file.id))
#     parent_file_size = (
#         File.objects.all_with_deleted().get(pk=file.id).parent.file_size
#     )
#     assert parent_file_size == 0.0


# @pytest.mark.django_db
# def test_bg_job_deletion_of_soft_deleted_files_and_folders_should_succeed(
#     celery_config,
#     client,
#     folder,
#     headers,
# ):
#     File.objects.all().delete()
#     db_clean_up.apply()
#     assert File.all_objects.all().count() == 0


# @pytest.mark.django_db
# def test_bg_job_deletion_of_expired_share_file_link_should_succeed(
#     celery_config,
#     client,
#     folder,
#     headers,
#     expired_share_link,
# ):
#     delete_expired_share_links.apply()
#     assert ShareLink.all_objects.all().count() == 0
