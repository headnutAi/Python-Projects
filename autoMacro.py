import threading
import time
import random
from pynput import keyboard
import pyautogui

# Flag to control auto-clicking
auto_clicking = False
click_thread = None

def auto_click():
    global auto_clicking
    while auto_clicking:
        # Click at the current mouse position
        pyautogui.rightClick()
        # Random interval between 0.5 and 1.0 seconds
        interval = random.uniform(0.5, 1.0)
        time.sleep(interval)

def on_press(key):
    global auto_clicking, click_thread
    try:
        if key == keyboard.Key.f6:
            if not auto_clicking:
                auto_clicking = True
                print("Auto-clicking started.")
                # Start the auto-click thread
                click_thread = threading.Thread(target=auto_click)
                click_thread.start()
        elif key == keyboard.Key.f7:
            if auto_clicking:
                auto_clicking = False
                print("Auto-clicking stopped.")
                if click_thread is not None:
                    click_thread.join()
    except AttributeError:
        pass

# Set up the listener for hotkeys
with keyboard.Listener(on_press=on_press) as listener:
    print("Press F6 to start auto-clicking, F7 to stop.")
    print("Auto-click will click at your current mouse position.")
    listener.join()
