import requests


class ValidationException(requests.RequestException):
    def __init__(self, message):
        super().__init__(message)