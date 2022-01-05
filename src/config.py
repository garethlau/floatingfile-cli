import os
import sys
import configparser
from dotenv import load_dotenv

# https://stackoverflow.com/questions/41864951/pyinstaller-3-adding-datafiles-with-onefile/42145611#42145611
if getattr(sys, "frozen", False):
    extDataDir = sys._MEIPASS
else:
    extDataDir = os.getcwd()

load_dotenv(dotenv_path=os.path.join(extDataDir, ".env"))


def init():
    file_path = os.path.join(os.getenv("HOME"), ".floatingfile", "settings.ini")
    if not os.path.isfile(file_path):
        config = configparser.ConfigParser()
        config["profile"] = {"username": "Anonymous"}
        config["download"] = {"dir": "Downloads", "group_by_space": "Yes"}
        with open(file_path, "w") as f:
            config.write(f)


API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")


config = configparser.ConfigParser()


def get_username():
    config.read(os.path.join(os.getenv("HOME"), ".floatingfile", "settings.ini"))
    return config["profile"]["username"]


def get_download_path(code=None):
    config.read(os.path.join(os.getenv("HOME"), ".floatingfile", "settings.ini"))

    download_dir = config["download"]["dir"]
    group_by_space = config["download"]["group_by_space"]

    if group_by_space == "Yes":
        return os.path.join(os.getenv("HOME"), download_dir, code)
    return os.path.join(os.getenv("HOME"), download_dir)


BASE_HEADERS = {"api-key": API_KEY}
