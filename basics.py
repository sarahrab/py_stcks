class MenuAction:
    def __init__(self, data: object | None = None):
        self.data = data
        self.result = None

    def execute(self):
        pass


class MenuItem:
    def __init__(self, id: str, text: str, action: MenuAction):
        self.id = id
        self.text = text
        self.action = action

    def show(self):
        print(f"{self.id}: {self.text}")

    def execute(self, data: object | None = None):
        self.action.data = data
        self.action.execute()


class Menu:
    def __init__(self, title):
        self.title = title
        self.items = []

    def add_item(self, item: MenuItem):
        self.items.append(item)

    def get_item(self, id: str) -> MenuItem | None:
        for item in self.items:
            if item.id == id:
                return item
        return None

    def show(self, data: object | None = None):
        for item in self.items:
            item.show()

    def run(self, data: object | None = None):
        self.show(data)
        option = input()
        item = self.get_item(option)
        if item is not None:
            item.execute(data)

    def count(self) -> int:
        return len(self.items)


class View:
    def __init__(self, name, menu: Menu = None):
        self.name = name
        self.menu = menu
        self.data = None

    def show(self):
        pass

    def show_menu(self):
        if self.menu is not None:
            self.menu.run(self.data)
