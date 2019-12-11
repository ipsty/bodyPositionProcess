import numpy as np
import cv2 as cv

cap1 = cv.VideoCapture(0)
cap2 = cv.VideoCapture(1)
if not cap1.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # capture frame-by-frame
    ret, frame = cap1.read()
    ret, frame2 = cap2.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Our operations on the frame come here
    # Display the resulting frame
    cv.imshow('frame1', frame)
    cv.imshow('frame2', frame2)
    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the cap1ture
cap1.release()
cv.destroyAllWindows()
