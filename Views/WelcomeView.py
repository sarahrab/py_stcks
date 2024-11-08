from basics import *

class WelcomeView(View):
    def __init__(self, title, menu: Menu = None):
        super().__init__(title, menu)

    def show(self):
        print("Welcome, friend!")




