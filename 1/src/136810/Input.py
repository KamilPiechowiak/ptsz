class Input:
    def __init__(self):
        self.size = 0
        self.instances = []

    def readFromStandard(self):
        self.size = int(input())
        for i in range(0, int(self.size)):
            self.instances.append(list(map(lambda x: int(x), input().split())))

    def readFromFile(self, inputPath):
        file = open(inputPath)
        allLines = file.readlines()
        file.close()
        content = [line.split() for line in allLines]
        output = []
        for row in content:
            row = [int(i) for i in row]
            output.append(row)
        self.size = int(output[0][0])
        self.instances = output[1:]
