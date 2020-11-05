DURATION = 0
START = 1
END = 2
WEIGHT = 3

class Criterium:
    def __init__(self):
        self.moment = 0
        self.weight = 0

    def analyseInstance(self, instance):
        if instance[START] > self.moment:
            self.moment = instance[START]
        self.moment += instance[DURATION]
        if instance[END] < self.moment:
            self.weight += instance[WEIGHT]

    def getCriterium(self, output, instances):
        for instanceIndex in output:
            self.analyseInstance(instances[instanceIndex - 1])