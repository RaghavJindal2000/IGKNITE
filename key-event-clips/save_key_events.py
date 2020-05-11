from pyimagesearch.keyclipwriter import KeyClipWriter
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np

cap = cv2.VideoCapture('vtest.mp4')
frame_width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))

frame_height =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc('X','V','I','D')

out = cv2.VideoWriter("output.mp4", fourcc, 5.0, (1280,720))
ap = argparse.ArgumentParser()
args = vars(ap.parse_args())
ret, frame1 = cap.read()
ret, frame2 = cap.read()

c=0
while cap.isOpened() and c<3000:
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 900:
            continue
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 3)
    #cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

        # initialize key clip writer and the consecutive number of
        # frames that have *not* contained any action
        #kcw = KeyClipWriter(bufSize=args["buffer_size"])
        consecFrames = 0

        # keep looping
        while True:


            image = cv2.resize(frame1, (1280,720))
            out.write(image)
            cv2.imshow("feed", frame1)
            frame1 = frame2
            ret, frame2 = cap.read()
            c=c+1
            if cv2.waitKey(40) == 27:
                break
                     # if we are not already recording, start recording
                if not kcw.recording:
                        timestamp = datetime.datetime.now()
                        p = "{}/{}.avi".format(args["output"],
                                timestamp.strftime("%Y%m%d-%H%M%S"))
                        kcw.start(p, cv2.VideoWriter_fourcc(*args["codec"]),
                                args["fps"])


                # otherwise, no action has taken place in this frame, so
                        # increment the number of consecutive frames that contain
                        # no action
                        if updateConsecFrames:
                                consecFrames += 1

                        # update the key frame clip buffer
                        kcw.update(frame)

                        # if we are recording and reached a threshold on consecutive
                        # number of frames with no action, stop recording the clip
                        if kcw.recording and consecFrames == args["buffer_size"]:
                                kcw.finish()

                        # show the frame
                        cv2.imshow("Frame", frame)
                        key = cv2.waitKey(1) & 0xFF

                        # if the `q` key was pressed, break from the loop
                if key == ord("q"):
                        break

# if we are in the middle of recording a clip, wrap it up
if kcw.recording:
	kcw.finish()

cv2.destroyAllWindows()
cap.release()
out.release()
