import getValue
import matplotlib.pyplot as plt
import sys


def pushUpVisualization(coor, i):
    '''Read coordinates and display it
       input: List of coordinates
       ouput: The analysis of some infos of the whole process
    '''
    plt.ion()
    # for i, coor in enumerate(coorList):
    #     if not coor:
    #         continue
    cnt = i
    r_elbow_angle = getValue.getElbowAngle(coor, 'R')
    r_knee_angle = getValue.getKneeAngle(coor, 'R')
    hip_angle = getValue.getHipAngle(coor, 'R')
    hip_distance = getValue.getHipDistance(coor, 'R')

    # if r_elbow_angle:
    #     elb_ang.append(r_elbow_angle)
    # else:
    #     elb_ang.append(0)

    # if hip_distance:
    #     hip_dis.append(hip_distance)
    # else:
    #     hip_dis.append(0)

    # if r_knee_angle:
    #     knee_ang.append(r_knee_angle)
    # else:
    #     knee_ang.append(0)

    # if hip_angle:
    #     hip_ang.append(hip_angle)
    # else:
    #     hip_ang.append(0)

# elb_ang_below_105 = []
# for ans in elb_ang:
#     if ans < 105:
#         elb_ang_below_105.append(ans)
#     else:
#         elb_ang_below_105.append(None)
# cnt += 1

    ax1 = plt.subplot(2, 2, 1)
# plt.hlines(165, )
# ax1.scatter(range(cnt1), elb_ang, label='elbow angle', s=10)
# ax1.scatter(range(cnt1), elb_ang_below_105, label='elbow angle', color='r', s=10)
# actu = [89, 149, 238, 328, 418, 597, 686, 746, 836, 955, 985]
# region = 0
    ax1.scatter(i, r_elbow_angle, label='elbow angle', s=2)
    # ax1.scatter(i, elb_ang_below_105, label='elbow angle', color='r', s=2)
    ax1.hlines(165, 0, cnt, colors='c')
    # ax1.vlines(actu, 0, 180, colors='r')
    ax1.set_title('elbow_angle')

    ax2 = plt.subplot(2, 2, 2)
    ax2.scatter(i, hip_distance, label='hip distance', s=2)
    ax2.set_title('hip_distance')

    ax3 = plt.subplot(2, 2, 3)
    ax3.scatter(i, r_knee_angle, label='knee angle', s=2)
    # ax3.vlines(actu, 0, 180, colors='r')
    ax3.set_title('knee_angle')

    ax4 = plt.subplot(2, 2, 4)
    ax4.scatter(i, hip_angle, label='hip', s=2)
    # ax4.vlines(actu, 0, 180, colors='r')
    ax4.set_title('hip_angle')
    # plt.pause(0.01)

    plt.plot()
    # plt.savefig(r'E:\University\科研创新\雏燕计划-体测\push-up-side.png')


plt.ion()
ax = plt.subplot(1, 1, 1)
cnt = 0
while sys.stdin.isatty():
    ax.scatter(cnt, sys.stdin.read(), s=2)
    cnt += 1
