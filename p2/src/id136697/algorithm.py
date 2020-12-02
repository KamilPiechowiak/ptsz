from p2.src.algorithm_api import Algorithm
from p2.src.data_api import Instance, Solution, Schedule


class Algorithm136697(Algorithm):
   
    @staticmethod    
    def double_sort(task_list):
        task_list.sort(key=lambda x: (x[2], x[1]))  # sorty by r then by p
        return task_list
    @staticmethod
    def rearange_machines(b):
        b.sort(key=lambda x: x[2])  # sort by bi from the fastest to the slowest
        return b
    @staticmethod    
    def algorytm(sorted_task_list, sorted_machines):
        tasks_to_machine_allocation = [[],[],[],[],[]]
        F = 0
        real_time = 0
        for real_task_index, pi, ri in sorted_task_list:
            task_done = False
            predicted_Cis_sorted_machines = [[0,-1],[1,-1],[2,-1],[3,-1],[4,-1]] #sorted_machine_index, predicted_ci
            for sorted_machine_index, (real_machine_index, machine_time, machine_delay) in enumerate(sorted_machines):
                if(machine_time <= ri): #machine idle
                    machine_time = ri + round(pi*machine_delay, 6)
                    sorted_machines[sorted_machine_index][1] = machine_time
                    tasks_to_machine_allocation[real_machine_index].append(real_task_index)
                    task_done = True
                    Ci = machine_time
                    Fi = Ci - ri
                    F += Fi
                    break
                else: #machine not idle
                    predicted_Cis_sorted_machines[sorted_machine_index][1] = machine_time + round(pi*machine_delay, 6)
                    predicted_Cis_sorted_machines[sorted_machine_index][0] = sorted_machine_index
            if(not task_done):
                for sorted_machine_index, predicted_ci in sorted(predicted_Cis_sorted_machines, key=lambda x: x[1]):
                    if(predicted_ci != -1):
                        real_machine_index = sorted_machines[sorted_machine_index][0]
                        machine_time = predicted_ci
                        sorted_machines[sorted_machine_index][1] = machine_time
                        tasks_to_machine_allocation[real_machine_index].append(real_task_index)
                        task_done = True
                        Fi = predicted_ci - ri
                        F += Fi
                        break
        return tasks_to_machine_allocation, sorted_machines, F
        
    def run(self, in_data: Instance) -> Solution:        
        
        machines = in_data.machine_speeds
        machines2 = [[],[],[],[],[]]
        for i in range(len(machines)):
            machines2[i] = [i, 0, machines[i]] #real machine index, time, delay
        sorted_machines = self.rearange_machines(machines2)
        
        tasks_weird = in_data.tasks
        tasks_unsorted = []
        for task_index, task in enumerate(tasks_weird):
            tasks_unsorted.append([task_index+1, task.duration, task.ready])
        
        sorted_tasks = self.double_sort(tasks_unsorted) #((real_task_index, p, r), ())
        tasks_to_machine_allocation, sorted_machines, F = self.algorytm(sorted_tasks, sorted_machines)
        
        n = len(tasks_weird)
        
        # print(tasks_to_machine_allocation)
        
        
        schedule = Schedule(n = n, m = len(machines), schedule = tasks_to_machine_allocation)
                
        return Solution(score = round(F/n, 6), schedule = schedule)
        
