from typing import Optional

import requests
from fastapi import FastAPI
from requests import Response

from exceptions.AttemptsException import AttemptsException
from exceptions.ValidationException import ValidationException


class ValidationResult:
    result: Optional[bool] = False
    success: bool
    error: str
    status_code: int

    def __init__(self, response: Response | None = None):
        self.result = False
        self.success = response.ok
        self.error = "" if response.ok else response.reason
        self.status_code = response.status_code
        self.update_result(response)

    def update_result(self, response: Response):
        if self.success:
            json = response.json()
            self.result = json["can_execute"]


class TransactionValidation:
    # app = FastAPI()
    validation_url = ""
    max_tries = 5

    @classmethod
    def validate_transaction(cls) -> ValidationResult:
        attempt= 0
        while attempt < cls.max_tries:
            try:
                r = requests.get(cls.validation_url)
                return ValidationResult(r)

            except requests.Timeout as err:
                attempt += 1

            except requests.RequestException as err:
                raise ValidationException(err.strerror)

        raise AttemptsException(f"validation failed. number of attempts exceeds {cls.max_tries}")

