#!/usr/bin/env python3
import sys
from metadata import indices, program_commands
import subprocess as sp

INF = str(int(1e18))

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} project_no validator_command student_index", file=sys.stderr)
        exit(-1)
    
    project_no = int(sys.argv[1])
    validator_command = sys.argv[2]
    student_index = sys.argv[3]

    losses = []
    times = []
    for n in range(50, 501, 50):
        losses_row = []
        times_row = []
        for index in indices:
            if index not in program_commands[project_no].keys():
                loss, ti = INF, INF
            else:
                validator = sp.Popen([*validator_command.split(" "), f"{project_no}/instances/{student_index}_{n}.in", "p", program_commands[project_no][index]], stdout=sp.PIPE)
                out = validator.communicate()[0].decode("utf-8").split(" ")
                if int(out[0]) != 1:
                    loss, ti = INF, INF
                else:
                    loss = str(int(out[1]))
                    ti = str(round(float(out[2]), 3))#.replace(".", ",")
            losses_row.append(loss)
            times_row.append(ti)
        losses.append(losses_row)
        times.append(times_row)

    print("\n".join(["\t".join(row) for row in losses]), end="\n\n")
    print("\n".join(["\t".join(row) for row in times]), end="\n\n")