from misc.config import Config
from kivy.logger import Logger


def wait_till_page_load(driver, timeout=Config.getint("Mining", "page_timeout")):
    Logger.info("WebDriverWait: Starting")
    driver.implicitly_wait(timeout)
    Logger.info("WebDriverWait: Finished")

