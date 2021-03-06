import sys
import cv2
import os
from sys import platform
import time
import keyPointsProcess as kpp

# try:
# Import Openpose (Windows/Ubuntu/OSX)
dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    # Windows Import
    # Change these variables to point to the correct folder (Release/x64 etc.)
    sys.path.append(r'E:\Programming\Openpose\openpose\openposePython\build\python\openpose\Release')
    os.environ['PATH'] = os.environ['PATH'] + ';' + r'E:\Programming\Openpose\openpose\openposePython\build\x64\Release;' + r'E:\Programming\Openpose\openpose\openposePython\build\bin;'
    import pyopenpose as op
except ImportError as e:
    print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
    raise e

params = dict()
params["model_folder"] = r"E:\Programming\Openpose\openpose\openposePython\models"

# Starting OpenPose
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()

# get video from webcam or video
start = time.time()
# cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(r'E:\University\科研创新\雏燕计划-体测\体测姿势素材\push-up\push-up-test-1.mp4')
# if not cap.isOpened():
#     print("Cannot open camera")
# Process and display images
cnt = 0
while True:
    # Get images from cam
    ret, imageToProcess = cap2.read()
    # frame = cv2.flip(frame, 1)

    # cv2.imshow('frame', fr5ame)
    # print(frame)
    # print("type:", type(frame))
    if cnt % 2 == 0:
        datum = op.Datum()
        datum.cvInputData = imageToProcess
        opWrapper.emplaceAndPop([datum])
        # print(type(datum.poseKeypoints), 'Shape', datum.poseKeypoints.shape)
        print("Body keypoints: \n")
        # print(datum.poseKeypoints.size)
        if datum.poseKeypoints.size != 1:
            coor = kpp.getKeyPoints(datum.poseKeypoints[0])
            print(coor)
            cv2.imshow("OpenPose 1.5.1 - Tutorial Python API", datum.cvOutputData)

        if cv2.waitKey(1) == ord('q'):
            break
    cnt += 1

end = time.time()
print("OpenPose demo successfully finished. Total time: " + str(end - start) + " seconds")
# except Exception as e:
#     print(e)
#     sys.exit(-1)
