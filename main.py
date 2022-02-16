from PIL import Image
from pystray import MenuItem as Item, Menu
import pystray
from threading import Thread
import subprocess
from time import time
from time import sleep
import tkinter as tk


paused = False
title = "Pinger"
image = Image.open("Icon_y.ico")
hostname = "8.8.8.8"
IconState = 'y'
interval = 1
isRunning = True


def pause(ic):
    global paused
    paused = not paused
    if paused:
        img = Image.open('Icon_b.ico')
        text = "Resume"
    else:
        IconState = 'y'
        img = Image.open('Icon_y.ico')
        text = "Pause"
    ic.icon = img
    menu = Menu(
        Item(text, pause, default=True),
        Item('Settings', showSettings),
        Item('Quit', quitProgram)
    )


def quitProgram(ic, item):
    ic.stop()


def showSerttingsWindow():
    fg = "#d1d1d1"
    bg = "#363636"
    font = ("Roboto", 10)
    padding = {'padx': 5, 'pady': 5}

    window = tk.Tk()
    window.geometry("300x90")
    window.title = "Pinger"
    window.iconbitmap("Icon_g.ico")

    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)
    window.columnconfigure(2, weight=1)

    svHost = tk.StringVar(value=hostname)

    lbl_host = tk.Label(text="Host:", font=font)
    lbl_host.grid(column=0, row=0, **padding)

    ent_host = tk.Entry(font=font, textvariable=svHost)
    ent_host.grid(column=1, row=0, **padding)

    btn_save = tk.Button(text="Save", font=font, relief="solid", borderwidth=1, padx=15)
    btn_save.grid(column=2, row=0, **padding)

    lbl_status = tk.Label(font=font)
    lbl_status.grid(column=0, row=1, columnspan=3, **padding)

    def updateHostname(arg=None):
        global hostname
        hostname = svHost.get()
        lbl_status.config(text="Host changed to " + hostname)

    ent_host.bind("<Return>", updateHostname)
    btn_save.config(command=updateHostname)

    window.mainloop()



def showSettings():
    settingsWindowThread = Thread(target=showSerttingsWindow)
    settingsWindowThread.start()


menu = Menu(
    Item('Pause', pause, default=True),
    Item('Settings', showSettings),
    Item('Quit', quitProgram)
)
icon = pystray.Icon("name", image, "Pinger", menu)


# returns 0 if successful, otherwise 1
def ping(hostname):
    p = subprocess.Popen('ping -n 1 -w 500 ' + hostname, shell=False)
    p.wait()
    result = p.poll()
    p.kill()
    return result


# single update
def updateIcon(hostname):
    global IconState
    check = ping(hostname)

    if check == 0:
        icon.icon = Image.open("Icon_g.ico")
        IconState = 'g'
    elif check == 1:
        if IconState == 'g':
            IconState = 'y'
            icon.icon = Image.open("Icon_y.ico")
        elif IconState == 'y':
            IconState = 'r'
            icon.icon = Image.open("Icon_r.ico")


# tries to ping every second, twice in case the package was lost
def updateLoop():
    while isRunning:
        start = time()
        if paused is False:
            updateIcon(hostname)
        sleep(abs(round(start) + interval - start))


def main():
    updateThread = Thread(target=updateLoop)
    updateThread.start()

    icon.run()
    global isRunning
    isRunning = False



main()
