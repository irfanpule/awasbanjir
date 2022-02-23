from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError
from rest_framework import authentication
from rest_framework import exceptions, HTTP_HEADER_ENCODING
from perangkat.models import Perangkat


class DeviceAPIAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        self.validate_token(request)
        return AnonymousUser(), None

    def validate_token(self, request):
        header = self.get_header(request)
        if header is None:
            raise exceptions.AuthenticationFailed('Tidak terdapat server key pada request')
        raw_token = self.get_raw_token(header)
        if raw_token is None:
            raise exceptions.AuthenticationFailed('Kesalahan dalam Authorization Device Id')

        try:
            if not Perangkat.objects.filter(device_id=raw_token.decode('utf8')).exists():
                raise exceptions.AuthenticationFailed('Device Id tidak valid')
        except ValidationError:
            raise exceptions.AuthenticationFailed('Device Id tidak valid')

        request.device_id = raw_token.decode('utf8')
        return None

    def get_header(self, request):
        header = request.META.get('HTTP_AUTHORIZATION')
        if isinstance(header, str):
            header = header.encode(HTTP_HEADER_ENCODING)

        return header

    def get_raw_token(self, header):
        parts = header.split()

        if len(parts) == 0:
            return None

        if parts[0].decode(HTTP_HEADER_ENCODING) != "Device":
            raise exceptions.AuthenticationFailed('Authorization bukan dari perangkat yang valid',
                                                  code='bad_authorization_header')

        if len(parts) != 2:
            raise exceptions.AuthenticationFailed(
                'Authorization berisi dua nilai yang dipisahkan dengan spasi',
                code='bad_authorization_header',
            )

        return parts[1]
