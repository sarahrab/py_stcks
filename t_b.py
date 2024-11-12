from Views.WelcomeView import WelcomeView
from actions import LoginAction, SwitchViewAction
from basics import Menu, MenuItem, MenuAction

def test_menu_create():
    menu = Menu("menu")
    assert menu and menu.title == "menu"
def test_menu_add():
    menu = Menu("menu")
    a = MenuAction()
    menu.add_item(MenuItem("1", "item1", a))
    assert len(menu.items) == 1

def test_menu_get():
    menu = Menu("menu")
    a = MenuAction()
    menu.add_item(MenuItem("1", "item1", a))
    item = menu.get_item("1")
    assert item is not None and item.text == "item1"

def test_welcome_view():
    v = WelcomeView("welcome")
    v.create_menu()
    assert len(v.menu.items) == 3
    item = v.menu.get_item("1")
    assert item is not None and item.action is not None and type(item.action) is SwitchViewAction
    #isinstance(item.action, LoginAction)

