#!/usr/bin/env python3
import sys

w = 0
S = 1
H = 2
l = 3
O = 0
M = 0


def find_next(jobs, K, j):
    B = None
    R = -1000
    s = []
    for i in range(len(jobs)):
        if i + 1 not in j and K >= jobs[i][S]:
            P = 2 * jobs[i][l] / M - jobs[i][H] / O
            if K + jobs[i][w] > jobs[i][H]:
                s.append(i)
            elif P > R:
                R = P
                B = i
    if B is None and s.__len__() != 0:
        B = s.pop()
    return B


def rank_jobs(t, jobs):
    global O, M
    for i in range(len(jobs)):
        if jobs[i][H] > O:
            O = jobs[i][H]
        if jobs[i][l] > M:
            M = jobs[i][l]
    j = []
    K = 0
    F = 0
    while t != j.__len__():
        U = find_next(jobs, K, j)
        if U is None:
            K += 1
        else:
            K += jobs[U][w]
            if K > jobs[U][H]:
                F += jobs[U][l]
            j.append(U + 1)
    return F, j


def main(argv):
    p = []
    m = int(input())
    for i in range(m):
        h = input().split(" ")
        p.append([int(x.strip()) for x in h if x != ' '])
    c, j = rank_jobs(m, p)
    print(c)
    for i in range(len(j)):
        print(j[i], end=' ')


if __name__ == "__main__":
    main(sys.argv[1:])