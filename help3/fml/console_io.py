from base import WriterBase, ReaderBase


class ConsoleWriter(WriterBase):
    def write(self, text: str):
        print(text)


class ConsoleReader(ReaderBase):
    def read_string(self, prompt: str | None) -> str:
        return input(prompt)

    def read_int(self, prompt: str | None) -> int:
        value= input(prompt)
        try:
            number = int(value)
            return  number

        except ValueError:
            print("invalid format!")
            return  0
