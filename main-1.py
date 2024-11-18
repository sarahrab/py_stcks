from view import View

if __name__ == '__main__':
    print("Start")
    v = View("welcome")
    v.show()
    v.show_menu()

    v1 = View("login")
    v1.show()
    v1.show_menu()