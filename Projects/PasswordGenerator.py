import random
import string
import pyautogui
import tkinter as tk
from tkinter import messagebox

def generatepassword():

    length = int(length_entry.get())

    if length <= 0:
        messagebox.showerror("Error", "Please enter a positive integer")
        return

    mixed_list = (
        list(range(1, 10)) +
        list(string.ascii_lowercase) +
        list(string.ascii_uppercase) +
        list(string.punctuation)
    )



    password = []

    for i in range(length):
        password.append(random.choice(mixed_list))

    password = "".join(map(str, password))


    x,y = pyautogui.position()

    x = str(x)
    y = str(y)


    result = x + password + y + 'D' + 'w' + '!'

    resultList = list(map(str, result))
    random.shuffle(resultList)
    FinishedPassword = "".join(resultList)

    print(FinishedPassword)

    output_label.config(text=FinishedPassword)

def copy_password():
    pwd = output_label.cget("text")
    if pwd:
        root.clipboard_clear()
        root.clipboard_append(pwd)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showwarning("Warning", "No password to copy!")



root = tk.Tk()
root.title("Password Generator")
root.geometry("500x250")

instruction_label = tk.Label(root, text="Enter the desired password length:")
instruction_label.pack(pady=10)

length_entry = tk.Entry(root)
length_entry.pack(pady=5)

generate_button = tk.Button(root, text="Generate Password", command=generatepassword)
generate_button.pack(pady=10)

output_label = tk.Label(root, text="", wraplength=450, font=("Arial", 12))
output_label.pack(pady=20)

copy_button = tk.Button(root, text="Copy Password", command=copy_password)
copy_button.pack(pady=10)

root.mainloop()