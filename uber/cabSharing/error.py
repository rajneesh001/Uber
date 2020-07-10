from rest_framework import status
from rest_framework.settings import api_settings


class Error:
    status = status.HTTP_400_BAD_REQUEST

    def __init__(self, message, status=None):
        self.message = message
        if status is not None:
            self.status = status

    def get_response(self):
        return {api_settings.NON_FIELD_ERRORS_KEY: self.message}
