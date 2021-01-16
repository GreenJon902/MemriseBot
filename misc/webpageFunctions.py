from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from misc.config import Config
from kivy.logger import Logger


def wait_till_page_load(driver, timeout=Config.getint("Mining", "page_timeout")):
    try:
        Logger.info("WebDriverWait: Starting")
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
        Logger.info("WebDriverWait: Finished")
    except TimeoutException:
        Logger.critical("WebDriverWait: Waiting took to long")
