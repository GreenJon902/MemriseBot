import sys
from threading import Thread

import chromedriver_autoinstaller
import selenium
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class Bot:
    should_run = False
    need_close = False
    callback: callable
    driver: selenium.webdriver.Chrome
    translation: str

    def __init__(self, callback):
        self.callback = callback

        Thread(target=self.chrome_handler).start()

    def start_bot(self, translation):
        self.callback("log", "Starting")
        self.translation = translation
        self.should_run = True

    def end_bot(self):
        self.should_run = False

    def end(self):
        self.end_bot()
        self.need_close = True

    def chrome_handler(self):
        chromedriver_autoinstaller.install()

        options = selenium.webdriver.chrome.options.Options()
        options.set_capability("unhandledPromptBehavior", "dismiss")

        self.driver = selenium.webdriver.Chrome(options=options)
        self.driver.set_window_size(700, 700)
        self.driver.get("https://www.memrise.com/home/")

        while not self.need_close:
            if self.should_run:
                path = None
                for element in self.driver.find_elements_by_tag_name("a"):
                    if "Review" in element.text:
                        path = element.get_attribute("href")
                        break

                if path is None:
                    print("Failed")
                    print(
                        "Could not get attribute href from element with text \"review\", maybe your on the wrong page, "
                        "the url should end with \"name of the course/level number/\"!\ne.g.german/4")
                    sys.exit()

                print("Running")

            while self.should_run:
                try:
                    self.driver.get(path)

                    WebDriverWait(self.driver, 1000).until(
                        expected_conditions.presence_of_element_located((By.XPATH, "/html/body/div[4]/div[3]/div/div/div[4]/input")))
                    self.driver.find_element_by_xpath("/html/body/div[4]/div[3]/div/div/div[4]/input").send_keys(self.translation)

                    WebDriverWait(self.driver, 1000).until(
                        expected_conditions.presence_of_element_located((By.XPATH, "/html/body/div[4]/div[3]/div/div/div[1]/button/span")))
                    self.driver.find_element_by_xpath("/html/body/div[4]/div[3]/div/div/div[1]/button/span").click()

                    WebDriverWait(self.driver, 1000).until(
                        expected_conditions.presence_of_element_located((By.XPATH, "/html/body/div[5]/div[3]/div/div/div[3]/span[2]")))

                except Exception as e:
                    print("failed", e)

        self.driver.close()
