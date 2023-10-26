import numpy as np
import cv2 as cv
import time

def record_video(): 
    cap = cv.VideoCapture(0)

    goal_time = 15

    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    out = cv.VideoWriter('Test_Videos\output.mp4', fourcc, 20.0, (640, 480))

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    start_time = time.time()
    while (int(time.time()-start_time) < goal_time):
        
        ret, frame = cap.read()
    
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        
        out.write(frame)
        cv.imshow('frame', frame)
        
        if cv.waitKey(1) == ord('q'):
            break

    cap.release()
    out.release()
    cv.destroyAllWindows()