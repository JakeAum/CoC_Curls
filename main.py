# Jacob Auman and Evan Tone
# 10-24-23

# First attempt at building the CoC curl detector.

# Import statements
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

            # Call func for angle of the arm
            

            # Plot a circle at the elbow
            # -------------------------------- #
        
            # LEFT ARM
            # elbow_x = keypoints["left_elbow"]["x"]
            # elbow_y = keypoints["left_elbow"]["y"]

            # RIGHT ARM
            elbow_x = keypoints_dict["right_elbow"]["x"]
            elbow_y = keypoints_dict["right_elbow"]["y"]

            #cv2.circle(frame,(int(elbow_x), int(elbow_y)), 30, (0, 0, 255), 2)
            #cv2.ellipse(frame, (int(elbow_x), int(elbow_y)), (25, 25), 0, startAngle, endAngle, color[, thickness[, lineType[, shift]]])
            

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

