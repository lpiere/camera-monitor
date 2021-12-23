import cv2
import datetime
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
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

def start_move_detector_with_pycamera(time_wrap):
    # initialize the camera and grab a reference to the raw camera capture
    size = (640, 480)
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 60
    rawCapture = PiRGBArray(camera, size=size)
    # allow the camera to warmup
    time.sleep(0.1)
    # capture frames from the camera
    
    prox_frame = []
    start_time = datetime.datetime.now()
    capture = None

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        frame_cv2 = frame.array
        # show the frame
        cv2.imshow("Frame", frame_cv2)

        if len(prox_frame) == 0:
            prox_frame = frame_cv2.copy()
        
        capture, start_time = move_detect(frame_cv2, prox_frame, size, start_time, time_wrap, capture)
        rawCapture.truncate(0)
        
        prox_frame = frame_cv2.copy()
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord("q"):
            break