import io
import os
import time
from threading import Thread

from kivy import Logger
from kivy.clock import Clock
from kivy.event import EventDispatcher
from kivy.graphics import Line
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, OptionProperty, DictProperty
from kivy.uix.screenmanager import Screen
from kivy.core.image import Image as CoreImage

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions

import chromedriver_autoinstaller
from selenium.webdriver.common.alert import Alert

from misc import user_data_dir
from misc.webpageFunctions import wait_till_page_load
from misc.config import Config
from misc.memriseElements import MemriseElements


class MiningScreen(Screen):
    Miner = None

    midLinePos = NumericProperty(0)
    stopOnlyWhenStopPressed = BooleanProperty(False)

    def __init__(self, *args, **kwargs):
        self.Miner = self._Miner()
        self.Miner.Gui = self

        super(MiningScreen, self).__init__(*args, **kwargs)

    def on_pre_enter(self, *args):
        if not self.stopOnlyWhenStopPressed:
            try:
                self.ids["InfoLabel"].text = self.ids["InfoLabel"].text + "\nMine for " + str(int(self.Miner.mineForTime)) + \
                                             " minutes"
            except TypeError:
                pass
            try:
                self.ids["InfoLabel"].text = self.ids["InfoLabel"].text + "\nStop when " + \
                                             str(int(self.Miner.mineUntilPoints)) + " points reached"
            except TypeError:
                pass
            self.ids["InfoLabel"].text = self.ids["InfoLabel"].text + "\nRequire All - " + str(self.Miner.requireAll)

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

    def update_webpage_image(self, coreImage, t):
        texture = coreImage.texture
        self.ids["WebpageImage"].texture = texture
        self.ids["WebpageImageLarge"].texture = texture

        Logger.debug("WebpageImage: Finished image update in " + str(time.time() - t))

    def on_enter(self, *args):
        Thread(target=self.Miner.start, daemon=True).start()

    # Miner ------------------------------------------------------------------------------------------------------------

    class _Miner(EventDispatcher):
        usrName = StringProperty("")
        pwdInput = StringProperty("")
        stopOnlyWhenStopPressed = BooleanProperty(False)
        mineUntilPoints = NumericProperty(None)
        mineForTime = NumericProperty(None)
        requireAll = BooleanProperty(True)
        midLinePos = NumericProperty(0)
        webpage_image_update_interval = Config.getfloat("Gui", "webpage_image_update_interval")

        do_webpage_image_update = False
        driver = None
        Gui = None

        def start(self):
            self.webpage_image_update_interval = Config.getfloat("Gui", "webpage_image_update_interval")

            self.install_dependants()
            self.setup()
            self.start_webpage_image_updater()
            self.do_webpage_image_update = True
            self.pre_mine()
            self.mine()
            self.do_webpage_image_update = False
            self.post_mine()

        def start_webpage_image_updater(self):
            Thread(target=self.webpage_image_updater, daemon=True).start()

        def webpage_image_updater(self):
            while True:
                if self.do_webpage_image_update:
                    t = time.time()

                    Logger.debug("WebpageImage: Starting image update")

                    data = io.BytesIO(self.driver.get_screenshot_as_png())

                    coreImage = CoreImage(data, ext="png")
                    Clock.schedule_once(lambda _: self.Gui.update_webpage_image(coreImage, t), 0)

                    try:
                        time.sleep(self.webpage_image_update_interval - (time.time() - t))
                    except ValueError:
                        Logger.warning("WebpageImage: Convert took to long, took " + str(time.time() - t) +
                                       " and it should've took " + str(self.webpage_image_update_interval))

                else:
                    time.sleep(self.webpage_image_update_interval)

        def install_dependants(self):
            chromedriver_autoinstaller.install()
            Logger.info("Miner: Chromedriver installed if not already")

        def setup(self):
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
            chrome_options.add_argument("--log-path=" + str(os.path.join(user_data_dir, "chromedriver.log")))
            Logger.info("Miner: Chromedriver setup")

            url = Config.get("Mining", "url")
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.get(url)

            Logger.info("Miner: Loaded " + str(url))

        def pre_mine(self):
            Logger.info("Miner: Started pre mining setup function")

            MemriseElements.get("username_input", self.driver).send_keys(self.usrName)
            MemriseElements.get("password_input", self.driver).send_keys(self.pwdInput)
            MemriseElements.get("login_submit_button", self.driver).click()


            Logger.info("Miner: Finished pre mining setup function")



        def mine(self):
            Logger.info("Miner: Started ghost mining function")

            pass

            Logger.info("Miner: Finished ghost mining function")

        def post_mine(self):
            self.driver.close()
