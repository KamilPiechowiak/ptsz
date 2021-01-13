from p3.src.algorithm_api import Algorithm
from p3.src.data_api import Instance, Solution, Schedule
import sys


class Algorithm136697(Algorithm):

    def run(self, in_data: Instance) -> Solution:
    
        n = in_data.no_tasks
        no_machines = in_data.no_machines
        tasks_list = in_data.tasks
        
        
        tasks_list = [[i+1,x,0] for i,x in enumerate(tasks_list)] 
        
        
        
        tasks_list.sort(key = lambda t: (t[1].duration[0]+t[1].duration[1]+t[1].duration[2])*t[1].due_date/t[1].weight)
        
       
        maximum = -1
        time1 = 0
        time2 = 0
        time3 = 0 
        c1 = 0
        c2 = 0
        c3 = 0
        mianownik = 0
        licznik = 0
                    
            
        #wyliczanie wyniku
        for x in tasks_list:
            task_number = x[0]
            task_info = x[1]
            p1 = task_info.duration[0]
            p2 = task_info.duration[1]
            p3 = task_info.duration[2]
            due_date = task_info.due_date
            weight = task_info.weight
                        
            time1 += p1
            c1 = time1
            
            time2 = max(c1, c2) 
            time2 += p2
            c2 = time2
            
            time3 = max(c2, c3)
            time3 += p3 
            c3 = time3
            
            Dj = max(0, c3 - due_date)
            mianownik += weight
            licznik += weight*Dj
        
        score = licznik/mianownik
        
        schedule = Schedule(no_tasks = n, schedule = [index_tasksinfo[0] for index_tasksinfo in tasks_list])
        
        return Solution(score = score, schedule = schedule)
        
