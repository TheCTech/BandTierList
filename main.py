from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

import sys
import os
import logging
from colorlog import ColoredFormatter

from logging.handlers import RotatingFileHandler

from ui_utils import HomeScreen, ListScreen, ProfileScreen
from data_persistency import SavedData


# region setup
os.makedirs("cache", exist_ok=True) # Create cache folder for saving data
os.makedirs("logs", exist_ok=True) # Create logs folder for storing logs

handler = logging.StreamHandler(sys.stdout)

formatter = ColoredFormatter(
    "[%(log_color)s%(levelname)s%(reset)s %(name)s]: %(message)s",
    log_colors={
        "DEBUG": "cyan",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    }
)

handler.setFormatter(formatter)

logger = logging.getLogger()
logger.handlers = []
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

file_handler = RotatingFileHandler(
    "logs/app.log",
    maxBytes=2_000_000,
    backupCount=3,
    encoding="utf-8"
)

file_formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s %(name)s]: %(message)s"
)

file_handler.setFormatter(file_formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(file_handler)

# endregion

class MusixApp(App):
    def build(self):
        self.saved_data = SavedData()

        self.sm = ScreenManager()

        self.home_screen = HomeScreen(name="home_screen", saved_data=self.saved_data)
        self.sm.add_widget(self.home_screen)

        self.list_screen = ListScreen(name="list_screen", saved_data=self.saved_data)
        self.sm.add_widget(self.list_screen)

        self.profile_screen = ProfileScreen(name="profile_screen", saved_data=self.saved_data)
        self.sm.add_widget(self.profile_screen)

        self.sm.current = "home_screen"

        return self.sm


if __name__ == "__main__":
    logger.info("APP STARTING")
    MusixApp().run()