import os

from kivy.config import ConfigParser

from misc import user_data_dir

Config = ConfigParser()
Config.read(os.path.join(user_data_dir, "config.ini"))


def create():
    for section in Config.sections():
        Config.remove_section(section)

    with open(os.path.join(user_data_dir, "config.ini"), 'w'):
        Config.write()
