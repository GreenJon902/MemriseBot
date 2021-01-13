from kivy.app import App
from kivy.core.window import Window


Window.size = 950, 500

Window.minimum_width = 950
Window.minimum_height = 500


class MemriseAutoApp(App):
    RequirementsChangeLastSelected = None

    def switch_changed(self, _, state):
        self.root.ids["HomeScreen"].ids["PointsInput"].opacity = 0.5 if state else 1
        self.root.ids["HomeScreen"].ids["TimeInput"].opacity = 0.5 if state else 1
        self.root.ids["HomeScreen"].ids["RequirementsAll"].opacity = 0.5 if state else 1
        self.root.ids["HomeScreen"].ids["RequirementsSingle"].opacity = 0.5 if state else 1

        self.root.ids["HomeScreen"].ids["PointsInput"].disabled = state
        self.root.ids["HomeScreen"].ids["TimeInput"].disabled = state
        self.root.ids["HomeScreen"].ids["RequirementsAll"].disabled = state
        self.root.ids["HomeScreen"].ids["RequirementsSingle"].disabled = state

    def RequirementsChange(self, this):
        other = self.root.ids["HomeScreen"].ids["RequirementsAll"] if this == self.root.ids["HomeScreen"].ids["RequirementsSingle"] else self.root.ids["HomeScreen"].ids["RequirementsSingle"]

        if this.state == "normal" and other.state == "normal":
            this.state = "down"

    def start_mining(self):
        pass
