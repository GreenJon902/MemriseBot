from selenium.webdriver.common.by import By


class _MemriseElements:
    elements = {}

    def setup(self, config):
        elements = {}

        for key in config.options("Memrise_Element"):
            value = config.get("Memrise_Element", key)
            elementFinderType = key.split("-")[1]
            elements[key.split("-")[0]] = By.__dict__[elementFinderType.upper()], value

        self.elements.update(elements)

    def get(self, name, driver):
        print(name, self.elements)
        return driver.find_element(*self.elements[name])


MemriseElements = _MemriseElements()
