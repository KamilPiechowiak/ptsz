#!/usr/bin/env python3
import sys
import os
import time
from my.s136780 import Task, read_instance, compute_loss

def run_program(instance_path, program_command, output_path):
    t1 = time.time()
    os.system(f"{program_command} < {instance_path} > {output_path}")
    t2 = time.time()
    return (t2-t1)*1000

def check_order(n, order):
    if len(order) != n:
        print("Number of tasks is incorrect", file=sys.stderr)
        return False
    used = [0]*n
    for idx in order:
        if idx < 0 or idx >= n:
            print("Invalid task number encountered", file=sys.stderr)
            return False
        if used[idx] != 0:
            print("Single task appearing multiple times", file=sys.stderr)
            return False
        used[idx]+=1
    return True
    

def test_result(instance_path, output_path):
    with open(instance_path) as file:
        tasks = read_instance(file)
    with open(output_path) as file:
        loss = int(file.readline())
        order = [int(x)-1 for x in file.readline().split(" ") if x != "\n"]
    
    if check_order(len(tasks), order) == False:
        return 0, 0

    my_loss = compute_loss(order, tasks)
    correct = 1
    if my_loss != loss:
        print("Invalid loss", file=sys.stderr)
        correct = 0
    return my_loss, correct

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} instance_path o|p output_path|program_command", file=sys.stderr)
        print("Program name should end with .py", file=sys.stderr)
        print("If program is given, returns: correct loss time", file=sys.stderr)
        print("If output is given returns: correct loss", file=sys.stderr)
        exit(-1)
    instance_path = sys.argv[1]
    if sys.argv[2] == "p":
        output_path = "tmp.out"
        program_command = sys.argv[3]
        t = run_program(instance_path, program_command, output_path)
        loss, exit_code = test_result(instance_path, output_path)
        print(exit_code, loss, t)
    else:
        output_path = sys.argv[3]
        loss, exit_code = test_result(instance_path, output_path)
        print(exit_code, loss)