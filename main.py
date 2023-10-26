# Jacob Auman, Evan Tone, Grant H
# 10-24-23

# First attempt at building the CoC curl detector.

# Import statements
import math
import cv2
from ultralytics import YOLO
import numpy as np

# Load Model 
# ----------------------------------- #
pose_model = YOLO("yolov8s-pose.pt")

keypoint_names = [
    "nose",
    "left_eye",
    "right_eye",
    "left_ear",
    "right_ear",
    "left_shoulder",
    "right_shoulder",
    "left_elbow",
    "right_elbow",
    "left_wrist",
    "right_wrist",
    "left_hip",
    "right_hip",
    "left_knee",
    "right_knee",
    "left_ankle",
    "right_ankle",
]

# Initialize Variable
# ----------------------------------- #
whichSideArm = 'right'
angleThreshold = 90
weightUsed = 35 #Lbs 16 kg in video

frame_counter = 0
fps = 10
rep_counter = 0
keypoints_dict = {}
swingState = "down"

# Functions
# ----------------------------------- #

def getJointCoords(whichSideArm, keypoints_dict):
    # This Function checks which side arm to look for and passes the set of joint coordiantes
    ############################################################
    if whichSideArm == "left" or whichSideArm == "right":
        wrist = np.array([keypoints_dict[f"{whichSideArm}_wrist"]['x'], keypoints_dict[f"{whichSideArm}_wrist"]['y']])
        elbow = np.array([keypoints_dict[f"{whichSideArm}_elbow"]['x'], keypoints_dict[f"{whichSideArm}_elbow"]['y']])
        shoulder = np.array([keypoints_dict[f"{whichSideArm}_shoulder"]['x'], keypoints_dict[f"{whichSideArm}_shoulder"]['y']])
        return wrist, elbow, shoulder
    else:
        raise ValueError("Invalid arm side! (left or right,R)")

def getAngle(whichSideArm, keypoints_dict):
    # This Function is used to calculate the angle at the elbow
    ############################################################
    # Get the correct side, joint coordinates
    wrist, elbow, shoulder = getJointCoords(whichSideArm, keypoints_dict)

    # Use the X, Y coordinates to calculate the angle at the elbow
    # ----------------------------------- #
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

def getAngleRelative(whichSideArm, keypoints_dict):
    # This Function is only really needed for graphing the Joint angle with OpenCV
    # Converts the single angle into two relative angle measured form +X axis counter clockwise
    ############################################################
    wrist, elbow, shoulder = getJointCoords(whichSideArm, keypoints_dict)

    # Create vectors AB and BC
    AB = np.array([wrist[0]-elbow[0], wrist[1]-elbow[1]])
    BC = np.array([shoulder[0] - elbow[0], shoulder[1] - elbow[1]])

    # Calculate the angle between AB and the positive x-axis
    angle_AB = np.arctan2(AB[1], AB[0]) * 180 / np.pi

    # Calculate the angle between BC and the positive x-axis
    angle_BC = np.arctan2(BC[1], BC[0]) * 180 / np.pi

    return angle_AB, angle_BC

def maxCurl_brzycki(weight, reps):
    maxCurl = int(weight * (36 / (37 - reps)))
    # round to the nearest 2.5
    #maxCurl = round(maxCurl * 2) / 2
    return maxCurl



# Video Source choose Webcam or File
# ----------------------------------- #
#cap = cv2.VideoCapture(0) # Webcam front
#cap = cv2.VideoCapture(1) # Webcam back
cap = cv2.VideoCapture('Test_Videos\\16kg-bicep-curl-until-failure-720-ytshorts.savetube.me.mp4') # Video File

