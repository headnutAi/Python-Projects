import pyautogui
import time

print("Move mouse to TOP-LEFT of container in 5 seconds")
time.sleep(5)
print(pyautogui.position())

print("Move mouse to BOTTOM-RIGHT of container in 5 seconds")
time.sleep(5)
print(pyautogui.position())
