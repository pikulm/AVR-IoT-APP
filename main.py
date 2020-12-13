from statistics import mode

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ToggleButtonBehavior
from google.cloud import iot_v1


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
        self.mode = mode_selected
        print(self.mode)
        return self.mode

    def get_current_mode(self):
        print(self.mode)
        return self.mode

    def set_current_color(self, color_selected):
        self.color = color_selected
        print(self.color)
        return self.color

    def get_current_color(self):
        print(self.color)
        return self.color

    def set_config(self):
        service_account_json = "/Users/magdalenapikul/.gcpkey/avr-iot-led-8dfc70c2f480.json"
        project_id = "avr-iot-led"
        cloud_region = "us-central1"
        registry_id = "AVR-IOT"
        device_id = "d01234019E0F3381BFE"
        version = 0
        config = "\"autoMode\":{mode}, \"color\":\"{color}\"".format(mode=self.mode, color=self.color)

        print("Set device configuration")
        client = iot_v1.DeviceManagerClient()
        device_path = client.device_path(project_id, cloud_region, registry_id, device_id)

        data = config.encode("utf-8")

        return client.modify_cloud_to_device_config(
            request={"name": device_path, "binary_data": data, "version_to_update": version}
        )
        # [END iot_set_device_config]




MainApp().run()