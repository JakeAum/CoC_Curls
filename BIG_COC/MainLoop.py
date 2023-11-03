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
from ultralytics import YOLO
import json
import numpy as np

# Initialize Variables
#############################################
testIMG = 'CoC_Curls\\Test_Videos\\test.png'
webcam_running = False
cap = None  # Global variable to hold the capture object
frame_counter = 0
fps = 2
rep_counter = 0
keypoints_dict = {}
swingState = "down" # Default state is down
arm="right" # Default arm is right

# Load Model 
#############################################
pose_model = YOLO("yolov8s-pose.pt")

keypoint_names = ["nose","left_eye","right_eye","left_ear","right_ear","left_shoulder","right_shoulder","left_elbow","right_elbow","left_wrist","right_wrist","left_hip","right_hip", "left_knee", "right_knee", "left_ankle", "right_ankle"]

# Functions
#############################################
# The function to update the image in the GUI

# Function to start the webcam capture
def start_webcam(label):
    global webcam_running, cap
    if not webcam_running:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise IOError("Cannot open webcam")
        webcam_running = True
        update_image(label, cap)

#############################################
# Image Processing Functions
def update_image(label, cap, scale_factor=1.5):
    global webcam_running, rep_counter, swingState, arm
    if webcam_running:
        success, frame = cap.read()
        if success:
            # Get Arm Angle and Count Reps
            wrist, elbow, shoulder = getJointCoords(frame, pose_model, arm)
            if wrist.any() and elbow.any() and shoulder.any():
                angle = getArmAngle(wrist, elbow, shoulder)
                rep_counter, swingState = countReps(angle, swingState, rep_counter)
                writeRepCount(rep_counter)
                # Display
                angleA, angleB = getAngleRelative(wrist, elbow, shoulder)
                frame = imageOverlay(frame, wrist, elbow, shoulder, angleA, angleB, angle)

                # Convert the image to PIL format...For GUI Display
                cv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(cv_image)
                # Scale up the image
                new_size = (int(pil_image.size[0] * scale_factor), int(pil_image.size[1] * scale_factor))
                pil_image = pil_image.resize(new_size)
                imgtk = ImageTk.PhotoImage(image=pil_image)
                label.configure(image=imgtk)
                label.image = imgtk
                label.after(10, lambda: update_image(label, cap))
                return rep_counter, swingState
            
            else:   
                # Convert the image to PIL format...For GUI Display
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

def getJointCoords(frame, pose_model, whichSideArm): #Complete
    # COMPLETE
    # Pose detection
    pose_results = pose_model(frame, verbose=False, conf=0.7)
    # Analyze the pose results
    for person in pose_results:
        keypoints = person.keypoints.data[0]
        for keypoint, name in zip(keypoints, keypoint_names):
            x, y, probability = keypoint
            keypoints_dict[name] = {"x": x.item(), "y": y.item(), "probability": probability.item()}
    
    if whichSideArm == "left" or whichSideArm == "right":
        wrist = np.array([keypoints_dict[f"{whichSideArm}_wrist"]['x'], keypoints_dict[f"{whichSideArm}_wrist"]['y']])
        elbow = np.array([keypoints_dict[f"{whichSideArm}_elbow"]['x'], keypoints_dict[f"{whichSideArm}_elbow"]['y']])
        shoulder = np.array([keypoints_dict[f"{whichSideArm}_shoulder"]['x'], keypoints_dict[f"{whichSideArm}_shoulder"]['y']])
        return wrist, elbow, shoulder
    else:
        raise ValueError("Invalid arm side! (left or right)")

def getArmAngle(wrist, elbow, shoulder): # Complete
    # Use the X, Y coordinates to calculate the angle at the elbow
    # Create vectors AB and BC
    AB = np.array([wrist[0]-elbow[0], wrist[1]-elbow[1]])
    BC = np.array([shoulder[0] - elbow[0], shoulder[1] - elbow[1]])
    # Compute the dot product and the magnitudes of AB and BC
    dot_product = np.dot(AB, BC)
    magnitude_AB = np.linalg.norm(AB)
    magnitude_BC = np.linalg.norm(BC)   
    # Calculate the cosine of the angle
    cos_angle = dot_product / (magnitude_AB * magnitude_BC)
    # Make sure the value of cosine is in the domain of arccos function
    cos_angle = np.clip(cos_angle, -1.0, 1.0)
    # Calculate the angle in radians and then convert it to degrees
    angle = np.arccos(cos_angle)
    angle_degrees = np.degrees(angle)
    angle_output = int(angle_degrees)
    return angle_output

def countReps(angle, swingState, rep_counter): #complete
    # State Based Rep Counter
    if angle > 90 and swingState == "up":
        swingState = "down"
    if angle < 90 and swingState == "down":
        rep_counter += 1
        swingState = "up"
    return rep_counter, swingState

def getAngleRelative(wrist, elbow, shoulder): #Complete
    # This Function is only really needed for graphing the Joint angle with OpenCV
    # Converts the single angle into two relative angle measured form +X axis counter clockwise
    # Create vectors AB and BC
    AB = np.array([wrist[0]-elbow[0], wrist[1]-elbow[1]])
    BC = np.array([shoulder[0] - elbow[0], shoulder[1] - elbow[1]])

    # Calculate the angle between AB and the positive x-axis
    angle_AB = np.arctan2(AB[1], AB[0]) * 180 / np.pi

    # Calculate the angle between BC and the positive x-axis
    angle_BC = np.arctan2(BC[1], BC[0]) * 180 / np.pi

    return angle_AB, angle_BC

