import test
import analysis
<<<<<<< HEAD
import pullUp
import pushUp

PULL_UP_FILEPATH = r'E:\Programming\Openpose\openpose\openpose\output\pull-up'
PUSH_UP_FILEPATH = r'E:\Programming\Openpose\openpose\openpose\output\pushUp\45cm-4s-2ns\upside'

times = pushUp.pushUpAnalysis(PUSH_UP_FILEPATH)
# times2 = pullUp.pullUpAnalysis(PULL_UP_FILEPATH)
=======
#import pullUp
#import pushUp
import sitUp

#PULL_UP_FILEPATH = r'E:\Programming\Openpose\openpose\openpose\output\pull-up'
#PUSH_UP_FILEPATH = r'E:\Programming\Openpose\openpose\openpose\output\push-up'
SIT_UP_FILEPATH = r'C:\Users\Lenovo\Desktop\雏燕2019\后端部分所需资料\situp-side'

#times = pushUp.pushUpAnalysis(PUSH_UP_FILEPATH)
# times2 = pullUp.pullUpAnalysis(PULL_UP_FILEPATH)
times = sitUp.sitUpAnalysis(SIT_UP_FILEPATH)
>>>>>>> bodyPositionProcess/situp
region = []
for time in times:
    print(time)
    region.append(time['Flag'])
# test.getPullUpInfos(PULL_UP_FILEPATH, True)
<<<<<<< HEAD
test.getPushUpInfos(PUSH_UP_FILEPATH, True, region)
=======
# test.getPushUpInfos(PUSH_UP_FILEPATH, True, region)
test.getSitUpInfos(SIT_UP_FILEPATH, True,region)
>>>>>>> bodyPositionProcess/situp
