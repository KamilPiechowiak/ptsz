#!/usr/bin/env python3
import sys

INF = int(1e18)

class Task:
    def __init__(self, p, r, d, w):
        self.p, self.r, self.d, self.w = p, r, d, w

def read_instance(file):
    n = int(file.readline())
    tasks = []
    for i in range(n):
        tasks.append(Task(*[int(x) for x in file.readline().split(" ") if x != "\n"]))
    return tasks

def compute_loss(order, tasks):
    loss = 0
    t = 0
    for idx in order:
        task = tasks[idx]
        t = max(t, task.r)
        t+=task.p
        if t > task.d:
            loss+=task.w
    return loss

def place_and_reject(order, tasks):
    placed = []
    rejected = []
    t = 0
    for idx in order:
        task = tasks[idx]
        if max(t, task.r)+task.p <= task.d:
            placed.append(idx)
            t = max(t, task.r)+task.p
        else:
            rejected.append(idx)
    return placed+rejected

def earlier_ready_first(tasks):
    n = len(tasks)
    order = [i for i in range(n)]
    order.sort(key = lambda idx: tasks[idx].r)
    return place_and_reject(order, tasks)

def earlier_duedate_first(tasks):
    n = len(tasks)
    order = [i for i in range(n)]
    order.sort(key = lambda idx : tasks[idx].d)
    # print(order)
    return place_and_reject(order, tasks)

def max_unit_weight_first(tasks, choose_place):
    n = len(tasks)
    order = [i for i in range(n)]
    order.sort(key = lambda idx : -tasks[idx].w/tasks[idx].p)
    placed = [] #i, latest_begin_i
    rejected = []
    for idx in order:
        task = tasks[idx]
        prev_earliest_stop = 0
        chosen_place = -1
        for i in range(len(placed)+1): #find places to put a new task
            if i != len(placed):
                elem = placed[i]
            else:
                elem = (-1, INF)
            if max(prev_earliest_stop, task.r)+task.p <= min(task.d, elem[1]):
                chosen_place = choose_place(chosen_place, i)
            if elem[0] == -1: #last element
                continue
            current_task = tasks[elem[0]]
            prev_earliest_stop = max(prev_earliest_stop, current_task.r)+current_task.p

        if chosen_place != -1: #place new task and possibly move others
            current_start = task.d
            if chosen_place < len(placed):
                current_start = min(current_start, placed[chosen_place][1])
            current_start-= task.p
            placed.insert(chosen_place, [idx, current_start])
            i = chosen_place-1
            while i >= 0:
                current_task = tasks[placed[i][0]]
                if placed[i+1][1]-current_task.p >= placed[i][1]:
                    break
                placed[i][1] = placed[i+1][1]-current_task.p
                i-=1
        else: #move new task to the end
            rejected.append(idx)

    return [x[0] for x in placed]+rejected

def max_unit_weight_first_leftmost(tasks):
    def choose_place(chosen_place, i):
        return i if chosen_place == -1 else chosen_place
    return max_unit_weight_first(tasks, choose_place)

def max_unit_weight_first_rightmost(tasks):
    def choose_place(chosen_place, i):
        return i
    return max_unit_weight_first(tasks, choose_place)

def solve():
    tasks = read_instance(sys.stdin)
    # order = max_unit_weight_first_rightmost(tasks)
    # print(compute_loss(order, tasks))
    # print(" ".join([str(idx+1) for idx in order]))
    methods = [earlier_ready_first, earlier_duedate_first, max_unit_weight_first_leftmost, max_unit_weight_first_rightmost]
    best_order = []
    best_loss = INF
    for f in methods:
        order = f(tasks)
        loss = compute_loss(order, tasks)
        if loss < best_loss:
            best_loss = loss
            best_order = order
    print(best_loss)
    print(" ".join([str(idx+1) for idx in best_order]))

if __name__ == "__main__":
    solve()