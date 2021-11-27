import sys
from tkinter import Tk, Label, Button, Text

import chromedriver_autoinstaller
import selenium.webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


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
print("Getting ulr that review button goes too")

path = None
for element in driver.find_elements_by_tag_name("a"):
    if "Review" in element.text:
        path = element.get_attribute("href")
        break

if path is None:
    print("Failed")
    print("Could not get attribute href from element with text \"review\", maybe your on the wrong page, the url should end with \"name of the course/level number/\"!\ne.g.german/4")
    sys.exit()

print("Running")
while not isDone.done:
    try:
        driver.get(path)


        WebDriverWait(driver, 1000).until(
            expected_conditions.presence_of_element_located((By.XPATH,
                                                             "/html/body/div[4]/div[3]/div/div/div[4]/input")))
        driver.find_element_by_xpath("/html/body/div[4]/div[3]/div/div/div[4]/input").send_keys(trans)


        WebDriverWait(driver, 1000).until(
            expected_conditions.presence_of_element_located((By.XPATH,
                                                             "/html/body/div[4]/div[3]/div/div/div[1]/button/span")))
        driver.find_element_by_xpath("/html/body/div[4]/div[3]/div/div/div[1]/button/span").click()


        WebDriverWait(driver, 1000).until(
            expected_conditions.presence_of_element_located((By.XPATH,
                                                             "/html/body/div[5]/div[3]/div/div/div[3]/span[2]")))



    except Exception as e:
        print("failed", e)
