from kivy.app import App
from kivy.lang import Builder


class MemriseBot(App):
    def build(self):
        return Builder.load_file("resources/kv.kv")

    def start_botting(self, translation):
        print(f"Starting, translation is {translation}")


if __name__ == "__main__":
    memriseBot = MemriseBot()
    memriseBot.run()
