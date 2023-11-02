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
#This is what I wrote we don't have to use it but it should work

# def increment_rep():
#     global rep_counter
#     rep_counter += 1
#     rep_label.config(text=f'Reps: {rep_counter}')

# def reset_rep():
#     global rep_counter
#     rep_counter = 0
#     rep_label.config(text='Reps: 0')

# def update_weight():
#     global weightGUI
#     weigtGUI = weight_entry.get()
#     weight_label.config(text=f'Weight: {weightGUI} lbs')

# def update_arm():
#     global armGUI
#     armGUI = arm_var.get()

# rep_count = 0
# weightGUI = 0
# armGUI = "Left"

# # Create the main window
# root = tk.Tk()
# root.title("Curl Rep Counter")

# # Weight input
# weight_label = tk.Label(root, text="Weight: 0 lbs")
# weight_label.pack()
# weight_entry = tk.Entry(root)
# weight_entry.pack()
# weight_button = tk.Button(root, text="Set Weight", command=update_weight)
# weight_button.pack()

# # Arm selection
# arm_label = tk.Label(root, text="Arm:")
# arm_label.pack()
# arm_var = tk.StringVar(value="Left")
# arm_left_radio = tk.Radiobutton(root, text="Left", variable=arm_var, value="Left", command=update_arm)
# arm_right_radio = tk.Radiobutton(root, text="Right", variable=arm_var, value="Right", command=update_arm)
# arm_left_radio.pack()
# arm_right_radio.pack()

# # Rep counter
# rep_label = tk.Label(root, text="Reps: 0")
# rep_label.pack()
# increment_button = tk.Button(root, text="Increment Rep", command=increment_rep)
# increment_button.pack()
# reset_button = tk.Button(root, text="Reset", command=reset_rep)
# reset_button.pack()

# root.mainloop()
