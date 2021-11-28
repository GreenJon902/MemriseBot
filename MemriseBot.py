from kivy import Logger
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from bot import Bot


class MemriseBot(App):
    bot: Bot = None

    def build(self):
        self.bot = Bot()
        return Builder.load_file("resources/kv.kv")

    # noinspection PyMethodMayBeStatic
    def start_botting(self, translation):
        Logger.info(f"Starting, translation is {translation}")
        self.bot.start_bot(translation)
        popup = Popup(title="Bot running", auto_dismiss=False, on_dismiss=lambda *args: self.bot.end_bot())
        popup.content = Button(text="Stop",
                               on_release=lambda *args: popup.dismiss())
        popup.open()

    def stop_botting(self, *args):
        self.bot.end_bot()

    def stop(self, *args):
        self.bot.end()
        App.stop(self, *args)


if __name__ == "__main__":
    memriseBot = MemriseBot()
    memriseBot.run()
