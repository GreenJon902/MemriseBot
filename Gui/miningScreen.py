import io
import time
from threading import Thread

from kivy import Logger
from kivy.clock import Clock
from kivy.graphics import Line
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, OptionProperty, DictProperty
from kivy.uix.screenmanager import Screen
from kivy.core.image import Image as CoreImage

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

import chromedriver_autoinstaller
from misc.config import Config
from misc.memriseElements import MemriseElements


class MiningScreen(Screen):
    MinerSettings = DictProperty({
        "usrName": StringProperty(""),
        "pwdInput": StringProperty(""),
        "mineUntilPoints": NumericProperty(None),
        "mineForTime": NumericProperty(None),
        "requireAll": BooleanProperty(True),
        "mode": OptionProperty(Config.get("Mining", "mode"), options=["Blatant", "Ghost"]),
        "webpage_image_update_interval": Config.getint("Gui", "webpage_image_update_interval")
    })

    Miner = None

    midLinePos = NumericProperty(0)
    stopOnlyWhenStopPressed = BooleanProperty(False)

    def on_pre_enter(self, *args):
        self.MinerSettings["mode"] = Config.get("Mining", "mode")
        self.MinerSettings["webpage_image_update_interval"] = Config.getint("Gui", "webpage_image_update_interval")

        self.ids["InfoLabel"].text = "Mining Mode - " + str(self.MinerSettings["mode"])

        if not self.stopOnlyWhenStopPressed:
            try:
                self.ids["InfoLabel"].text = self.ids["InfoLabel"].text + "\nMine for " + str(int(self.MinerSettings["mineForTime"])) + \
                                             " minutes"
            except TypeError:
                pass
            try:
                self.ids["InfoLabel"].text = self.ids["InfoLabel"].text + "\nStop when " + \
                                             str(int(self.MinerSettings["mineUntilPoints"])) + " points reached"
            except TypeError:
                pass
            self.ids["InfoLabel"].text = self.ids["InfoLabel"].text + "\nRequire All - " + str(self.MinerSettings["requireAll"])

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
        self.Miner = self._Miner(**self.MinerSettings)

        Thread(target=self.Miner.start, daemon=True).start()

    # Miner ------------------------------------------------------------------------------------------------------------

    class _Miner:
        do_webpage_image_update = False
        driver = None

        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

        def start(self):
            self.install_dependants()
            self.set_up()
            self.do_webpage_image_update = True
            self.mine()
            self.do_webpage_image_update = False

        def webpage_image_update(self, coreImage, t):
            texture = coreImage.texture
            self.ids["WebpageImage"].texture = texture

            Logger.debug("WebpageImage: Finished image update in " + str(time.time() - t))

        def webpage_image_updater(self):
            while self.do_webpage_image_update:
                t = time.time()

                Logger.debug("WebpageImage: Starting image update")

                data = io.BytesIO(self.driver.get_screenshot_as_png())

                coreImage = CoreImage(data, ext="png")
                Clock.schedule_once(lambda _: self.webpage_image_update(coreImage, t), 0)

                time.sleep(self.webpage_image_update_interval - (time.time() - t))

        def install_dependants(self):
            chromedriver_autoinstaller.install()
            Logger.info("Miner: Chromedriver installed if not already")

        def set_up(self):
            try:
                self.driver.quit()
            except AttributeError:
                pass

            chromedriver_autoinstaller.install()
            Logger.info("Miner: Chromedriver installed if not already")

            chrome_options = ChromeOptions()
            if Config.getboolean("Gui", "headless"):
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=1920,1080")
            Logger.info("Miner: Chromedriver setup")

            url = Config.get("Mining", "url")
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.get(url)

            Logger.info("Miner: Loaded " + str(url))

        def mine(self):
            Logger.info("Miner: Started mining function")

            MemriseElements.get("username_input", self.driver).send_keys(self.usrName)
            MemriseElements.get("password_input", self.driver).send_keys(self.pwdInput)
            MemriseElements.get("login_submit_button", self.driver).click()

            time.sleep(5)

            self.driver.close()

            Logger.info("Miner: Finished mining function")
