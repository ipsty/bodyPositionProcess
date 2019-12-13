import json
import cv2
import os
import keyPointsProcess as kpp

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
cap_side = cv2.VideoCapture(0)
cap_front = cv2.VideoCapture(1)
# cap2 = cv2.VideoCapture(r'E:\University\科研创新\雏燕计划-体测\体测姿势素材\push-up\push-up-test-1.mp4')


def videoDetect(filepath):
    # Process

    while True:
        ret, imageToProcessFront = cap_front.read()
        ret, imageToProcessSide = cap_side.read()
        cv2.imshow('front', imageToProcessFront)
        cv2.imshow('side', imageToProcessSide
        count = 0
        cnt = 0
        if cnt % 2 == 0:
            datum_front = op.Datum()
            datum_side = op.Datum()
            datum_front.cvInputData = imageToProcessFront
            datum_side.cvInputData = imageToProcessSide
            opWrapper.emplaceAndPop([datum_front])
            opWrapper.emplaceAndPop([datum_side])
            cv2.imshow("front", datum_front.cvOutputData)
            cv2.imshow("side", datum_side.cvOutputData)
            if cv2.waitKey(1) == ord('q'):
                break

            if datum_front.poseKeypoints.size != 1 and datum_side.poseKeypoints.size != 1:
                coor_front = kpp.getKeyPoints(datum_front.poseKeypoints[0])
                coor_side = kpp.getKeyPoints(datum_side.poseKeypoints[0])
                with open(filepath + r'/side/side' + str(count), 'w') as fSide:
                    json.dump(coor_side, fSide)
                with open(filepath + r'/front/front' + str(count), 'w') as fFront:
                    json.dump(coor_front, fFront)


videoDetect('')
