class LoginAction(MenuAction):
    def __init__(self, view_name, data: User | None = None):
        super().__init__(data)
        self.view_name = view_name

    def execute(self):
        if self.data is None:
            print("Invalid user data")
            ViewManager.switch_view("login", self.result)

        self.result = None
        try:
            self.login_user()
            Model().save_users()
            ViewManager.switch_view(self.view_name, self.result)

        except PyStocksException as e:
            retry = input(e.message)
            if retry.lower() == "y":
                ViewManager.switch_view("login", self.result)
            else:
                ViewManager.switch_back()
 
    def login_user(self):
        user = Model().users.find(self.data.name, self.data.password)
        if user is not None:
            user.logged_in = True
            self.result = user
        else:
            raise PyStocksException("unknown_user")

class PyStocksException(Exception):
    def __init__(self, message: str):
        self.message = message if Model().error_messages is None else Model().error_messages.get_error_message(message)
