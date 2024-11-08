from stocks import Stocks

class User:
    def __init__(self, name, password, amount: int = 0):
        self.name = name
        self.password = password
        self.amount = amount

class UserAccount(User):
    def __init__(self, name, password, amount: int = 0):
        super().__init__(name, password, amount)
        self.loggedIn = False
        self.stocks = Stocks()

class UserManager:
    def __init__(self):
        self.users = []

    def find(self, name: str, password: str | None = None) -> UserAccount | None:
        for user in self.users:
            if user.name == name and (password is None or user.password == password):
                return user
        return None

    def add(self, name: str, password: str, amount: int) -> UserAccount | None:
        user = self.find(name, password)
        if user is None:
            user = UserAccount(name, password, amount)
            self.users.append(user)
        return user

    def remove(self, name: str) -> bool:
        user = self.find(name)
        if user is not None:
            if user.stocks.count() == 0:
                user.loggedIn = False
                self.users.remove(user)
                return True
        return False

