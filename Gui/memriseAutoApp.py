from kivy.animation import Animation
from kivy.app import App
from kivy.core.window import Window

from Gui.miningScreen import MiningScreen


Window.size = 950, 500

Window.minimum_width = 950
Window.minimum_height = 500


class MemriseAutoApp(App):
    RequirementsChangeLastSelected = None

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
        mining = self.root.get_screen("MiningScreen")
        mining.usrName = home.ids["UsrNameInput"].text
        mining.pwdInput = home.ids["PwdInput"].text
        mining.stopOnlyWhenStopPressed = home.ids["MineUntilOrForSwitch"].active
        mining.mineUntilPoints = None if home.ids["PointsInput"].text == "" else home.ids["PointsInput"].text
        mining.mineForTime = None if home.ids["TimeInput"].text == "" else home.ids["TimeInput"].text
        mining.requireAll = home.ids["RequirementsAll"].state == "down"

        self.root.current = "MiningScreen"
