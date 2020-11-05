import sys
import math

first=-1
class Task:
    def __init__(self, nr, inside_system, proc_time, deadline, weight):
        self.nr=nr
        self.p_time=proc_time
        self.r_time=inside_system
        self.d_time=deadline
        self.weight=weight

    def __str__(self):
        return f'Task: processing time: {self.p_time}, interval <{self.r_time}:{self.d_time}>, weight: {self.weight}'

class Task_in_order:
    #prev, next - następny obiekt w Porządku Przeznaczenia, beg, end - czasy początku/zakończenia (różnica to proc_time)
    def __init__(self, task, beg, end, prev, nexte):
        self.task=task
        self.beg=beg
        self.end=end-1 #Kontrowersja
        self.prev=prev
        self.next=nexte

    def __str__(self):
        return f'Task nr {self.task.nr}: working in time interval: <{self.beg}:{self.end}>'


def parse(line):
    x=line.split(' ')
    if (x[-1]=='' or x[-1]==' ' or x[-1]=='\n'):
        x.pop()
    if x[-1][-1]=='\n':
        x[-1]=x[-1][:-1]
    y=[int(z) for z in x]
    return y

def try_insert_before(nachste, task_x):
    global first
    if nachste.prev==-1:
        left_possible=task_x.r_time
    else:
        left_possible=max(nachste.prev.end+1, task_x.r_time)
    right_possible=min(nachste.beg-1, task_x.d_time)

    if right_possible - left_possible >= task_x.p_time-1:
        cur=Task_in_order(task_x, left_possible, left_possible+task_x.p_time, nachste.prev, nachste)
        if nachste.prev!=-1:
            nachste.prev.next=cur
        else:
            first=cur
        nachste.prev=cur
        return 1
    return -1


def pusherman(task_x):
    global first
    last=first
    while last.next!=-1:
        last=last.next

    while (last.prev!=-1):
        last.end=min(last.task.d_time, last.next.beg-1) if last.next!=-1 else last.task.d_time
        last.beg=last.end-last.task.p_time+1
        last=last.prev

    
    while type(last)!=type(-1):
        res=try_insert_before(last, task_x)
        if (res==1):
            return
        last.beg=max(last.prev.end+1, last.task.r_time) if last.prev!=-1 else last.task.r_time
        last.end=last.beg+last.task.p_time-1
        seminal=last
        last=last.next

    left_possible=max(seminal.end+1, task_x.r_time)
    right_possible=task_x.d_time
    if right_possible - left_possible >= task_x.p_time-1:
        cur=Task_in_order(task_x, left_possible, left_possible+task_x.p_time, seminal, -1)
        seminal.next=cur



def easy_add(task_x):
    global first
    if first==-1:
        cur=Task_in_order(task_x, task_x.r_time, task_x.r_time+task_x.p_time, -1, -1)
        first=cur
        return 1
    else:
        nachste=first
        while type(nachste)!=type(-1):
            res=try_insert_before(nachste, task_x)
            if (res==1):
                return
            last=nachste
            nachste=nachste.next

        left_possible=max(last.end+1, task_x.r_time)
        right_possible=task_x.d_time
        if right_possible - left_possible >= task_x.p_time-1:
            cur=Task_in_order(task_x, left_possible, left_possible+task_x.p_time, last, -1)
            last.next=cur
        else:
            pusherman(task_x)


def caterpillar(task_x):
    global first

    right=first
    left=first
    current_best_cut=0
    summa=0

    while type(right)!=type(-1):
        summa+=right.task.weight
        while left.task.nr != right.task.nr:
            lefty=left.end+1
            righty=right.next.beg-1 if right.next!=-1 else right.end+1+task_x.p_time
            if righty-lefty < task_x.p_time-1:
                break
            summa-=left.task.weight
            left=left.next
        lefty=max(left.prev.end+1, task_x.r_time) if left.prev!=-1 else task_x.r_time
        righty=min(right.next.beg-1, task_x.d_time) if right.next!=-1 else task_x.d_time

        if righty-lefty >= task_x.p_time-1 and summa+current_best_cut < task_x.weight:
            current_best_cut = task_x.weight-summa
            best_left_cut=left
            best_right_cut=right

        right=right.next

    if current_best_cut > 0:
        lefty=max(best_left_cut.prev.end+1, task_x.r_time) if best_left_cut.prev!=-1 else task_x.r_time
        cur=Task_in_order(task_x, lefty, lefty+task_x.p_time, best_left_cut.prev, best_right_cut.next)
        #print(f'Swap addon: {current_best_cut}')
        #print(f'Left: {best_left_cut}')
        #print(f'Right: {best_right_cut}')
        #print(f'Real: {cur}')
        if (best_left_cut.prev==-1):
            first=cur
        else:
            best_left_cut.prev.next=cur

        if (best_right_cut.next!=-1):
            best_right_cut.next.prev=cur


lst=[]
n=int(input())
dp=[0]*n
for i in range(n):
    tmp=parse(input())
    lst.append(Task(i, tmp[1], tmp[0], tmp[2], tmp[3]))

sorted_lst=sorted(lst, key=lambda x: -x.weight/x.p_time)
loge=int(math.ceil(math.log(n)))
#_=[print(x) for x in sorted_lst]

for x in sorted_lst:
    res=easy_add(x)

for j in range(loge):
    nachste=first
    while type(nachste)!=type(1):
        dp[nachste.task.nr]=1
        nachste=nachste.next

    for x in sorted_lst:
        if dp[x.nr]==0:
            caterpillar(x)

    dp=[0]*n
    nachste=first
    while type(nachste)!=type(1):
        dp[nachste.task.nr]=1
        nachste=nachste.next

for x in sorted_lst:
    if dp[x.nr]==0:
        easy_add(x)

dp=[0]*n
nachste=first
while type(nachste)!=type(1):
    dp[nachste.task.nr]=1
    nachste=nachste.next

cost=0
all_cost=0
for i in range(0, n):
    if dp[i]==0:
        cost+=lst[i].weight
    all_cost+=lst[i].weight

print(str(cost))
nachste=first
while type(nachste)!=type(1):
    if nachste.task.p_time != nachste.end-nachste.beg+1:
        print("LIPA!")
    if nachste.beg < nachste.task.r_time:
        print("LIPA!")
    if nachste.end > nachste.task.d_time:
        print("LIPA!")
    if nachste.next!=-1 and nachste.next.beg <= nachste.end:
        print("LIPA!")
    if nachste.prev!=-1 and nachste.prev.end >= nachste.beg:
        print("LIPA!")

    print(str(nachste.task.nr+1), end=' ')
    nachste=nachste.next

for i in range(0, n):
    if dp[i]==0:
        print(i+1, end=' ')

print()
