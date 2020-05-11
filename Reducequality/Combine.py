 import numpy as np
import cv2
import os

# this two lines are for loading the videos.
# in this case the video are named as: cut1.mp4, cut2.mp4, ..., cut15.mp4
videofiles = ['cut1.avi','cut2.avi','cut3.avi','cut4.avi']
videofiles = sorted(videofiles, key=lambda item: int( item.partition('.')[0][3:]))
fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
video_index = 0
cap = cv2.VideoCapture(videofiles[0])

# video resolution: 1624x1234 px
out = cv2.VideoWriter("video.avi", fourcc, 15, (1624, 1234))

while(cap.isOpened() and video_index < len(videofiles)):
    ret, frame = cap.read()
    if frame is None:
        print ("end of video " + str(video_index) + " .. next one now")
        video_index += 1
        if video_index >= len(videofiles):
            break
        cap = cv2.VideoCapture(videofiles[ video_index ])
        ret, frame = cap.read()
    cv2.imshow('frame',frame)
    out.write(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()

print ("end")
