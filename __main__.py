from tkinter import Tk, Label, Button, Text
import time
import selenium.webdriver
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options


class id:
    def __init__(self):
        self.done = False

    def do(self):
        self.done = True

chromedriver_autoinstaller.install()

options = Options()
options.set_capability("unhandledPromptBehavior", "dismiss")

driver = selenium.webdriver.Chrome(options=options)
driver.get("https://www.memrise.com/home/")


isDone = id()

window = Tk()
Label(window,
      text="Place the window with memrise on next to this window. Go to the levels menu on the Course and \n" +
           "then click on a level that has already been complected. Click the Ignore button, click All and \n" +
           "then unselected one. Once this is done, scroll down to the bottom and click Save.").pack()
Button(window, text="Next", command=isDone.do).pack(),

while not isDone.done:
    window.update()

window.destroy()

# -----------------------------------------------------------------------------------------------
isDone = id()

window = Tk()
Label(window, text="Translation").grid(row=0, column=0)
t3 = Text(window, height=1)
t3.delete(1.0, "end")
t3.insert(1.0, "Not Set")
t3.grid(row=0, column=1)

Button(window, text="Next", command=isDone.do).grid(row=1, column=0, columnspan=2)

while not isDone.done:
    window.update()

trans = str(t3.get(1.0, "end-1c"))

window.destroy()

# -----------------------------------------------------------------------------------------------

isDone = id()

window = Tk()
Label(window, text="Running!").pack()
Button(window, text="Stop", command=isDone.do).pack()


for element in driver.find_elements_by_tag_name("a"):
    if "Review" in element.text:
        print(element.text)
        path = element.get_attribute("href")

        break



while not isDone.done:

    window.update()

    try:
        driver.get(path)
        #time.sleep(1)
        driver.find_element_by_class_name("typing-type-here").send_keys(trans)
        #time.sleep(0.1)
        driver.find_element_by_class_name("next-icon").click()
        print("Worked")


    except Exception as e:
        print("failed", e)
