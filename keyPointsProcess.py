import numpy as np
BODY_PATRS = ['Nose', 'Neck',
              'RShoulder', 'RElbow', 'RWrist',
              'LShoulder', 'LElbow', 'LWrist',
              'MidHip',
              'RHip', 'RKnee', 'RAnkle',
              'LHip', 'LKnee', 'LAnkle',
              'REye', 'LEye', 'REar', 'LEar',
              'LBigToe', 'LSmallToe', 'LHeel',
              'RBigToe', 'RSmallToe', 'RHeel',
              'Background']


def getKeyPoints(keyPointsList):
    if keyPointsList.size == 75:
        coor = {}
        for x in range(25):
            s = ()
            s = (keyPointsList[x][0], keyPointsList[x][1], keyPointsList[x][2])
            coor[BODY_PATRS[x]] = s
        return coor
