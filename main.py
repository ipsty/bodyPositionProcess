import test
import analysis
import pullUp
import pushUp

import videoInputDetectSitUp as su
import videoInputDetectPullUp as pllu
import videoInputDetectPushUp as pshu

PULL_UP_FILEPATH = r'E:\Programming\Openpose\openpose\openpose\output\pull-up'
PUSH_UP_FILEPATH = r'E:\Programming\Openpose\openpose\openpose\output\pushUp\45cm-4s-2ns\upside'

times = pushUp.pushUpAnalysis(PUSH_UP_FILEPATH)
# times2 = pullUp.pullUpAnalysis(PULL_UP_FILEPATH)
region = []
for time in times:
    print(time)
    region.append(time['Flag'])
# test.getPullUpInfos(PULL_UP_FILEPATH, True)
test.getPushUpInfos(PUSH_UP_FILEPATH, True, region)
def main():
    su.sitUpDetect(60)
    # pllu.pullUpDetect(60)
    # pshu.pushUpDetect(60)

main()
