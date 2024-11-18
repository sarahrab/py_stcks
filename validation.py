import requests
from fastapi import FastAPI
from requests import Response


class ValidationResult:
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

    @classmethod
    def validate_transaction(cls) -> ValidationResult:
        try:
            r = requests.get(cls.validation_url)
            return ValidationResult(r)

        except Exception as e:
            vr = ValidationResult()
            vr.success = False
            vr.ok = False
            vr.error = repr(e)
            return vr
