from Criterium import Criterium
import sys
from Input import Input
from Schedule import Schedule

inputPath2 = r"C:\Users\kinkr\Desktop\DyskD\Pooolibuda\VIIsemestr\PTSZ\Lab\ptsz\1\instances\136810_50.in"

if __name__ == '__main__':
    input = Input()
    #input.readFromFile(inputPath2)
    input.readFromStandard()


    scheduling = Schedule()
    scheduling.getJobs(input.instances)
    scheduling.scheduleOverlapsLossless()
    scheduling.scheduleRest()
    scheduled = scheduling.getFinalSchedule()

    criterium = Criterium()
    criterium.getCriterium(scheduled, input.instances)
    output = str(criterium.weight) + "\n"
    for job in scheduled:
        output += str(job) + " "
    sys.stdout.write(output)
