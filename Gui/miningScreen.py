import io
import threading
import time
from threading import Thread

from kivy import Logger
from kivy.clock import Clock
from kivy.graphics import Line
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, OptionProperty
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.core.image import Image as CoreImage

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

import chromedriver_autoinstaller
from misc.config import Config


class MiningScreen(Screen):
    usrName = StringProperty("")
    pwdInput = StringProperty("")
    stopOnlyWhenStopPressed = BooleanProperty(False)
    mineUntilPoints = NumericProperty(None)
    mineForTime = NumericProperty(None)
    requireAll = BooleanProperty(True)
    mode = OptionProperty(Config.get("Mining", "mode"), options=["Blatant", "Ghost"])
    midLinePos = NumericProperty(0)

    driver = None

    def on_pre_enter(self, *args):
        self.mode = Config.get("Mining", "mode")

        self.ids["InfoLabel"].text = "Mining Mode - " + str(self.mode)

        if not self.stopOnlyWhenStopPressed:
            try:
                self.ids["InfoLabel"].text = self.ids["InfoLabel"].text + "\nMine for " + str(int(self.mineForTime)) + \
                                             " minutes"
            except TypeError:
                pass
            try:
                self.ids["InfoLabel"].text = self.ids["InfoLabel"].text + "\nStop when " + \
                                             str(int(self.mineUntilPoints)) + " points reached"
            except TypeError:
                pass
            self.ids["InfoLabel"].text = self.ids["InfoLabel"].text + "\nRequire All - " + str(self.requireAll)

        self.ids["InfoLabelHidden"].text = self.ids["InfoLabel"].text
        self.ids["InfoLabelHidden"].texture_update()

        self.midLinePos = self.ids["InfoLabelHidden"].texture_size[0] + self.ids["InfoLabelHidden"].right
        self.ids["LabelHolder"].width = self.midLinePos

    def on_size(self, *args, **kwargs):
        self.draw()


    def on_midLinePos(self, *args, **kwargs):
        self.draw()

    def draw(self):
        self.canvas.after.clear()

        with self.canvas.after:
            Line(points=[self.midLinePos, 0, self.midLinePos, self.height - self.ids["Nav"].height], width=2,
                 cap="none", joint="none", close=False)

    def on_enter(self, *args):
        Thread(target=self.mine).start()

    def update_image(self, _):
        data = io.BytesIO(self.driver.get_screenshot_as_png())

        coreImage = CoreImage(data, ext="png")
        texture = coreImage.texture
        self.ids["WebpageImage"].texture = texture

    def mine(self):
        Logger.info("Miner: Started mining function")

        chromedriver_autoinstaller.install()
        Logger.info("Miner: Chromedriver installed if not already")

        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        Logger.info("Miner: Chromedriver setup")

        url = Config.get("Mining", "url")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        Logger.info("Miner: Loaded " + str(url))

        self.driver = driver
        screenShotClock = Clock.schedule_interval(self.update_image, 1)
        Logger.info("Miner: Started window viewer clock")


        time.sleep(100)


        screenShotClock.cancel()
        Logger.info("Miner: Finished mining function")