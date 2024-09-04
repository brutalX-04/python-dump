__title__ = 'XModLb'
__author__ = 'Rizky Nurahman'
__license__ = 'MIT'
__copyright__ = 'Copyright 2023 Rizky Nurahman'
__version__ = '0.0.1'
__description__ = 'This library was created to shorten the process of creating Python scripts.'


from .XmodLb import *

from requests import get
from colorama import Fore, Style

latestVersion = get("https://pypi.org/pypi/XModLb/json").json()["info"]["version"]

if __version__ != latestVersion:
    print(f"{Fore.RED}WARNING:{Style.RESET_ALL} You are using an outdated version of XModLb ({__version__}). The latest version is {latestVersion}.")