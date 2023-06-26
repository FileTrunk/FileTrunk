# Documentation

### Description:
Great file hosting service for you. This app provides not only handy file storage with easy sign up, but an ability to share files and receive analytics about taken storage. This app enhances concepts of background tasks and REST API in order to achieve flexibility and quick action.

Apart from that, there is an integrated admin panel in the app for the developer. 

### Stack:
*Languages*: Python, Javascript

*Frameworks*: Django, Django REST, React

*Spec. libraries*: celery, redis, google-auth, gunicorn, pytest

*Database*: PostgreSQL

*Error-handling*: sentry-sdk

### Tables
![UML diagram](umlclass.png?raw=true "Classes UML Diagram")

### API:
```
Path: /api/v1/users/google-login/
Allow: POST
Content-Type: application/json
Details: On this endpoint token, obtained from google authorization on frontend, is sent and user is being created/logged in and JWT authentication token is sent back and saved on the user side as cookie.
```

```
Path: /api/v1/users/me/
Allow: GET
Content-Type: application/json
Details: Return information about the user.
```

```
Path: /api/v1/users/user-stats/
Allow: GET
Content-Type: application/json
Details: Return user statistics regarding saved files by user.
```

```
Path: /api/v1/files/
Allow: GET, POST, DELETE
Content-Type: application/json
Details: Endpoint for creation of folders, deletion of files/folders and obtaining information about file/files(in specific folder). Files are soft-deleted at first and then cleared by background job.
```

```
Path: /api/v1/files/file-load/
Allow: GET, POST
Content-Type: multipart/form-data
Details: Endpoint for file upload and downloading file.
```

```
Path: /api/v1/files/share-load
Allow: GET, POST, DELETE
Content-Type: application/json
Details: Endpoint for deactivating and creating temporary file links. Although downloading files by the links.
```

### Authorization/Authentication
In order to authorize in the app, the user has only an option to use Google OAuth 2.0. 
![OAuth diagram](oauthdiag.png?raw=true "OAuth 2.0 Diagram")
On the diagram above depicted the way the user is authorized in the app. As backend verifies google token, the **JWT token** is created using app's secret and user's id. After that, this JWT token is saved on the user side as a cookie. Everytime the frontend does an authorized request to the backend, it adds this token in the header of the request, this token is then verified on the backend side and information from it is decoded.

### Background tasks
For background tasks the **celery** was used, which is run in a different process. In order for Django to communicate with celery **redis** was used as a broker. The following processes were taken into the background:

- Identifying and cleaning expired links from the database. *Regularity*: every 2 minutes.
- Removal of previously deleted files by users. *Regularity*: every 24 hours.
- Updating user statistics. *Toggle*: every time file/folder is deleted/uploaded.
- Updating folders metadata. *Toggle*: every time file/folder is deleted/uploaded.

Background tasks transfered resource heavy tasks in a different queue and thus freed up a lot of time for the user, who doesn't need to wait for this tasks to end before receiving response and keep working with the application.

### Exceptions handling
In order to log exceptions on the production side **sentry** service is used - every error is fixated by sentry-sdk and can be found on the sentry project page.