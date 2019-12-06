import sys
import analysis
import getValue
import jsonProcess as jp

def pushUpAnalysisReadByPipe(folder_path):
    '''Open folder and process .json into a dict
       input: The file path
       ouput: The times of push-up
       Judge by tendency!
    '''

    results = []
    tendency = []
    result = {}
    r_elbow_angle_list = []
    r_knee_angle_list = []
    hip_angle_list = []
    # l_elbow_angle_list = []
    tick = []
    cnt = 0

    for i, file in sys.stdin.fileno():
        coor = jp.getJson(folder_path + '\\' + file)
        if not coor:
            continue

        r_elbow_angle = getValue.getElbowAngle(coor, 'R')
        r_knee_angle = getValue.getKneeAngle(coor, 'R')
        hip_angle = getValue.getHipAngle(coor, 'R')

        if hip_angle:
            hip_angle_list.append(hip_angle)

        if r_knee_angle:
            r_knee_angle_list.append(r_knee_angle)

        if r_elbow_angle:
            r_elbow_angle_list.append(r_elbow_angle)
            tick.append(r_elbow_angle)

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
                            standard = analysis.pushUpPeriodJudge(r_elbow_angle_list, hip_angle_list, r_knee_angle_list)
                            result['IsRElbowStandard'], result['IsHipAngleStandard'], result['IsRKneeStandard'] = standard
                            result['Flag'] = i
                            r_elbow_angle_list = r_knee_angle_list = hip_angle_list = []
                            results.append(result)
                            result = {}
    # print(tendency)
    return results
