import tkinter as tk
import capture_video as cv
import os
import subprocess

window = tk.Tk()

label = tk.Label(text="Name")
entry = tk.Entry()


def run_repcounter():
   subprocess.run(['python', 'rep_counter.py'])


button = tk.Button(
    text="Record",
    width=10,
    height=5,
    command=cv.record_video
)

button2 = tk.Button(
    text="Analyze",
    width=10,
    height=5,
    command=run_repcounter
)

label.pack()
entry.pack()
button.pack()
button2.pack()


window.mainloop()
