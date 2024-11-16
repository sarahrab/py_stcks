from typing import Dict

from pydantic import BaseModel


class ErrorManager(BaseModel):
    errors: Dict[str, str] = {}

    def get_error_message(self, error: str) -> str:
        return self.errors.get(error, "")
