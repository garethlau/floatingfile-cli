import os
import sys
from dotenv import load_dotenv

# https://stackoverflow.com/questions/41864951/pyinstaller-3-adding-datafiles-with-onefile/42145611#42145611
if getattr(sys, "frozen", False):
    extDataDir = sys._MEIPASS
else:
    extDataDir = os.getcwd()

load_dotenv(dotenv_path=os.path.join(extDataDir, ".env"))


API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")


BASE_HEADERS = {"api-key": API_KEY}
