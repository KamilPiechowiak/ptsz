from Job import Job


def getSingleJobs(index, initJob):
    job = Job()
    job.number = index
    job.canStart = initJob[1]
    job.canEnd = initJob[2]
    job.weight = initJob[3]
    job.duration = initJob[0]
    return job


def debug(job):
    print("JOB")
    #print("\tLATE: ", job.canEnd - job.finished)
    #print("\tSTART GOOD: ", job.begin - job.canStart)
    #print("\tNUMBER: ", job.number)
    print("\tBEGIN: ", job.begin)
    print("\tSTART: ", job.canStart)
    print("\tFINISH: ", job.finished)
    print("\tEND: ", job.canEnd)
    print("\tDURATION: ", job.duration)
    # print("\tWEIGHT: ", job.weight)

    # -2 no overlap before
    # -1 overlap before
    # 0 - inside/outside
    # 1 overlap after
    # 2 no overlap after


def checkOverlap(job, subjob):
    if subjob.canStart <= job.canStart and subjob.canEnd >= job.canEnd \
            or subjob.canStart >= job.canStart and subjob.canEnd <= job.canEnd:
        return 0
    elif subjob.canStart < job.canStart and subjob.canEnd <= job.canStart:
        return -2
    elif subjob.canStart < job.canStart < subjob.canEnd:
        return -1
    elif subjob.canStart < job.canEnd < subjob.canEnd:
        return 1
    elif subjob.canStart >= job.canEnd and subjob.canEnd > job.canEnd:
        return 2

def isOverlapping(job, overlapping):
    for i in range(0, len(overlapping)):
        start = min(map(lambda x: x.canStart, overlapping[i]))
        end = max(map(lambda x: x.canEnd, overlapping[i]))
        mockJob = Job()
        mockJob.canEnd = end
        mockJob.canStart = start
        overlap = checkOverlap(mockJob, job)
        if -1 <= overlap <= 1:
            return i
    return -1


def getNewLimits(job, overlap, limits):
    if overlap == -1:
        return [max([limits[0], job.canEnd]), limits[1]]
    elif overlap == 1:
        return [limits[0], min([limits[1], job.canStart])]
    elif overlap == 0:
        if job.canStart == limits[0]:
            return [job.canStart, min([limits[1], job.canEnd])]
        elif job.canEnd == limits[1]:
            return [max(limits[0], job.canStart), job.canEnd]
        elif job.canStart > limits[0] and job.canEnd < limits[1]:
            return [[limits[0], job.canStart], [job.canEnd, limits[1]]]
        else:
            return [0, 0]
    else:
        return [limits[0], limits[1]]


