from tkinter import Tk, Label, Button, Text
import time
import selenium.webdriver


class id:
    def __init__(self):
        self.done = False

    def do(self):
        self.done = True


driver = selenium.webdriver.Chrome(executable_path="./chromedriver")
driver.get("https://www.memrise.com/home/")

while True:
    isDone = id()

    window = Tk()
    Label(window, text="Place the window with memrise on next to this window. Go to the levels menu on the Course and \n" +
                       "then click on a level that has already been complected. Click the Ignore button, click All and \n" +
                       "then unselected one. Once this is done, scroll down to the bottom and click Save.").pack()
    Button(window, text="Next", command=isDone.do).pack()

    while not isDone.done:
        window.update()

    window.destroy()


    # -----------------------------------------------------------------------------------------------
    isDone = id()

    window = Tk()
    Label(window, text="Set the positions of the Review and the levels button by going through once, when you click \n" +
                       "change then you have 5 seconds to get the mouse over the button.").grid(row=0, column=0,
                                                                                                columnspan=3)
    Label(window, text=" ").grid(row=1, column=0, columnspan=3)


    Label(window, text="Translation").grid(row=4, column=0)
    t3 = Text(window, height=1)
    t3.delete(1.0, "end")
    t3.insert(1.0, "Not Set")
    t3.grid(row=4, column=1)

    Label(window, text="Repetitions").grid(row=5, column=0)
    t4 = Text(window, height=1)
    t4.delete(1.0, "end")
    t4.insert(1.0, "10")
    t4.grid(row=5, column=1)

    Button(window, text="Next", command=isDone.do).grid(row=6, column=0, columnspan=3)

    while not isDone.done:
        window.update()

    trans = str(t3.get(1.0, "end-1c"))
    reps = int(str(t4.get(1.0, "end-1c")).split(",")[0])


    window.destroy()



    # -----------------------------------------------------------------------------------------------


    isDone = id()

    window = Tk()
    Label(window, text="Running!").pack()
    progress = Label(window, text="0/" + str(reps))
    progress.pack()
    Button(window, text="Stop", command=isDone.do).pack()

    n = 0

    for element in driver.find_elements_by_tag_name("a"):
        if str(element.text).find("Review"):
            path = element.get_attribute("href")

            break



    while not isDone.done:
        print(n)
        n = n + 1

        progress.configure(text=str(n) + "/" + str(reps))
        window.update()

        try:
            driver.get(path)
            time.sleep(1)
            driver.find_element_by_class_name("typing-type-here").send_keys(trans)
            time.sleep(0.1)
            driver.find_element_by_class_name("next-icon").click()
            time.sleep(0.1)
            driver.find_element_by_class_name("next-icon").click()
            time.sleep(0.1)


        except:
            print("failed")
            time.sleep(0.5)

            try:
                driver.get(path)
                time.sleep(1)
                driver.find_element_by_class_name("typing-type-here").send_keys(trans)
                time.sleep(0.1)
                driver.find_element_by_class_name("next-icon").click()
                time.sleep(0.1)
                driver.find_element_by_class_name("next-icon").click()
                time.sleep(0.1)


            except:
                print("failed")
                time.sleep(0.5)

                try:
                    driver.get(path)
                    time.sleep(1)
                    driver.find_element_by_class_name("typing-type-here").send_keys(trans)
                    time.sleep(0.1)
                    driver.find_element_by_class_name("next-icon").click()
                    time.sleep(0.1)
                    driver.find_element_by_class_name("next-icon").click()
                    time.sleep(0.1)


                except:
                    print("failed")
                    time.sleep(0.5)

                try:
                    driver.get(path)
                    time.sleep(1)
                    driver.find_element_by_class_name("typing-type-here").send_keys(trans)
                    time.sleep(0.1)
                    driver.find_element_by_class_name("next-icon").click()
                    time.sleep(0.1)
                    driver.find_element_by_class_name("next-icon").click()
                    time.sleep(0.1)


                except:
                    print("ooooooooofffffff")
                    time.sleep(0.5)



        if n == reps:
            break

