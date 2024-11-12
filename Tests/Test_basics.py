from basics import Menu, MenuItem, MenuAction


def test_menu_add():
    menu = Menu("menu")
    a = MenuAction()
    menu.add_item(MenuItem("1", "item1", a))
    assert len(menu.items) == 1
