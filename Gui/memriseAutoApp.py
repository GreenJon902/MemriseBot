from kivy import Logger
from kivy.animation import Animation
from kivy.app import App
from kivy.core.window import Window

from Gui.miningScreen import MiningScreen
from misc import encode, decode
from misc.config import Config

Window.size = 950, 500

Window.minimum_width = 950
Window.minimum_height = 500


class MemriseAutoApp(App):
    RequirementsChangeLastSelected = None

    def mabyDoPasswordAndLogins(self, screen):
        if Config.getboolean("Misc", "saveLogins"):
            screen.ids["UsrNameInput"].text = Config.get("Misc", "username")
            screen.ids["PwdInput"].text = decode(str(Config.get("Misc", "password")), "JonIsGreen")

            Logger.info("Logins: Loaded")

    def switch_changed(self, _, state):
        a = Animation(opacity=(0.2 if state else 1), duration=0.5)

        a.start(self.root.ids["HomeScreen"].ids["PointsInput"])
        a.start(self.root.ids["HomeScreen"].ids["TimeInput"])
        a.start(self.root.ids["HomeScreen"].ids["RequirementsAll"])
        a.start(self.root.ids["HomeScreen"].ids["RequirementsSingle"])
        a.start(self.root.ids["HomeScreen"].ids["MineUntilLabel"])
        a.start(self.root.ids["HomeScreen"].ids["MineForLabel"])

        self.root.ids["HomeScreen"].ids["PointsInput"].disabled = state
        self.root.ids["HomeScreen"].ids["TimeInput"].disabled = state
        self.root.ids["HomeScreen"].ids["RequirementsAll"].disabled = state
        self.root.ids["HomeScreen"].ids["RequirementsSingle"].disabled = state

    def RequirementsChange(self, this):
        other = self.root.ids["HomeScreen"].ids["RequirementsAll"] if this == self.root.ids["HomeScreen"].ids["RequirementsSingle"] else self.root.ids["HomeScreen"].ids["RequirementsSingle"]

        if this.state == "normal" and other.state == "normal":
            this.state = "down"

    def start_mining(self):
        home = self.root.get_screen("HomeScreen")

        if Config.getboolean("Misc", "saveLogins"):
            Config.set("Misc", "username", home.ids["UsrNameInput"].text)
            Config.set("Misc", "password", encode(str(home.ids["PwdInput"].text), "JonIsGreen"))
            Config.write()

            Logger.info("Logins: Saved")


        MinerSettings = self.root.get_screen("MiningScreen").MinerSettings
        MinerSettings["usrName"] = home.ids["UsrNameInput"].text
        MinerSettings["pwdInput"] = home.ids["PwdInput"].text
        MinerSettings["stopOnlyWhenStopPressed"] = home.ids["MineUntilOrForSwitch"].active
        MinerSettings["mineUntilPoints"] = None if home.ids["PointsInput"].text == "" else home.ids["PointsInput"].text
        MinerSettings["mineForTime"] = None if home.ids["TimeInput"].text == "" else home.ids["TimeInput"].text
        MinerSettings["requireAll"] = home.ids["RequirementsAll"].state == "down"

        self.root.current = "MiningScreen"

    def on_stop(self):
        Config.write()

        mining = self.root.get_screen("MiningScreen")
        try:
            mining.driver.quit()
        except AttributeError:
            pass
