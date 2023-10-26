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

frame_counter = 0
keypoints_dict = {}

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
        if frame_counter % 2 == 0:

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
            if arm_angle < angleThreshold:
                color = (0, 255, 0)
            elif arm_angle > angleThreshold:
                color = (0, 0, 255)
            
            startAngle, endAngle = getAngleRelative(whichSideArm, keypoints_dict)
            cv2.ellipse(frame,((elbow_x), (elbow_y)), (35, 35), 0, startAngle, endAngle, color, -1)
            
            #overlay the angle of the arm at the elbow
            #cv2.putText(frame, str(arm_angle), (int(elbow_x), int(elbow_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
            
            


            # Plot Pose Skeleton on frame
            # -------------------------------- #
            pose_annotated_frame = person.plot()
            cv2.imshow("Pose Detection", pose_annotated_frame)
                

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()

