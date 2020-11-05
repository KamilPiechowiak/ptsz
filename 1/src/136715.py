#!/usr/bin/env python3
import sys

u = 0
t = 1
N = 2
q = 3
A = 0
C = 0


def read_files(w: str):
    w = open(w, "r+")
    return int(w.readline().rstrip()), [[int(x) for x in line.strip().split(' ')] for line in w.readlines()]


def find_next(jobs, y, L):
    p = None
    b = -1000
    n = []
    for i in range(len(jobs)):
        if i + 1 not in L and y > jobs[i][t]:
            d = 2 * jobs[i][q] / C - jobs[i][N] / A
            if y + jobs[i][u] > jobs[i][N]:
                n.append(i)
            elif d > b:
                b = d
                p = i
    if p is None and n.__len__() != 0:
        p = n.pop()
    return p


def rank_jobs(l, jobs):
    global A, C
    for i in range(len(jobs)):
        if jobs[i][N] > A:
            A = jobs[i][N]
        if jobs[i][q] > C:
            C = jobs[i][q]
    L = []
    y = 0
    J = 0
    while l != L.__len__():
        r = find_next(jobs, y, L)
        if r is None:
            y += 1
        else:
            y += jobs[r][u]
            if y > jobs[r][N]:
                J += jobs[r][q]
            L.append(r + 1)
    return J, L


def main(argv):
    f = []
    a = int(input())
    for i in range(a):
        v = input().split(" ")
        f.append([int(x) for x in v])
    M, L = rank_jobs(a, f)
    sys.stdout.write(M.__str__())
    sys.stdout.write("\n")
    for i in range(len(L)):
        sys.stdout.write(L[i].__str__())
        sys.stdout.write(" ")


if __name__ == "__main__":
    main(sys.argv[1:])