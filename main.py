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
frame_counter = 0
keypoints_dict = {}


# Functions
# ----------------------------------- #

def getAngle(whichSideArm, keypoints_dict):
    # Side Check Statment
    if whichSideArm == "left" or whichSideArm == "L":
        wrist = np.array([keypoints_dict["left_wrist"]['x'], keypoints_dict["left_wrist"]['y']])
        elbow = np.array([keypoints_dict["left_elbow"]['x'], keypoints_dict["left_elbow"]['y']])
        shoulder = np.array([keypoints_dict["left_shoulder"]['x'], keypoints_dict["left_shoulder"]['y']])
    elif whichSideArm == "right" or whichSideArm == "R":
       wrist = np.array([keypoints_dict["right_wrist"]['x'], keypoints_dict["right_wrist"]['y']])
       elbow = np.array([keypoints_dict["right_elbow"]['x'], keypoints_dict["right_elbow"]['y']])
       shoulder = np.array([keypoints_dict["right_shoulder"]['x'], keypoints_dict["right_shoulder"]['y']])
    else:
        ValueError("Please enter a valid arm side (left or right)")

    # Use the X, Y coordinates to calculate the angle at the elbow
    # ----------------------------------- #
    # Create vectors AB and BC
    AB = wrist - elbow
    BC = shoulder - elbow
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
    
    # Start and End angle are used to draw the arc 

    return angle_output, #startAngle, endAngle





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
                    
                    if name in ["right_shoulder, right_elbow, right_wrist"]: print(True)
                    x, y, probability = keypoint
                    keypoints_dict[name] = {"x": x.item(), "y": y.item(), "probability": probability.item()}
        
            # Plot a circle at the elbow
            # -------------------------------- #
            # LEFT ARM
            # elbow_x = keypoints["left_elbow"]["x"]
            # elbow_y = keypoints["left_elbow"]["y"]
            # RIGHT ARM
            elbow_x = keypoints_dict["right_elbow"]["x"]
            elbow_y = keypoints_dict["right_elbow"]["y"]

            #cv2.circle(frame,(int(elbow_x), int(elbow_y)), 30, (0, 0, 255), 2)
    
            #cv2.ellipse(frame, (int(elbow_x), int(elbow_y)), (25, 25), 0, startAngle, endAngle, (0, 0, 255), -1)
            
            #overlay the angle of the arm at the elbow
            arm_angle = getAngle("right", keypoints_dict)
            cv2.putText(frame, str(arm_angle), (int(elbow_x), int(elbow_y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)


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

