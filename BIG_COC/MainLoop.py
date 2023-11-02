# Jacob Auman
# 11-1-23
###########################################
# MAIN LOOP for the Custom Tkinter Display
###########################################
# Import statements
import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
from threading import Thread
import json

# Initialize Variables
maxWeight = 1000
testIMG = 'CoC_Curls\\Test_Videos\\test.png'
webcam_running = False
cap = None  # Global variable to hold the capture object

# Functions
#############################################
# The function to update the image in the GUI
from PIL import Image, ImageTk

def update_image(label, cap, scale_factor=1.5):
    global webcam_running
    if webcam_running:
        ret, frame = cap.read()
        if ret:
            cv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(cv_image)
            # Scale up the image
            new_size = (int(pil_image.size[0] * scale_factor), int(pil_image.size[1] * scale_factor))
            pil_image = pil_image.resize(new_size)
            imgtk = ImageTk.PhotoImage(image=pil_image)
            label.configure(image=imgtk)
            label.image = imgtk
            label.after(10, lambda: update_image(label, cap))
        else:
            print("Failed to capture frame")
            webcam_running = False
            cap.release()

# Function to start the webcam capture
def start_webcam(label):
    global webcam_running, cap
    if not webcam_running:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise IOError("Cannot open webcam")
        webcam_running = True
        update_image(label, cap)

# Function to stop the webcam capture
def stop_webcam():
    global webcam_running, cap
    if webcam_running:
        webcam_running = False
        cap.release()

# Modify the buttonPress2 function to start the webcam stream
def buttonPress2():
    print("Button 2 Pressed")
    start_webcam(image)

def buttonPress1():
    # Button reads in the weight int value and arm string value
    weight = int(weightInput.get())
    arm = switch_var.get()
    print(f"Values saved:{weight} {arm}")

    # Read the data.json file for the weight and reps
    with open('CoC_Curls\BIG_COC\data.json', 'r') as f:
        data = json.load(f)
    # Access specific values using their keys
    data['weight'] = weight
    data['arm'] = arm
    # Write the values to a json file
    with open('CoC_Curls\BIG_COC\data.json', 'w') as f:
        json.dump({"weight":weight, "arm":arm}, f)

def switch_event():
    print("switch toggled, current value:", switch_var.get())


# Setup Custom Tkinter Window
#############################################
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
root = ctk.CTk()
# Window Title
root.title("CoC Curls")
# Define the window size
root.geometry("700x800")
# Define where the window opens
root.geometry("+100+100")


# Create and Define GUI Elements
#############################################
inputFrame = ctk.CTkFrame(master=root)
# User input box for weight used
weightInput = ctk.CTkEntry(master=inputFrame, placeholder_text="Enter Weight LBS per hand")
# Switch for left or right arm
switch_var = ctk.StringVar(value="right")
switch = ctk.CTkSwitch(master=inputFrame, text="Toggle For Left Hand", command=switch_event, variable=switch_var, onvalue="left", offvalue="right")


# BUTTTONS
inputButton = ctk.CTkButton(master=inputFrame, text="Submit Values", command = buttonPress1)
recordButton = ctk.CTkButton(master=inputFrame, text="Start Recording", fg_color='green', hover_color='dark green', command = buttonPress2)
stopButton = ctk.CTkButton(master=inputFrame, text="Stop Recording", fg_color='red', hover_color='dark red',command=stop_webcam)

# FIMAGE
displayFrame = ctk.CTkFrame(master=root)
testIMG = Image.open(testIMG)
# Set the width and height
width, height = 200 , 300
# Create a CTkImage object with the specified size
imageTest = ctk.CTkImage(light_image=testIMG, size=(width, height))
# Create a label and add the image to it
image = ctk.CTkLabel(master=displayFrame, text=None ,image=imageTest)
# Keep a reference to the image
image.image = imageTest


outputFrame = ctk.CTkFrame(master=root)
resultLabel = ctk.CTkLabel(master=outputFrame, text=f"You can curl a max of {maxWeight} lbs", font=("Arial", 30 , "bold"))
# Create the Stop Recording button




# Pack to Display GUI Elements
#############################################
inputFrame.pack(pady=20, padx=60, fill="both", expand=True)
weightInput.pack(pady=5,padx=140, fill="both")
switch.pack(pady=5)
inputButton.pack(pady=5)
recordButton.pack()
stopButton.pack(pady=5)

displayFrame.pack(pady=20, padx=60, fill="both", expand=True)
image.pack(pady=20)

outputFrame.pack(pady=20, padx=60, fill="both", expand=True)
resultLabel.pack(pady=30)



root.mainloop()