class Schedule:
    def __init__(self):
        self.currentMoment = 0
        self.jobs = []
        self.scheduled = []

    # OTHER FUNCTIONS
    def flushJobs(self):
        self.jobs = list(set(self.jobs) - set(self.scheduled))

    def getJobs(self, initJobs):
        self.jobs = [getSingleJobs(i, job) for i, job in enumerate(initJobs)]
        self.jobs.sort(key=lambda job: job.canStart)

    def scheduleSingleJob(self, job, jobBegin, jobFinish):
        job.begin = jobBegin
        job.finished = jobFinish
        self.scheduled.append(job)

    def getOverlappingSets(self):
        overlappingSets = []
        self.jobs.sort(key=lambda x: x.canStart)
        for job in self.jobs:
            updatedSet = isOverlapping(job, overlappingSets)
            if updatedSet == -1:
                overlappingSets.append([job])
            else:
                overlappingSets[updatedSet].append(job)
        return overlappingSets

    def limitJobSet(self, jobs):
        minimumStart = min(map(lambda job: job.canStart, jobs))
        maximumEnd = max(map(lambda job: job.canEnd, jobs))
        mockedJob = Job()
        mockedJob.canStart = minimumStart
        mockedJob.canEnd = maximumEnd
        for scheduled in self.scheduled:
            overlap = checkOverlap(mockedJob, scheduled)
            if overlap == -1:
                minimumStart = scheduled.finished
            elif overlap == 1:
                maximumEnd = scheduled.begin
            else:
                continue
        return minimumStart, maximumEnd

    # NO-OVERLAPS
    def scheduleNoOverlaps(self):
        for job in self.jobs:
            before = []
            after = []
            hasBiggerJob = False
            for subjob in self.jobs:
                overlap = checkOverlap(job, subjob)
                if overlap == 0:
                    hasBiggerJob = True
                    break
                elif overlap == -1:
                    before.append(subjob)
                elif overlap == 1:
                    after.append(subjob)
            if hasBiggerJob:
                continue
            if len(before) == 0 and len(after) == 0:
                self.scheduleSingleJob(job, job.canStart, job.canStart + job.duration)
            elif len(before) == 0:
                minimumStart = min(map(lambda i: i.canStart, after))
                if minimumStart - job.duration >= job.canStart:
                    self.scheduleSingleJob(job, minimumStart - job.duration, minimumStart)
            elif len(after) == 0:
                maximumEnd = max(map(lambda i: i.canEnd, before))
                if maximumEnd + job.duration <= job.canEnd:
                    self.scheduleSingleJob(job, job.canEnd - job.duration, job.canEnd)
        self.flushJobs()

    # NO-LOSSLESS
    def fitLimits(self, job, limits):
        for limit in limits:
            fits = limit[1] - limit[0] >= job.duration
            if fits:
                return limit
        return False

    def scheduleSingleSet(self, jobSet, limits):
        jobSet.sort(key=lambda x: x.canStart)
        for job in jobSet:
            newLimits = [(max(limits[0], job.canStart), min(limits[1], job.canEnd))]
            for subjob in jobSet:
                updatedLimits = []
                for limit in newLimits:
                    mockJob = Job()
                    mockJob.canStart = limit[0]
                    mockJob.canEnd = limit[1]
                    overlap = checkOverlap(mockJob, subjob)
                    updatedLimit = getNewLimits(subjob, overlap, limit)
                    if isinstance(updatedLimit[0], list):
                        for sublist in updatedLimit:
                            updatedLimits.append(sublist)
                    else:
                        updatedLimits.append(updatedLimit)
                newLimits = updatedLimits
                if not self.fitLimits(job, newLimits):
                    break
            limitForJob = self.fitLimits(job, newLimits)
            if limitForJob:
                self.scheduleSingleJob(job, limitForJob[0], limitForJob[0] + job.duration)

    def scheduleOverlapsLossless(self):
        overlapping = self.getOverlappingSets()
        for ov in overlapping:
            limits = self.limitJobSet(ov)
            self.scheduleSingleSet(ov, limits)
        self.flushJobs()

    # REST
    def fits(self, job, preJob):
        scheduledEnd = preJob.begin + preJob.duration
        if scheduledEnd + job.duration > job.canEnd:
            return False
        return True

    def getOverlappingScheduled(self, job, scheduled):
        output = []
        for scheduledJob in scheduled:
            if 1 >= checkOverlap(job, scheduledJob) >= -1:
                output.append(scheduledJob)
        return output

    def getPossibleChanges(self, job, overlaps):
        output = []
        for overlappingJob in overlaps:
            startSet = []
            endSet = []
            if overlappingJob.canStart + job.duration <= job.canEnd:
                mockStart = Job()
                mockStart.canStart = overlappingJob.canStart
                mockStart.canEnd = overlappingJob.canStart + job.duration
                for subJob in overlaps:
                    if -1 <= checkOverlap(mockStart, subJob) <= 1:
                        startSet.append(subJob)
            if overlappingJob.canEnd + job.duration <= job.canEnd:
                mockEnd = Job()
                mockEnd.canStart = overlappingJob.canEnd
                mockEnd.canEnd = overlappingJob.canEnd + job.duration
                for subJob in overlaps:
                    if -1 <= checkOverlap(mockEnd, subJob) <= 1:
                        endSet.append(subJob)
            if len(startSet) > 0 and startSet not in output:
                output.append((startSet, overlappingJob.canStart))
            if len(endSet) > 0 and endSet not in output:
                output.append((endSet, overlappingJob.canEnd))
        return output

    def getInitialSchedule(self, jobSet):
        scheduled = []
        outScheduled = []
        for job in jobSet:
            if len(scheduled) == 0:
                job.begin = job.canStart
                scheduled.append(job)
            elif self.fits(job, scheduled[-1]):
                job.begin = max([scheduled[-1].begin + scheduled[-1].duration, job.canStart])
                scheduled.append(job)
            else:
                outScheduled.append(job)
        return scheduled, outScheduled

    def getBestChanges(self, scheduled, outScheduled):
        bestChanges = []
        for job in outScheduled:
            bestGain = 0
            changeSet = 0
            overlappingScheduled = self.getOverlappingScheduled(job, scheduled)
            possibleChanges = self.getPossibleChanges(job, overlappingScheduled)
            for change in possibleChanges:
                changeWeight = 0
                for jobsToChange in change[0]:
                    changeWeight += jobsToChange.weight
                if job.weight - changeWeight > bestGain:
                    bestGain = job.weight - changeWeight
                    changeSet = (job, change, bestGain)
            if changeSet != 0:
                bestChanges.append(changeSet)
        bestChanges.sort(key=lambda x: x[2], reverse=True)
        return bestChanges

    def switchJobs(self, bestChanges, scheduled, outScheduled):
        alreadyChanged = []
        toChange = []
        for index, change in enumerate(bestChanges):
            newChangedNums = list(map(lambda x: x.number, change[1][0]))
            intersec = set(alreadyChanged).intersection(set(newChangedNums))
            if len(intersec) == 0:
                alreadyChanged += newChangedNums
                toChange.append(index)
        for index in toChange:
            change = bestChanges[index]
            outScheduled[outScheduled.index(change[0])].begin = change[1][1]
            for scheduledJob in change[1][0]:
                scheduled[scheduled.index(scheduledJob)].begin = -1
        return scheduled, outScheduled


    def scheduleRest(self):
        overlapping = self.getOverlappingSets()
        for jobSet in overlapping:
            scheduled, outScheduled = self.getInitialSchedule(jobSet)
            bestChanges = self.getBestChanges(scheduled, outScheduled)
            scheduled, outScheduled = self.switchJobs(bestChanges, scheduled, outScheduled)
            for job in scheduled + outScheduled:
                if job.begin != -1:
                    self.scheduleSingleJob(job, job.begin, job.begin + job.duration)
            #należy schedulować lepszą pracę, zdobyć jej begin w jakiś sposób w funkcji getPossibleChange
        self.flushJobs()

    def getFinalSchedule(self):
        self.scheduled.sort(key=lambda x: x.begin)
        self.jobs.sort(key=lambda x: x.canStart)
        scheduled = self.scheduled + self.jobs
        #print(suma)
        return list(map(lambda job: job.number + 1, scheduled))
