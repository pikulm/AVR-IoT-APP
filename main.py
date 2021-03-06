from statistics import mode

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ToggleButtonBehavior
from google.cloud import iot_v1
import hashlib
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS']="avr-iot-led-8dfc70c2f480.json"

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

    def change_screen(self):
        screen_manager = self.root.ids['screen_manager']
        if self.verification_result == "ok":
            screen_manager.current = "home_screen"
        else:
            screen_manager.current = "login_screen"

    def set_current_mode(self, mode_selected):
        self.mode = mode_selected
        return self.mode

    def set_current_color(self, color_selected):
        self.color = color_selected
        return self.color

    def set_config(self):
        service_account_json = "avr-iot-led-8dfc70c2f480.json"
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

    def set_id_to_verify(self, id_to_verify):
        self.id_to_verify = id_to_verify
        return self.id_to_verify

    def set_password_to_verify(self, password_to_verify):
        self.password_to_verify = password_to_verify
        return self.password_to_verify

    def hash_login(self):
        self.hashed_password = hashlib.sha256(self.password_to_verify.encode('utf-8')).hexdigest()
        self.hashed_id = hashlib.sha256(self.id_to_verify.encode('utf-8')).hexdigest()
        return self.hashed_password
        return self.hashed_id

    def verify_login(self):
        if self.hashed_id == "7e1c9d8563d1e9582bf4303df7d7e0c655d28960db12be775a5c3b071a60e688"\
        and self.hashed_password == "fe27ac4eb0f053a51ff724ef445f7f48acd653d7544477abfe788b1414d53f32":
            self.verification_result = "ok"
        else:
            self.verification_result = "bad"

        return(self.verification_result)

MainApp().run()