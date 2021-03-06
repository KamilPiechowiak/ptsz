#!/usr/bin/env python3
import sys
from metadata import indices
import numpy as np
import subprocess as sp
import os

def create_sequential_solution(n, path, project_no):
    with open(path, "w") as file:
        if project_no == 1:
            file.write(f"0\n")
            file.write(" ".join([str(i+1) for i in range(n)]))
        elif project_no == 2:
            file.write("0\n")
            n_i = [n//5]*5
            n_i[4] = n-(n//5)*4
            start = 0
            for i in range(5):
                file.write(" ".join([str(i+1) for i in range(start, start+n_i[i])]))
                file.write("\n")
                start+=n_i[i]

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} project_no validator_command", file=sys.stderr)
        exit(-1)

    project_no = int(sys.argv[1])
    validator_command = sys.argv[2]

    losses = []
    
    path = "seq.out"
    for index in indices:
        for n in range(50, 501, 50):
            create_sequential_solution(n, path, project_no)
            validator = sp.Popen([*validator_command.split(" "), f"{project_no}/instances/{index}_{n}.in", "o", path], stdout=sp.PIPE)
            loss = int(validator.communicate()[0].decode("utf-8").split(" ")[1])
            losses.append(loss)
    os.remove(path)
    print("\n".join([str(loss) for loss in losses]))
