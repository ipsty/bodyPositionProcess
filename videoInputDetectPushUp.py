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

dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    # Windows Import
    # Change these variables to point to the correct folder (Release/x64 etc.)
    sys.path.append(
        r'E:\Programming\Openpose\openpose\openposePython\build\python\openpose\Release'
    )
    os.environ['PATH'] = os.environ[
        'PATH'] + ';' + r'E:\Programming\Openpose\openpose\openposePython\build\x64\Release;' + r'E:\Programming\Openpose\openpose\openposePython\build\bin;'
    import pyopenpose as op
except ImportError as e:
    print(e)
    print(
        'Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?'
    )

params = dict()
params["model_folder"] = r"E:\Programming\Openpose\openpose\openposePython\models"




def pushUpDetect(length):
    # Process
    cnt = 0

    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # get video from webcam or video
    start = time.time()
    cap_side = cv2.VideoCapture(0)
    cap_front = cv2.VideoCapture(1)
    # cap2 = cv2.VideoCapture(r'E:\University\科研创新\雏燕计划-体测\体测姿势素材\push-up\push-up-test-1.mp4')
    coorList = []


    results = []
    tendency = []
    result = {}
    r_elbow_angle_list = []
    l_elbow_angle_list = []
    l_knee_angle_list = []
    hip_angle_list = []
    hip_distance_list = []
    tick = []
    pushUpCnt = 0

    start_time = datetime.now()

    while True:
        # Get images from cam
        ret, imageToProcessFront = cap_front.read()
        ret, imageToProcessSide = cap_side.read()
        cv2.imshow('front', imageToProcessFront)
        cv2.imshow('side', imageToProcessSide)
        cnt = 0

        cur_time = datetime.now()
        delta_time = (cur_time - start_time).seconds
        print('\r倒计时：' + length - delta_time + '秒', end='')
        if delta_time == length:
            break

        if cnt % 2 == 0:
            datum_front = op.Datum()
            datum_side = op.Datum()
            datum_front.cvInputData = imageToProcessFront
            datum_side.cvInputData = imageToProcessSide
            opWrapper.emplaceAndPop([datum_front])
            opWrapper.emplaceAndPop([datum_side])
            # print("Body keypoints:")
            if datum_front.poseKeypoints.size != 1 and datum_side.poseKeypoints.size != 1:
                coor_front = kpp.getKeyPoints(datum_front.poseKeypoints[0])  # 记得改参数
                coor_side = kpp.getKeyPoints(datum_side.poseKeypoints[0])
                r_elbow_angle = getValue.getElbowAngle(coor_front, 'R')
                l_elbow_angle = getValue.getElbowAngle(coor_front, 'L')

                l_knee_angle = getValue.getKneeAngle(coor_side, 'L')
                hip_angle = getValue.getHipAngle(coor_side, 'L')
                hip_distance = getValue.getHipDistance(coor_side, 'L')

                if r_elbow_angle:
                    r_elbow_angle_list.append(r_elbow_angle)
                    tick.append(r_elbow_angle)
                    if hip_angle:
                        hip_angle_list.append(hip_angle)

                    if l_knee_angle:
                        l_knee_angle_list.append(l_knee_angle)

                    if l_elbow_angle:
                        l_elbow_angle_list.append(l_elbow_angle)

                    if hip_distance:
                        hip_distance_list.append(hip_distance)

                    if len(tick) == 5:
                        tend = analysis.getTendency(tick, 20)  # One tick
                        print(tend)
                        tick = []
                        if tend:
                            tendency.append(tend)
                            if 3 <= len(tendency):
                                if tendency[-1] == 'down' or tendency[-1] == 'stable':
                                    if tendency[-2] == 'upper':  # a period and tendency[-3] == 'upper'
                                        pushUpCnt += 1
                                        result['Num'] = pushUpCnt
                                        standard = analysis.pushUpPeriodJudgeTwoSides(
                                            r_elbow_angle_list,
                                            l_elbow_angle_list, hip_angle_list,
                                            l_knee_angle_list,
                                            hip_distance_list)
                                        result['IsRElbowStandard'], result[
                                            'IsLElbowStandard'], result[
                                                'IsHipAngleStandard'], result[
                                                    'IsRKneeStandard'], result[
                                                        'IsHipDistanceStandard'], total = standard

                                        r_elbow_angle_list = []
                                        l_elbow_angle_list = []
                                        l_knee_angle_list = []
                                        hip_angle_list = []
                                        hip_distance_list = []
                                        pushUpCnt += 1
                                        results.append(result)
                                        print(result)
                                        result = {}
                                        db.ret(delta_time, total, pushUpCnt, 'pushUp', results, True)
        cnt += 1
        cv2.imshow("front", datum_front.cvOutputData)
        cv2.imshow("side", datum_side.cvOutputData)

        if cv2.waitKey(1) == ord('q'):
            break
    db.ret(None, None, None, None, None, False)

pushUpDetect(60)
