from kivy import Logger
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup

from bot import Bot


class MemriseBot(App):
    bot: Bot = None

    def build(self):
        self.bot = Bot(self.bot_sent_info)
        return Builder.load_file("resources/kv.kv")

    # noinspection PyMethodMayBeStatic
    def start_botting(self, translation):
        Logger.info(f"Starting, translation is {translation}")
        self.bot.start_bot(translation)
        popup = Popup()
        popup.open()

    def bot_sent_info(self, *args):
        pass

    def stop(self, *args):
        self.bot.end()
        App.stop(self, *args)


if __name__ == "__main__":
    memriseBot = MemriseBot()
    memriseBot.run()
