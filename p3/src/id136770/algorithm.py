import random
import math
from copy import deepcopy

from p3.src.algorithm_api import Algorithm
from p3.src.data_api import Instance, Solution, Schedule


def maxer(task, machine_zeit):
    return max([machine_zeit[2]+task.duration[2], machine_zeit[1]+task.duration[1]+task.duration[2], machine_zeit[0]+sum(task.duration)])

def post_encode(x, machine_zeit):
    return -x[1].weight/sum([x*y for x, y in zip(x[1].duration, bottlenecks)])

velvet_decoder=lambda x: x[1].due_date
velvet_encoder=lambda x: -x[1].weight/sum(x[1].duration)

def evaluat(all_tasks):
    D=0
    n=len(all_tasks)
    m=3

    machine_zeit=m*[0]
    for x in all_tasks:
        task_zeit=0
        for ij in range(m):
            task_zeit=max(machine_zeit[ij], task_zeit)
            task_zeit+=x[1].duration[ij]
            machine_zeit[ij]=task_zeit

        D+=x[1].weight*max(0, task_zeit-x[1].due_date)
    return D/sum([y[1].weight for y in all_tasks])

def h_pop(heap, machine_zeit):
    ind=0
    for i, y in enumerate(heap):
        if post_encode(heap[ind], machine_zeit)>post_encode(y, machine_zeit):
            ind=i        
    res=deepcopy(heap[ind])
    heap.pop(ind)
    return res

def h_push(heap, x):
    heap.append(x)


class Algorithm136770(Algorithm):

    def run(self, in_data: Instance) -> Solution:
        n=in_data.no_tasks
        m=in_data.no_machines

        schedule = []
        end_tasks = []
        machine_zeit=m*[0]
        dead=[0]*(n+10)
        post_heap=[0]*(n+10)
        convoys_to_nothingness=[]

        tasks=in_data.tasks
        pos=range(1, n+1)
        all_tasks = [i for i in zip(pos, tasks)]
        maximal=max([sum([x.duration[y] for x in tasks]) for y in range(m)])
        global bottlenecks
        bottlenecks=[sum([x.duration[y] for x in tasks])/maximal for y in range(m)]

        partial=sorted(all_tasks, key=velvet_decoder)

        batches=math.ceil(math.log(n))
        schedule=[]

        for i, x in partial:
            if len(convoys_to_nothingness)!=0 or dead[i]==1:
                if dead[i]==0 and post_heap[i]==0 and maxer(x, machine_zeit)>=x.due_date:
                    post_heap[i]=1
                    h_push(convoys_to_nothingness, [i, x])
                i, x=h_pop(convoys_to_nothingness, machine_zeit)

            task_zeit=0
            for ij in range(m):
                task_zeit=max(machine_zeit[ij], task_zeit)
                task_zeit+=x.duration[ij]
                machine_zeit[ij]=task_zeit
            schedule.append([i, x])
            dead[i]=1

            for j, y in partial:
                if dead[j]==0 and post_heap[j]==0 and maxer(y, machine_zeit)>=y.due_date:
                    post_heap[j]=1
                    h_push(convoys_to_nothingness, (j, y))

        score=evaluat(schedule)
        schedule = [task[0] for task in schedule]

        return Solution(score=score, schedule=Schedule(no_tasks=n, schedule=schedule))
