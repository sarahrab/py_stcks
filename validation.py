import  requests
from fastapi import FastAPI

class TransactionValidation:
    app = FastAPI()
    validation_url = ""

    @classmethod
    def validate_transaction(cls) -> bool:
        response = requests.get(cls.validation_url).json()
        # check result   result = response["result"]
        return True # False