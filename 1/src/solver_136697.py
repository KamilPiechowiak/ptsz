import sys
def solve():
    
    # if len(sys.argv) != 2:
        # print("zla liczba argumentow, podaj tylko plik z instancja")
        # return -1
        
      
    # instance_file = sys.argv[1]
    
    
    # f = open(instance_file, "r")
    n = int(sys.stdin.readline())
    prdw = []
    for idx, line in enumerate(sys.stdin.readlines()):
        prdw.append([idx+1] + (line.strip()).split(" ") + [0]) # + [0,0] to status i kolejnosc
        
    # prdw = []
    # for idx, line in enumerate(f):
  
    # f.close()
    
    if(n != len(prdw)):
        print(f"Niepoprawny plik z instancja n: {n} , len(prdw): {len(prdw)}!")
        return False
        
        
    for i, line in enumerate(prdw):
        prdw[i][0] = int(prdw[i][0])
        prdw[i][1] = int(prdw[i][1])
        prdw[i][2] = int(prdw[i][2])
        prdw[i][3] = int(prdw[i][3])
        prdw[i][4] = int(prdw[i][4])
        
        
   
    in_prdw = sorted(prdw, key = lambda k : k[3]*k[1]/(k[4]+1)) #O(n log (n))
    time = 0
    time_change = 0
    out_prdw = []    
                
    S_wynik = 0            
                
    for i_index, i in enumerate(in_prdw):
        time_change = 0
        if(i[2] <= time and in_prdw[i_index][5] == 0):
            out_prdw.append(i)
            time = time + i[1]
            time_change = 1
            in_prdw[i_index][5] = 1
            if(time > i[3]):
                S_wynik += i[4]
            
        else:
            
            for j_index, j in enumerate(in_prdw):
                if(j[2] <= time and j[0] != i[0] and in_prdw[j_index][5] == 0):
                    out_prdw.append(j)
                    time = time + j[1]
                    time_change = 1
                    in_prdw[j_index][5] = 1
                    if(time > j[3]):
                        S_wynik += j[4]
                    break
            if(time_change == 0 and in_prdw[i_index][5] == 0):
                time = i[2] #wait for ready
                out_prdw.append(i)
                time = time + i[1]
                time_change = 1
                in_prdw[i_index][5] = 1
                if(time > i[3]):
                    S_wynik += i[4]
                
                
    
    
    for element in in_prdw:
        if element not in out_prdw:
            out_prdw.append(element)
            if(element[2] <= time):
                time+=element[1]
                if time>element[3]:
                    S_wynik+=element[4]
            else:
                time = element[1]
                if time>element[3]:
                    S_wynik+=element[4]
            
     
      
    print(f"{S_wynik}", sep='')
    print(" ".join([str(out_prdw[i][0]) for i in range(len(out_prdw))]), end='', sep='')
    
    
solve()