def imageOverlay(frame, wrist, elbow, shoulder, angleA, angleB, angle): #Complete
    #point of the elbow
    elbow_x, elbow_y = elbow[0], elbow[1]
    #point of the wrist
    wrist_x, wrist_y = wrist[0], wrist[1]
    #point of the shoulder
    shoulder_x, shoulder_y = shoulder[0], shoulder[1]
    # cast all coordinates to int
    elbow_x, elbow_y = int(elbow_x), int(elbow_y)
    wrist_x, wrist_y = int(wrist_x), int(wrist_y)
    shoulder_x, shoulder_y = int(shoulder_x), int(shoulder_y)

    
    # Draw the lines between the points
    cv2.line(frame, (elbow_x, elbow_y), (wrist_x, wrist_y), (0, 0, 0), 3)
    cv2.line(frame, (shoulder_x,shoulder_y), (elbow_x, elbow_y), (0, 0, 0), 3)
    # Draw dots at each point
    cv2.circle(frame, (elbow_x, elbow_y), 5, (0,255, 0 ), -3)
    cv2.circle(frame, (wrist_x, wrist_y), 5, (0,255, 0 ), -3)
    cv2.circle(frame, (shoulder_x, shoulder_y), 5, (0,255, 0), -3)
    # Color for the angle
    if angle < 90:
        color = (0, 255, 0)
    elif angle > 90:
        color = (0, 0, 255)
    # Draw the angle of the crook of the arm
    cv2.ellipse(frame,((elbow_x), (elbow_y)), (35, 35), 0, angleA, angleB, color, -1)
    #overlay the angle of the arm at the elbow
    cv2.putText(frame, str(rep_counter), (int(elbow_x), int(elbow_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2, cv2.LINE_AA)
    return frame
    

def writeRepCount(rep_counter):  #Complete
    # Read the data.json file for the weight and reps
    with open('CoC_Curls\BIG_COC\data.json', 'r') as f:
        data = json.load(f)
    # Access specific values using their keys
    data['reps'] = rep_counter
    # Write the values to a json file
    with open('CoC_Curls\BIG_COC\data.json', 'w') as f:
        json.dump({"reps":rep_counter}, f)

def maxCurl_brzycki(): #Complete
    # Read the data.json file for the weight and reps
    with open('CoC_Curls\BIG_COC\data.json', 'r') as f:
        data = json.load(f)
    # Access specific values using their keys
    weight = data['weight']
    reps = data['reps']
    # Calculate Max Curl using Brzycki Formula
    maxCurl = int(weight * (36 / (37 - reps)))
    return maxCurl

def displayMaxCurl(maxCurl): #Complete
    text = f"You can curl a max of {maxCurl} lbs"
    resultLabel.configure(text=text)

# Loop Start and Kill Functions
#############################################
# Function to stop the webcam capture
def stop_webcam():
    global webcam_running, cap
    if webcam_running:
        webcam_running = False
        cap.release()
        print("Camera Stopped")
    maxCurl = maxCurl_brzycki()
    displayMaxCurl(maxCurl)

# Modify the start_webcam function to start the webcam stream
def pressStart():
    print("Camera Started")
    start_webcam(image)

def buttonPress1():
    # Button reads in the weight int value and arm string value
    weight = int(weightInput.get())
    arm = switch_var.get()
    print(f"Values saved:{weight} {arm}")

    # # Read the data.json file for the weight and reps
    # with open('CoC_Curls\BIG_COC\data.json', 'r') as f:
    #     data = json.load(f)
    # # Access specific values using their keys
    # data['weight'] = weight
    # data['arm'] = arm
    # Write the values to a json file
    with open('CoC_Curls\BIG_COC\data.json', 'w') as f:
        json.dump({"weight":weight, "arm":arm}, f)

def switch_event():
    print("switch toggled, current value:", switch_var.get())

    # while webcam_running == True: 
    #     def max_curl_work():
    #         def readData():
    # # Read the data.json file for the weight and reps
    #             with open('CoC_Curls\\BIG_COC\\data.json', 'r') as f:
    #                 data = json.load(f)
    # # Access specific values using their keys
    #             weight = data['weight']
    #             reps = data['reps']
    #             return weight, reps

    #         def writeData(maxCurl):
    # # Write the updated data to the file
    #             with open('CoC_Curls\\BIG_COC\\data.json', 'r') as f:
    #                 data = json.load(f)
    #             data['maxCurl'] = maxCurl
    #             with open('CoC_Curls\\BIG_COC\\data.json', 'w') as f:
    #                 json.dump(data, f)

    #         def maxCurl_brzycki(weight, reps):
    # # Calculate Max Curl using Brzycki Formula
    #             maxCurl = int(weight * (36 / (37 - reps)))
    #             return maxCurl

    #         def main():
    #             weight, reps = readData()
    #             maxCurl = maxCurl_brzycki(weight, reps)
    #             print(f"Max Curl: {maxCurl} LBS")
    #             writeData(maxCurl)

    #         if __name__ == "__main__":
    #             main()






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
recordButton = ctk.CTkButton(master=inputFrame, text="Start Recording", fg_color='green', hover_color='dark green', command = pressStart)
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
resultLabel = ctk.CTkLabel(master=outputFrame, text=None, font=("Arial", 30 , "bold"))
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
