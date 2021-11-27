from kivy.logger import Logger
from misc.config import Config


def wait_till_page_load(driver, timeout=Config.getint("Mining", "page_timeout")):
    Logger.info("WebDriverWait: Starting")
    driver.implicitly_wait(timeout)
    Logger.info("WebDriverWait: Finished")

