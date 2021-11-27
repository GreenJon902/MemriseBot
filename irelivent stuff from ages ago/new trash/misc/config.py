import os

from kivy.config import ConfigParser
from misc import user_data_dir

Config = ConfigParser()
Config.read(os.path.join(user_data_dir, "config.ini"))


def create():
    """    for section in Config.sections():
        Config.remove_section(section)

    Config.add_section("Misc")
    Config.add_section("Mining")
    Config.add_section("Gui")"""
    Config.remove_section("Memrise_Element")
    Config.remove_section("URLs")
    Config.add_section("Memrise_Element")
    Config.add_section("URLs")

    Config.set("Mining", "page_timeout", 10)

    Config.set("URLs", "sign_in", "https://app.memrise.com/signin")
    Config.set("URLs", "groups", "https://app.memrise.com/groups/")

    Config.set("Gui", "webpage_image_update_interval", 0.5)
    #Config.set("Gui", "headless", True)

    Config.set("Memrise_Element", "username_input-id", "username")
    Config.set("Memrise_Element", "password_input-id", "password")
    Config.set("Memrise_Element", "login_submit_button-xpath", "//*[@id=\"__next\"]/div/div[2]/div/form/div[3]/div[1]/button")
    Config.set("Memrise_Element", "courses-class_name", "course-card-container")
    Config.set("Memrise_Element", "course_title-class_name", "title")
    Config.set("Memrise_Element", "groups-xpath", "//*[@id=\"content\"]/div/div[2]/div[2]/div")
    Config.set("Memrise_Element", "groups_individual-class_name", "class-view")
    Config.set("Memrise_Element", "groups_individual_title-class_name", "class-name")
    Config.set("Memrise_Element", "groups_individual_courses-class_name", "course-view")

    Config.set("Misc", "saveLogins", True)
    #Config.set("Misc", "username", "")#for testing
    #Config.set("Misc", "password", "")


    with open(os.path.join(user_data_dir, "config.ini"), 'w'):
        Config.write()
