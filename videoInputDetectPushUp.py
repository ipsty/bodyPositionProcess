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
cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)
# cap2 = cv2.VideoCapture(r'E:\University\科研创新\雏燕计划-体测\体测姿势素材\push-up\push-up-test-1.mp4')
coorList = []


def pullUpDetect():
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

    while True:
        # Get images from cam
        ret, imageToProcess1 = cap1.read()
        ret, imageToProcess2 = cap2.read()
        # cv2.imshow(imageToProcess)
        if cnt % 2 == 0:
            datum1 = op.datum()
            datum2 = op.datum()
            datum1.cvInputData = imageToProcess1
            datum2.cvInputData = imageToProcess2
            opWrapper.emplaceAndPop([datum1])
            opWrapper.emplaceAndPop([datum2])
            print("Body keypoints:")
            if datum1.poseKeypoints.size != 1 and datum2.poseKeypoints.size != 1:
                coor_front = kpp.getKeyPoints(datum1.poseKeypoints[0])  # 记得改参数
                coor_side = kpp.getKeyPoints(datum2.poseKeypoints[0])
                r_elbow_angle = getValue.getElbowAngle(coor_front, 'R')
                l_elbow_angle = getValue.getElbowAngle(coor_front, 'L')

                r_knee_angle = getValue.getKneeAngle(coor_side, 'R')
                hip_angle = getValue.getHipAngle(coor_side, 'R')
                hip_distance = getValue.getHipDistance(coor_side, 'R')

                if hip_angle:
                    hip_angle_list.append(hip_angle)

                if r_knee_angle:
                    r_knee_angle_list.append(r_knee_angle)

                if r_elbow_angle:
                    r_elbow_angle_list.append(r_elbow_angle)
                    tick.append(r_elbow_angle)

                if l_elbow_angle:
                    l_elbow_angle_list.append(l_elbow_angle)

                if hip_distance:
                    hip_distance_list.append(hip_distance)

                if len(tick) == 5:
                    tend = analysis.getTendency(tick, 20)  # One tick
                    tick = []
                    if tend:
                        tendency.append(tend)
                        if 3 <= len(tendency):
                            if tendency[-1] == 'down' or tendency[-1] == 'stable':
                                if tendency[-2] == 'upper' and tendency[-3] == 'upper':  # a period
                                    cnt += 1
                                    result['Num'] = cnt
                                    standard = analysis.pushUpPeriodJudgeTwoSides(r_elbow_angle_list, l_elbow_angle_list,
                                                                                hip_angle_list, r_knee_angle_list,
                                                                                hip_distance_list)
                                    result['IsRElbowStandard'], result['IsLElbowStandard'], result['IsHipAngleStandard'], result['IsRKneeStandard'], result['IsHipDistanceStandard'] = standard
                                    result['Flag'] = i

                                    r_elbow_angle_list = []
                                    l_elbow_angle_list = []
                                    r_knee_angle_list = []
                                    hip_angle_list = []
                                    hip_distance_list = []

                                    results.append(result)
                                    print(result)
                                    result = {}
        cnt += 1

    end = time.time()
    print("OpenPose demo successfully finished. Total time: " + str(end - start) + " seconds")
    # except Exception as e:
    #     print(e)
    #     sys.exit(-1)


pullUpDetect()
