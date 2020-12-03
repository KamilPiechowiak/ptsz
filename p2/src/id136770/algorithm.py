import sys
sys.path.append('.')
from p2.src.algorithm_api import Algorithm
from p2.src.data_api import Instance, Solution, Task

class Strange_Machines:
    def __init__(self, nr, coef):
        self.nr=nr
        self.last=-1
        self.first=-1
        self.coef=coef

class Task_in_Order:
    def __init__(self, task, machine, prev, nexte, t0, no):
        self.task=task
        self.no=no
        self.machine=machine

        self.prev=prev
        if prev!=-1:
            prev.nexte=self

        self.nexte=nexte
        if nexte!=-1:
            nexte.prev=self

        self.t0=t0
        self.t_end=t0+task.duration*machine.coef
    def __str__(self):
        prv=self.prev
        if prv!=-1:
            prv=prv.no

        nxt=self.nexte
        if nxt!=-1:
            nxt=nxt.no
        return f'no: {self.no}, machine: {self.machine.nr}, p/n: {prv}, {nxt}, t0: {self.t0}, t_end: {self.t_end}'


class Algorithm136770(Algorithm):
    def run(self, in_data: Instance) -> Solution:
        def add_meaning(mach, task, prev, nexte, t0, no):
            order_of_destiny=Task_in_Order(task, mach, prev, nexte, t0, no)
            if prev==-1:
                mach.first=order_of_destiny
            if nexte==-1:
                mach.last=order_of_destiny

            cur_task=order_of_destiny
            while cur_task!=-1:
                if prev!=-1 and cur_task.t0 < cur_task.prev.t_end:
                    cur_task.t0=cur_task.prev.t_end
                    cur_task.t_end=cur_task.t0+mach.coef*cur_task.task.duration
                cur_task=cur_task.nexte

        def procession(task, machine):
            if machine.first==-1:
                return task.duration*machine.coef, -1, -1, task.ready
            
            #Wstaw za lastem
            last=machine.last
            slain=-1
            slain_tasks=0
            cost=0
            res=0
            cur_cost=-1
            full_task_zeit=task.duration*machine.coef

            while True:
                if last!=-1:
                    nachste=last.nexte
                    t0=max(last.t_end, task.ready)
                else:
                    nachste=machine.first
                    t0=task.ready

                start_loss=t0-task.ready

                start_diff=full_task_zeit+1
                if nachste!=-1:
                    start_diff=nachste.t0-t0

                if start_diff>=full_task_zeit:
                    k=t0+full_task_zeit
                    slain=-1
                    res=0
                    slain_tasks=0


                else:
                    purged=0
                    if slain==-1:
                        slain=nachste
                    all_break=start_diff
                    slain_tasks+=1
                    while True:
                        bias=k-slain.t_end
                        if all_break<=bias:
                            k=k-all_break
                            break
                        else:
                            purged+=bias
                            all_break-=bias
                            res=res-purged
                            slain_tasks-=1
                            k=slain.t0
                            slain=slain.prev
                    res=res-slain_tasks*start_diff
                    res=res+task.duration*machine.coef

                cost=start_loss+res
                if cur_cost==-1 or cost<cur_cost:
                    cur_cost, cur_prev, cur_nexte, cur_t0=cost, last, nachste, t0

                if last==-1 or last.t0 < task.ready:
                    break
                last=last.prev

            return cur_cost+full_task_zeit, cur_prev, cur_nexte, cur_t0

        n=in_data.no_tasks
        m=in_data.no_machines
        tasks=in_data.tasks      
        machinas=in_data.machine_speeds

        strangers=[]
        overall_cost=0
        for i, x in enumerate(machinas):
            strangers.append(Strange_Machines(i, x))

        pos=range(1, n+1)
        all_tasks=list(zip(pos, tasks))
        all_tasks=sorted(all_tasks, key=lambda x: x[1].duration)

        for ij, ts in all_tasks:
            cur_cost=-1
            for mach in strangers:
                cost, prev, nexte, t0=procession(ts, mach)
                if cost<cur_cost or cur_cost==-1:
                    cur_cost, cur_mach, cur_prev, cur_nexte, cur_t0=cost, mach, prev, nexte, t0
            add_meaning(cur_mach, ts, cur_prev, cur_nexte, cur_t0, ij)
            overall_cost+=cur_cost

        my_schedule=[]
        for mach in strangers:
            fst=mach.first
            lst=[]
            while fst!=-1:
                lst.append(fst.no)
                fst=fst.nexte
            my_schedule.append(lst)
        #print(sum([len(x) for x in my_schedule]), sum([sum(x) for x in my_schedule])-(n*(n+1)//2))
        #print(my_schedule)
        #print(overall_cost/len(tasks))

        return Solution(score=overall_cost/len(tasks), schedule=my_schedule)


if __name__=='__main__':
    t1=Task(3, 10)
    t2=Task(5, 2)
    t3=Task(7, 5)
    t4=Task(1, 8)

    t5=Task(20, 50)
    t6=Task(1000, 1000)
    t7=Task(25, 30)

    t8=Task(2, 110)
    t9=Task(2, 112)
    t10=Task(2, 114)
    t11=Task(6, 107)
    t12=Task(3, 119)

    tasks=[t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12]
    ind=Instance(len(tasks), 1, [1.0], tasks)

    falka=Algorithm136770()
    falka.run(ind)


    t1=Task(4, 8)
    t2=Task(2, 14)
    t3=Task(5, 18)
    t4=Task(6, 25)
    t5=Task(1, 32)
    t6=Task(8, 6)
    t7=Task(3, 36)
    t8=Task(1, 40)
    t9=Task(1, 41)
    t10=Task(2, 43)
    tasks=[t1, t2, t3, t4, t5, t6, t7, t8, t9, t10]
    ind=Instance(len(tasks), 1, [1.0], tasks)
    falka.run(ind)



