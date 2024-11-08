from basics import View

class RegisterUserView(View):
    def __init__(self, name, password, amount: int):
        super().__init__(name)
