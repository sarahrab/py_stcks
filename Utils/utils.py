class Utils:

    @classmethod
    def get_int(cls, prompt: str) -> int:
        value= input(prompt)
        try:
            number = int(value)
            return  number
        except ValueError:
            print("invalid format!")
            return  0
