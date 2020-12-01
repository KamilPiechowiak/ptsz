class Job:
    number: int
    ready_moment: int
    duration: int
    begin: float
    end: float

    def __init__(self, ready_moment, duration, number):
        self.ready_moment = ready_moment
        self.duration = duration
        self.number = number
        self.begin = -1
        self.end = -1

    def __str__(self):
        output = f"\nJob no: {self.number}\tReady: {self.ready_moment}\tDuration: {self.duration}"
        if self.begin != -1:
            output += f"\tbegin: {self.begin}\tend: {self.end}"
        return output

    def __repr__(self):
        return self.__str__()
