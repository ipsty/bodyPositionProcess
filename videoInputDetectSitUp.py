import sys
import cv2
import os
import time
import keyPointsProcess as kpp
# import infoVisualization as iv
import matplotlib.pyplot as plt
import getValue
import analysis

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
params[
    "model_folder"] = r"E:\Programming\Openpose\openpose\openposePython\models"

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


def sitUpDetect():
    '''Open folder and process .json into a dict
       input: The file path
       ouput: The times of push-up
    '''

    results = []
    tendency = []
    tick = []
    result = {}
    r_waist_angle_list = []
    l_waist_angle_list = []
    r_s_knee_angle_list = []
    l_s_knee_angle_list = []
    r_elbowtoneck_dist_list = []
    l_elbowtoneck_dist_list = []

    total_r_elbowtoneck_dist = 0
    total_l_elbowtoneck_dist = 0
    cnt = cnt_1 = cnt_2 = 0

    while True:
        # Get images from cam
        ret, imageToProcessFront = cap_front.read()
        ret, imageToProcessSide = cap_side.read()
        cv2.imshow('front', imageToProcessFront)
        cv2.imshow('side', imageToProcessSide)
        if cnt % 2 == 0:
            datum1 = op.Datum()
            datum2 = op.Datum()
            datum1.cvInputData = imageToProcessFront
            datum2.cvInputData = imageToProcessSide
            opWrapper.emplaceAndPop([datum1])
            opWrapper.emplaceAndPop([datum2])
            if datum1.poseKeypoints.size != 1 and datum2.poseKeypoints.size != 1:
                coor_front = kpp.getKeyPoints(datum1.poseKeypoints[0])  # 记得改参数
                coor_side = kpp.getKeyPoints(datum2.poseKeypoints[0])
                r_waist_angle = getValue.getWaistAngle(coor_side, 'R')
                l_waist_angle = getValue.getWaistAngle(coor_side, 'L')
                r_s_knee_angle = getValue.getKneeAngle(coor_side, 'R')
                l_s_knee_angle = getValue.getKneeAngle(coor_side, 'L')
                r_elbowtoneck_dist = getValue.getElbowToNeckDistance(coor_front, 'R')
                l_elbowtoneck_dist = getValue.getElbowToNeckDistance(coor_front, 'L')

                if l_waist_angle:
                    l_waist_angle_list.append(r_waist_angle)
                    tick.append(l_waist_angle)
                    # if l_waist_angle:
                    #     l_waist_angle_list.append(l_waist_angle)
                    if r_s_knee_angle:
                        r_s_knee_angle_list.append(r_s_knee_angle)
                    if l_s_knee_angle:
                        l_s_knee_angle_list.append(l_s_knee_angle)
                    if r_elbowtoneck_dist:
                        r_elbowtoneck_dist_list.append(r_elbowtoneck_dist)
                        cnt_1 += 1
                        total_r_elbowtoneck_dist += r_elbowtoneck_dist
                        aver_r_elbowtoneck_dist = total_r_elbowtoneck_dist / cnt_1
                    if l_elbowtoneck_dist:
                        l_elbowtoneck_dist_list.append(l_elbowtoneck_dist)
                        cnt_2 += 1
                        total_l_elbowtoneck_dist += l_elbowtoneck_dist
                    aver_l_elbowtoneck_dist = total_l_elbowtoneck_dist / cnt_2

                    if len(tick) == 5:
                        tend = analysis.getTendency(tick, 8)  # One tick
                        tick = []
                        if tend:
                            tendency.append(tend)
                            if 3 <= len(tendency):
                                if tendency[-1] == 'down':
                                    if tendency[
                                            -2] == 'upper':  # a period and tendency[-3] == 'upper'
                                        cnt += 1
                                        result['Num'] = cnt
                                        standard = analysis.sitUpPeriodJudge(
                                            r_waist_angle_list, l_waist_angle_list,
                                            r_s_knee_angle_list, l_s_knee_angle_list,
                                            r_elbowtoneck_dist_list,
                                            l_elbowtoneck_dist_list,
                                            aver_r_elbowtoneck_dist,
                                            aver_l_elbowtoneck_dist)
                                        result['IsRWaistStandard'], result[
                                            'IsLWaistStandard'] = standard
                                        result['IsRKneeAngle'], result[
                                            'IsLKneeAngle'] = standard
                                        result['IsRElbowtoNeckStandard'], result[
                                            'IsLElbowtoNeckStandard'] = standard
                                        # result['Flag'] = i
                                        r_waist_angle_list = l_waist_angle_list = []
                                        r_s_knee_angle_list = l_s_knee_angle_list = []
                                        r_elbowtoneck_dist_list = l_elbowtoneck_dist_list = [
                                        ]   # 序列置空
                                        cnt_1 = cnt_2 = 0
                                        results.append(result)
                                        print(result)
                                        result = {}
        cnt += 1
        cv2.imshow("OpenPose 1.5.1 - Tutorial Python API", datum1.cvOutputData)
        cv2.imshow("OpenPose 1.5.1 - Tutorial Python API - front", datum2.cvOutputData)

        if cv2.waitKey(1) == ord('q'):
            break


sitUpDetect()
