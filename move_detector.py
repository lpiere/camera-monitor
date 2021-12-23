import cv2
import datetime
import os

def calculate_min_max(contours):
    min_x, max_x = 100000, 0
    min_y, max_y = 100000, 0
    for cout in contours:
        for coord in cout:
            x, y = coord[0]
            if(x > max_x):
                max_x = x
            if(x < min_x):
                min_x = x
            if(y > max_y):
                max_y = y
            if(y < min_y):
                min_y = y


    return min_x, max_x, min_y, max_y

def has_move(frame, min_x, max_x, min_y, max_y):
    width = max_x - min_x
    height = max_y - min_y
    new_frame = frame.copy()

    if(min_x > 10 and min_y > 10 and min_x != 100000 and min_y != 100000):
        new_frame = cv2.rectangle(new_frame, (min_x, min_y),(min_x+width,min_y+height), (0,0,255), 2)
        return new_frame, True

    return frame, False

def frame_filters(frame, prox_frame):
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    prox_frame_gray = cv2.cvtColor(prox_frame, cv2.COLOR_BGR2GRAY)
    
    frame_diff = cv2.absdiff(frame_gray, prox_frame_gray)
    
    imgGauss = cv2.GaussianBlur(frame_diff, (5,5),0)

    metodo = cv2.THRESH_BINARY_INV
    ret, imgBin = cv2.threshold(imgGauss, 100, 255, metodo)

    imgSeg = cv2.Canny(imgBin, 100, 200)

    return imgSeg

def rec_moviment(should_capture, capture, size, frame, file_name):
    if 'videos' not in os.listdir():
        os.mkdir('./videos')

    if should_capture and capture == None:
        new_capture = cv2.VideoWriter(f'./videos/{file_name}.rec.mp4', 
                        cv2.VideoWriter_fourcc(*'MP4V'),
                        20,
                        size)
        # print('start rec', file_name)
        return new_capture
    elif should_capture:
        # print('rec frame')
        capture.write(frame)
        return capture
    elif capture != None:
        # print('rec released')
        os.rename(f'./videos/{file_name}.rec.mp4', f'./videos/{file_name}.mp4')
        capture.release()
        return None

def move_detect(frame, prox_frame, size, start_time, time_wrap, capture):
    seconds = (datetime.datetime.now() - start_time).seconds

    imgSeg = frame_filters(frame, prox_frame)
    
    (contours, hierarchy) = cv2.findContours(imgSeg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    min_x, max_x, min_y, max_y = calculate_min_max(contours)
    new_frame, has_moviment = has_move(frame, min_x, max_x, min_y, max_y)
    
    if has_moviment and seconds > time_wrap and capture == None:
        start_time = datetime.datetime.now()
        seconds = (datetime.datetime.now() - start_time).seconds

    should_capture = seconds <= time_wrap

    file_name = start_time.strftime("date_%m_%d_%Y_time_%H_%M_%S")
    new_capture = rec_moviment(should_capture, capture, size, frame, file_name)

    return new_capture, start_time