# Main Video Loop
# ----------------------------------- #
while cap.isOpened():
    success, frame = cap.read()

    if success:
        frame_counter += 1
        # If the frame number is divisible by 2 proceed
        if frame_counter % fps == 0:

            # Pose detection
            pose_results = pose_model(frame, verbose=False, conf=0.7)

            # Print each body coordinate as a dictionary
            for person in pose_results:
                keypoints = person.keypoints.data[0]
                for keypoint, name in zip(keypoints, keypoint_names):
                    x, y, probability = keypoint
                    keypoints_dict[name] = {"x": x.item(), "y": y.item(), "probability": probability.item()}
        
            # Plot Over the Displayed Frame
            # -------------------------------- #
            if whichSideArm == "left" or whichSideArm == "right":
                elbow_x = int(keypoints_dict[f"{whichSideArm}_elbow"]["x"])
                elbow_y = int(keypoints_dict[f"{whichSideArm}_elbow"]["y"])
                

            # plot the visual elbow arc
            arm_angle = getAngle(whichSideArm, keypoints_dict)
            
            # State Based Rep Counter
            if arm_angle > angleThreshold and swingState == "up":
                swingState = "down"
            if arm_angle < angleThreshold and swingState == "down":
                rep_counter += 1
                swingState = "up"

            # Color for the angles
            if arm_angle < angleThreshold:
                color = (0, 255, 0)
            elif arm_angle > angleThreshold:
                color = (0, 0, 255)
            
            startAngle, endAngle = getAngleRelative(whichSideArm, keypoints_dict)
            cv2.ellipse(frame,((elbow_x), (elbow_y)), (35, 35), 0, startAngle, endAngle, color, -1)
            
            #overlay the angle of the arm at the elbow
            cv2.putText(frame, str(rep_counter), (int(elbow_x), int(elbow_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
        

            # Plot Pose Skeleton on frame
            # -------------------------------- #
            #pose_annotated_frame = person.plot()
            # Plot only the arm of interest
            if whichSideArm == "left" or whichSideArm == "right":
                keypoints = person.keypoints.data[0]
                # Draw the lines between the keypoints
                cv2.line(frame, (int(keypoints_dict[f"{whichSideArm}_wrist"]["x"]), int(keypoints_dict[f"{whichSideArm}_wrist"]["y"])), (int(keypoints_dict[f"{whichSideArm}_elbow"]["x"]), int(keypoints_dict[f"{whichSideArm}_elbow"]["y"])), (255,0,0 ), 4)
                cv2.line(frame, (int(keypoints_dict[f"{whichSideArm}_elbow"]["x"]), int(keypoints_dict[f"{whichSideArm}_elbow"]["y"])), (int(keypoints_dict[f"{whichSideArm}_shoulder"]["x"]), int(keypoints_dict[f"{whichSideArm}_shoulder"]["y"])), (255,0,0 ), 4)
                # Draw the circles at the keypoints
                for keypoint, name in zip(keypoints, keypoint_names):
                    x, y, probability = keypoint
                    if name == f"{whichSideArm}_wrist":
                        cv2.circle(frame, (int(x), int(y)), 5, (0,0,0 ), -2)
                    elif name == f"{whichSideArm}_elbow":
                        cv2.circle(frame, (int(x), int(y)), 5, (0,0,0 ), -2)
                    elif name == f"{whichSideArm}_shoulder":
                        cv2.circle(frame, (int(x), int(y)), 5, (0,0,0 ), -2)
                
            
            cv2.imshow("Pose Detection",frame)
                

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break



# Turn the entire frame black
cv2.rectangle(frame, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 0), -1)

# Print the results
cv2.putText(frame, f"You Curled {weightUsed} lbs", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

cv2.putText(frame, f"For {rep_counter} Reps",(10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

curlMax = maxCurl_brzycki(weightUsed, rep_counter)
cv2.putText(frame, f"Your Max Curl is {curlMax} lbs", (10, 500), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

cv2.imshow("Pose Detection",frame)


cv2.waitKey(0)
cap.release()



# Instead of console prints i think ill map text onto the CV image for the user to see
#|--------------------------------------------------|
#|print(f"Since you were able to {weight}lbs")       |
#|print(f"for {reps} on curls with RPE of {rpe}/10")|
#|print(f"Your current max is {max}lbs, WAY TO GO!!!)|
#|--------------------------------------------------|
