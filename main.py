from statistics import mode

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ToggleButtonBehavior

class LoginScreen(Screen):
    pass


class HomeScreen(Screen):
    pass


class ImageButton(ButtonBehavior, Image):
    pass


class ToggleButton(ToggleButtonBehavior, Image):
    pass


GUI = Builder.load_file("main.kv")


class MainApp(App):
    def build(self):
        return GUI

    def change_screen(self, screen_name):
        screen_manager = self.root.ids['screen_manager']
        screen_manager.current = screen_name

    def set_current_mode(self, mode_selected):
        global mode
        mode = mode_selected
        print(mode)
        return mode

    def get_current_mode(self):
        print(mode)
        return mode

MainApp().run()