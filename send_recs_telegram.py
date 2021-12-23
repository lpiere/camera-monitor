import telegram_send as ts
import os
import time

def send_video(paths=[]):
    for path in paths:
        if 'rec' in path:
            continue
        print(path)
        time.sleep(2)
        with open(f'./videos/{path}', 'rb') as video:
            ts.send(videos=[video])

        os.remove(f'./videos/{path}')
    
    
    

def start_monitor():
    ts.send(messages=['monitor iniciado'])
    while True:
        videos = os.listdir('./videos')
        send_video(paths=videos)
