from abc import ABC, abstractmethod


class ReaderBase(ABC):

    @abstractmethod
    def read_string(self, prompt: str | None) -> str:
        pass

    @abstractmethod
    def read_int(self, prompt: str | None) -> int:
        pass


class WriterBase(ABC):

    @abstractmethod
    def write(self, text: str):
        pass

