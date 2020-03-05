import sys
import cv2
import os
import time
import keyPointsProcess as kpp
# import infoVisualization as iv
from datetime import datetime
import getValue
import analysis
import dataBase as db

try:
    # Windows Import
    # Change these variables to point to the correct folder (Release/x64 etc.)
    sys.path.append(r'E:\Programming\Openpose\openpose\openposePython\build\python\openpose\Release')
    os.environ['PATH'] = os.environ['PATH'] + ';' + r'E:\Programming\Openpose\openpose\openposePython\build\x64\Release;' + r'E:\Programming\Openpose\openpose\openposePython\build\bin;'
    import pyopenpose as op
except ImportError as e:
    print(e)
    print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')

params = dict()
params["model_folder"] = r"E:\Programming\Openpose\openpose\openposePython\models"

# Starting OpenPose
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()

# get video from webcam or video
start = time.time()
cap = cv2.VideoCapture(0)
cap_t = cv2.VideoCapture(1)
# cap2 = cv2.VideoCapture(r'E:\University\科研创新\雏燕计划-体测\体测姿势素材\push-up\push-up-test-1.mp4')
coorList = []


def pullUpDetect(length):
    # Process
    cnt = 0

    results = []
    tendency = []
    result = {}
    r_elbow_angle_list = []
    l_elbow_angle_list = []
    eye_distance_list = []
    tick = []
    pullUpCnt = 0

    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # get video from webcam or video
    start = time.time()
    cap = cv2.VideoCapture(0)
    cap_t = cv2.VideoCapture(1)
    # cap2 = cv2.VideoCapture(r'E:\University\科研创新\雏燕计划-体测\体测姿势素材\push-up\push-up-test-1.mp4')
    coorList = []

    start_time = datetime.now()

    while True:
        # Get images from cam
        ret, imageToProcess = cap.read()
        ret, imageToTest = cap_t.read()
        cv2.imshow('video', imageToProcess)
        cv2.imshow('2', imageToTest)

        cur_time = datetime.now()
        delta_time = (cur_time - start_time).seconds
        print('\r倒计时：' + length - delta_time + '秒', end='')
        if delta_time == length:
            break

        if cnt % 2 == 0:
            datum = op.Datum()
            datum.cvInputData = imageToProcess
            opWrapper.emplaceAndPop([datum])
            if datum.poseKeypoints.size != 1:
                coor = kpp.getKeyPoints(datum.poseKeypoints[0])
                if coor:
                    r_elbow_angle = getValue.getElbowAngle(coor, 'R')
                    l_elbow_angle = getValue.getElbowAngle(coor, 'L')
                    eye_distance = getValue.getEyeWristDistance(coor)

                    if l_elbow_angle:
                        l_elbow_angle_list.append(l_elbow_angle)

                    if eye_distance:
                        eye_distance_list.append(eye_distance)

                    if r_elbow_angle:
                        r_elbow_angle_list.append(r_elbow_angle)
                        tick.append(r_elbow_angle)
                    if len(tick) == 5:
                        tend = analysis.getTendency(tick, 8)  # One tick
                        tick = []
                        if tend:
                            tendency.append(tend)
                            if 3 <= len(tendency):
                                if tendency[-1] == 'down' or tendency[-1] == 'stable':
                                    if tendency[-2] == 'upper' and tendency[-3] == 'upper':  # a period 
                                        pullUpCnt += 1
                                        result['Num'] = pullUpCnt
                                        standard = analysis.pullUpPeriodJudge(r_elbow_angle_list, l_elbow_angle_list, eye_distance_list)
                                        result['IsRElbowStandard'], result['IsLElbowStandard'], result['IsHeightStandard'], total = standard
                                        r_elbow_angle_list = l_elbow_angle_list = eye_distance_list = []
                                        results.append(result)
                                        print(result)
                                        result = {}
                                        db.ret(delta_time, total, pullUpCnt, 'pullUp', results, True)

                cv2.imshow("OpenPose 1.5.1 - Tutorial Python API", datum.cvOutputData)

            if cv2.waitKey(1) == ord('q'):
                break
        cnt += 1
    db.ret(None, None, None, None, None, False)


pullUpDetect(60)
