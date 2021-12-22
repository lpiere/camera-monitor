import cv2
import datetime
from move_detector import move_detect

def start_move_detector_with_webcam(time_wrap, source_camera):
    cap = cv2.VideoCapture(source_camera)
    ret, frame = cap.read()
    prox_frame = frame.copy()

    frame_width = int(cap.get(3)) 
    frame_height = int(cap.get(4)) 

    size = (frame_width, frame_height) 
    capture = None
    start_time = datetime.datetime.now()
    while True:
        # cv2.imshow("screen", new_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        capture, start_time = move_detect(frame, prox_frame, size, start_time, time_wrap, capture)
        
        prox_frame = frame.copy()
        ret, frame = cap.read()

    cap.release()
    cv2.destroyAllWindows()
