# Pulled from GreenJon902/md5-unhasher

from kivy.logger import Logger
from kivy.properties import OptionProperty, StringProperty, ObjectProperty, NumericProperty, ListProperty, DictProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.slider import Slider
from kivy.uix.switch import Switch
from kivy.uix.textinput import TextInput
from misc.config import Config
from misc.functions import emptyFunction


class ConfigItem(BoxLayout):
    # General options
    type = OptionProperty("string", options=["numericSlider", "string", "bool", "option", "title"])
    title = StringProperty("Title")
    description = StringProperty("Description")
    section = StringProperty("")
    option = StringProperty("")

    # Numeric slider options
    min = NumericProperty(None)
    max = NumericProperty(None)
    sliderMin = NumericProperty(None)
    sliderMax = NumericProperty(None)

    # Option options
    options = ListProperty([])
    extra_info = DictProperty({})


    _editorHolder = ObjectProperty()
    _editorWidget = ObjectProperty()
    _editorWidget2 = ObjectProperty(None)

    def on_kv_post(self, base_widget):
        self._editorHolder = self.ids["EditorHolder"]

        self.bind(type=self.update,
                  title=self.update,
                  description=self.update,
                  min=self.update,
                  max=self.update)

        self.update()

    def text_box_int_validator(self, *args):
        numb = int(self._editorWidget2.text)

        if self.min is not None and numb < self.min:
            numb = self.min

        elif self.max is not None and numb < self.max:
            numb = self.max

        self._editorWidget2.text = str(numb)
        self.value_changed(None, numb)

    def update(self, *args):
        self.ids["Title"].text = self.title
        self.ids["Description"].text = self.description

        self._editorHolder.clear_widgets()

        if self.type == "numericSlider":
            if self.sliderMin is None or self.sliderMax is None:
                raise ValueError("'sliderMin' and / or 'sliderMax' cannot be 'None' if type is numericSlider")


            self._editorWidget = Slider(min=self.sliderMin, max=self.sliderMax,
                                        value=Config.getint(self.section, self.option), step=1)
            self._editorWidget.bind(value=self.value_changed)

            self._editorWidget2 = TextInput(multiline=False, font_size=self._editorHolder.height / 2,
                                            text=Config.get(self.section, self.option), input_filter="int")
            self._editorWidget2.bind(on_text_validate=self.text_box_int_validator)
            self._editorWidget2.bind(focus=self.text_box_int_validator)


        elif self.type == "bool":
            self._editorWidget = Switch(active=Config.getboolean(self.section, self.option))
            self._editorWidget.bind(active=self.value_changed)


        elif self.type == "string":
            self._editorWidget = TextInput(multiline=False, font_size=self._editorHolder.height / 2,
                                           text=Config.get(self.section, self.option))
            self._editorWidget.bind(on_text_validate=lambda *args: self.value_changed(None, self._editorWidget.text))
            self._editorWidget.bind(focus=lambda *args: self.value_changed(None, self._editorWidget.text))

        elif self.type == "option":
            self._editorWidget = Button(text=Config.get(self.section, self.option))

            dropDown = DropDown()

            for option in self.options:
                text = str(option)
                try:
                    text = text + " - " + str(self.extra_info[option])
                except KeyError:
                    pass

                btn = Button(text=text, size_hint_y=None, height=self.height)
                btn.tag = str(option)
                btn.bind(on_release=lambda _btn: dropDown.select(_btn.tag))
                dropDown.add_widget(btn)

            self._editorWidget.bind(on_release=dropDown.open)
            self._editorWidget.bind(on_release=lambda *args: emptyFunction(dropDown.children))
            dropDown.bind(on_select=lambda instance, x: setattr(self._editorWidget, 'text', x))
            dropDown.bind(on_select=self.value_changed)


        if self._editorWidget2 is not None:
            self._editorHolder.add_widget(self._editorWidget2)

        if self.type != "title":
            self._editorHolder.add_widget(self._editorWidget)

    def value_changed(self, _, value):
        if self._editorWidget2 is not None:
            self._editorWidget2.text = str(value)

            self._editorWidget.value = int(value)

        Logger.info("Config: " + self.section + self.option + " set to " + str(value))
        Config.set(self.section, self.option, value)
        Config.write()
        Logger.info("Config: Saved config")
