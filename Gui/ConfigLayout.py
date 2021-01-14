# Pulled from GreenJon902/md5-unhasher

from kivy.animation import Animation
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.uix.boxlayout import BoxLayout


class ConfigLayout(BoxLayout):
    def add_widget(self, widget, index=0, canvas=None):
        super(ConfigLayout, self).add_widget(widget, index, canvas)
        widget.opacity = 0

    def on_enter(self):

        for n, child in enumerate(reversed(self.children)):
            child.opacity = 0

            a = Animation(duration=0.1*n)
            a += Animation(opacity=1, duration=1)
            a.bind(on_progress=self.draw_bg)
            a.start(child)

        self.bind(pos=self.draw_bg, size=self.draw_bg)

    def draw_bg(self, *args):
        n = 0
        colors = (0.1, 0.1, 0.1), (0.15, 0.15, 0.15)
        title_color = (0.3, 0.3, 0.3)

        with self.canvas.before:
            self.canvas.before.clear()

            for child in self.children:
                if child.__class__.__name__ != "Widget":

                    if child.type == "title":
                        Color(rgb=title_color, a=child.opacity)
                    else:
                        Color(rgb=colors[n], a=child.opacity)
                    Rectangle(pos=child.pos, size=(Window.width, child.height))

                n = (n + 1) % 2