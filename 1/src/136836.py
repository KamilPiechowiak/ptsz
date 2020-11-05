#!/usr/bin/python3
import os
import sys
class task():
    def __init__(self, id, att):
        self.p = int(att[0])
        self.r = int(att[1])
        self.d = int(att[2])
        self.w = int(att[3])
        self.id = id


def saveFile(serialized):
    currentMoment = 0
    score = 0
    for task in serialized:
        currentMoment = max(currentMoment, task.r)
        currentMoment += task.p
        score += task.w if task.d < currentMoment else 0

    print(score)

    f = sys.stdout
    for task in serialized:
        f.write(str(task.id)+" ")
    f.close()

def serialize(taskList):
    taskList = sorted(taskList, key=lambda task: -(task.w) )
    E = []
    p = 0
    l = taskList

    for task in taskList:
        E.append(task)
        p += task.p
        if p > task.d:
            possible = [t for t in E if t.d > p]
            if len(possible) != 0:
                chosenTask = max(possible, key=lambda task: task.d)
                E.remove(chosenTask)
                E.append(chosenTask)
            else:
                chosenTask = max(E, key=lambda task: task.p)
                p -= chosenTask.p
                E.remove(chosenTask)

    rest = [task for task in l if task not in E]
    serialized = sorted(E, key=lambda task: task.d) + rest
    return serialized

def main():
    taskList = []
    with sys.stdin as f:
        size = int(f.readline())
        for num, line in enumerate(f, 1):
            att = line.split()
            taskList.append(task(num, att))

    serialized = serialize(taskList)
    saveFile(serialized)

if __name__=="__main__":
    main()

