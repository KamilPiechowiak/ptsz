import os
import pandas as pd


def calculate_crit(seq: pd.DataFrame) -> int:
    beg = 0
    cri = 0
    for s in seq.index:
        inx = s
        beg = max(tasks[1][inx], beg) + tasks[0][inx]
        if beg > tasks[2][inx]:
            cri += tasks[3][inx]
    return cri


if __name__ == "__main__":

    # path = sys.argv[1]
    tmp = []
    n = int(input())
    for i in range(n):
        tmp.append([int(x) for x in input().split(' ') if x != ''])
    path = 'tmp.tmp'
    with open(path, 'w') as file:
        file.write(str(n) + '\n')
        for i in range(n):
            file.write(' '.join([str(x) for x in tmp[i]]))
            file.write('\n')

    tasks = pd.read_csv(path, sep=' ', skiprows=1, header=None)
    os.remove(path)
    # tasks = tasks.sort_values(by=[3], ascending=True)
    # print(tasks, '\n\n')
    seq = tasks.sort_values(by=[1, 3, 2], ascending=[True, False, True])
    # print(seq, '\n\n')
    # print(seq.index)
    # for s in seq.index:
    # print(s)
    end = []

    cri = 0
    beg = 0
    ev = 0

    for s in seq.iterrows():
        ev = max(s[1][1], beg) + s[1][0]
        if ev > s[1][2]:
            end.append(s)
            continue
        beg = ev
    for inx in end:
        seq = seq.drop(inx[0])
    # print(seq, '\n\n', len(seq[0]))

    cri = calculate_crit(seq)
    second_end = []
    sec_inx = []

    for e in end:
        inx = 0
        # print(seq.iloc[5][0])
        for i in range(len(seq[0])):
            if seq.iloc[i][1] >= e[1][1]:
                for m in (-1, 0, 1):

                    if 0 <= i+m < len(seq[0]) and seq.iloc[i + m][3] < e[1][3]:
                        tmp = pd.concat([seq.iloc[:(i+m)], pd.DataFrame(index=[e[0]],
                                                                    data={0: e[1][0], 1: e[1][1], 2: e[1][2],
                                                                          3: e[1][3]}),
                                         seq.iloc[(i + m + 1):]])  # [e[1][0], e[1][1], e[1][2], e[1][3]],
                        # print(tmp)
                        new_cri = calculate_crit(tmp)
                        if new_cri <= cri:
                            cri = new_cri
                            end.remove(e)
                            second_end.append(seq.iloc[i+m])
                            sec_inx.append(seq.index[i+m])
                            seq = tmp
                            break
                break

    for e in end:
        cri += e[1][3]
    for e in second_end:
        cri += e[3]
    # print('end:', len(end))
    print(cri)
    print(' '.join([str(s + 1) for s in seq.index]), ' '.join([str(s[0] + 1) for s in end]), ' '.join([str(s + 1) for s in sec_inx]))
    # tasks = []
    # with open(path, 'r') as r:
    #     line = r.readline().split(' ')
    #     n = int(line[0])
    #     for i in range(n):
    #         line = r.readline().split(' ')
    #         tasks.append((int(line[0]), int(line[1]), int(line[2]), int(line[3])))
