from typing import List

from p2.src.id136810.alg.Job import Job


class Machine:
    scheduled_jobs: List[Job]
    end_moment: float
    speed: float
    number: int

    def __init__(self, speed: float, number: int):
        self.speed = speed
        self.number = number
        self.end_moment = 0
        self.scheduled_jobs = []

    def schedule(self, job: Job):
        self.scheduled_jobs.append(job)
        self.end_moment = job.end

    def getSchedule(self):
        return [job.number for job in self.scheduled_jobs]

    def __str__(self):
        output = f"\n{{M{self.number} Speed: {self.speed}"
        curr_end = -1
        for index in range(0, len(self.scheduled_jobs)):
            if self.scheduled_jobs[index].begin != curr_end:
                if curr_end != -1:
                    output += f"{self.scheduled_jobs[index - 1].end}] "
                output += f"[{self.scheduled_jobs[index].begin}-"
            curr_end = self.scheduled_jobs[index].end
        if output[-2] != "]" and curr_end != -1:
            output += f"{curr_end}]"
        output += "}"
        return output

    def __repr__(self):
        return self.__str__()