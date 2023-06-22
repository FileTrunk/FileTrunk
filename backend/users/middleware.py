import jwt
from django.conf import settings
from django.http import HttpRequest


class JWTDecodeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        try:
            encoded = request.headers.get("Authorization")[9:]
            decoded_jwt = jwt.decode(
                encoded, settings.CLIENT_SECRET, algorithms="HS256"
            )
        except (
            jwt.exceptions.DecodeError,
            TypeError,
            jwt.exceptions.ExpiredSignatureError,
        ):
            request.user_id = None
            return self.get_response(request)
        request.user_id = decoded_jwt["user_id"]
        return self.get_response(request)


class DisableCSRFMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
        return self.get_response(request)
