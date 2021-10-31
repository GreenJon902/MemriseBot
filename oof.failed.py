import sys
import time
from tkinter import Tk, Label, Button, Text, DISABLED, NORMAL
import pyautogui


def setPos(tBox):
    time.sleep(5)

    pos = pyautogui.position()

    tBox.Config(state=NORMAL)
    tBox.delete(1.0, "end")
    tBox.insert(1.0, str(pos[0]) + ", " + str(pos[1]))
    tBox.Config(state=DISABLED)


class id:
    def __init__(self):
        self.done = False

    def do(self):
        self.done = True


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

Label(window, text="Review button position").grid(row=2, column=0)

t = Text(window, height=1)
t.delete(1.0, "end")
t.insert(1.0, "Not Set")
t.config(state=DISABLED)
t.grid(row=2, column=1)

Button(window, text="Change", command=lambda: setPos(t)).grid(row=2, column=2)

Label(window, text="Levels button position").grid(row=3, column=0)

t2 = Text(window, height=1)
t2.delete(1.0, "end")
t2.insert(1.0, "Not Set")
t2.config(state=DISABLED)
t2.grid(row=3, column=1)

Button(window, text="Change", command=lambda: setPos(t2)).grid(row=3, column=2)

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

revPos = (-2723, 491)  # int(str(t.get(1.0, "end-1c")).split(",")[0]), int(str(t.get(1.0, "end-1c")).split(",")[1])
levelsPos = (-2706, 435)  # int(str(t2.get(1.0, "end-1c")).split(",")[0]), int(str(t2.get(1.0, "end-1c")).split(",")[1])
trans = "gibt es"  # str(t3.get(1.0, "end-1c"))
reps = int(str(t4.get(1.0, "end-1c")).split(",")[0])

window.destroy()

# -----------------------------------------------------------------------------------------------


isDone = id()

window = Tk()
Label(window, text="Put memrise onto the level that you chose screen" +
                   "but make sure not to move the window (Levels > the one you chose) and then dis").pack()
Button(window, text="Start", command=isDone.do).pack()

while not isDone.done:
    window.update()

window.destroy()

# -----------------------------------------------------------------------------------------------

print(revPos)
print(levelsPos)
print(trans)
print(reps)
print()

isDone = id()

window = Tk()
Label(window, text="Running!").pack()
progress = Label(window, text="0/" + str(reps))
progress.pack()
Button(window, text="Stop", command=isDone.do).pack()

n = 0

while not isDone.done:
    n = n + 1

    progress.configure(text=str(n) + "/" + str(reps))
    window.update()

    time.sleep(2)
    print("Click Review")
    pyautogui.moveTo(revPos[0], revPos[1])
    pyautogui.doubleClick(interval=0.1)
    time.sleep(2)
    print("Typing", trans)
    pyautogui.write(trans)
    time.sleep(2)
    print("Click Enter")
    pyautogui.press("enter")
    time.sleep(2)
    print("Click Enter")
    pyautogui.press("enter")
    time.sleep(2)
    print("Click Enter")
    pyautogui.press("enter")
    time.sleep(2)
    print("Click Levels")
    pyautogui.moveTo(levelsPos[0], levelsPos[1])
    pyautogui.click()

    if n == reps:
        break

window.destroy()
