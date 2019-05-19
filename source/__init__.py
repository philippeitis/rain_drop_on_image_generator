import time

import PIL.ImageGrab
import pyautogui
from PIL import ImageFilter
from pynput import keyboard


def on_press(key):
    import os
    try:
        if key.char == 'q':
            os._exit(1)
    except AttributeError:
        someRandomThing = 0
        #print('special key {0} pressed'.format(
        #   key))


def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False


def move_mouse_pointer(x, y):
    pyautogui.moveTo(x,y, duration=0.001)


# Collect events until released
listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
listener.start()


def get_images():
    import os
    # May need to adjust for mac
    filenames = os.listdir("../input")
    return filenames

def generate_images():
    filenames = get_images()
    for filename in filenames:
        # May need to adjust for mac
        set_up_folder("../input/" + filename)
        launch_chrome()
        # May need to adjust for mac
        take_screenshots("../output/" + filename)


def set_up_folder(filename):
    from PIL import Image
    im = Image.open(filename)
    # Try to pass in 1920 x 1280 images or factors thereof
    im.save("../website/demo.jpg", "JPEG")


def take_screenshots(filename):
    time.sleep(10)
    im = PIL.ImageGrab.grab()
    im.save(filename[:-4] + "1" + ".jpg", "JPEG")
    time.sleep(1)
    im = PIL.ImageGrab.grab()
    im.save(filename[:-4] + "2" + ".jpg", "JPEG")
    time.sleep(1)
    im = PIL.ImageGrab.grab()
    im.save(filename[:-4] + "3" + ".jpg", "JPEG")
    time.sleep(1)
    im = PIL.ImageGrab.grab()
    im.save(filename[:-4] + "4" + ".jpg", "JPEG")
    time.sleep(1)
    im = PIL.ImageGrab.grab()
    im.save(filename[:-4] + "5" + ".jpg", "JPEG")


def launch_chrome():
    import os
    import webbrowser
    # May need to adjust path for Mac
    webbrowser.open('file://' + os.path.realpath("../website/home.html"))

generate_images()