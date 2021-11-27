from kivy.app import App
from kivy.lang import Builder


class MemriseBot(App):
    def build(self):
        return Builder.load_file("resources/kv.kv")


if __name__ == "__main__":
    memriseBot = MemriseBot()
    memriseBot.run()
