import heapq as heapq
a=range
d=len
I=max
V=abs
R=sum
g=min
s=map
e=id
q=heapq.heappop
q=heapq.heappop
J=heapq.heappush
J=heapq.heappush
from sortedcontainers import SortedSet
from p3.src.id136775.evaluator import Evaluator136775
from p3.src.algorithm_api import Algorithm as Algorithm
from p3.src.data_api import Instance as T,Solution as SS,Schedule as Schedule
from p3.src.data_api import Task
class Algorithm136775(Algorithm):
 def v(self,Y,task):
  f,F,Q=task.duration,task.due_date,task.weight
  t0=Y[0]
  G=0
  for i in a(d(Y)):
   t=Y[i]
   p=f[i]
   t0=I(t0,t)+p
   if i<d(Y)-1:
    G+=V(t0-t)
  return F-t0,G
 def run(self,in_data):
  n,m=in_data.no_tasks,in_data.no_machines
  l=in_data.tasks
  r=[]
  N=[]
  A=SortedSet(a(n),key=lambda idx:-l[idx].due_date)
  Y=[0 for _ in a(m)]
  for _ in a(n):
   while d(A)>0 and Y[2]>=l[A[-1]].due_date:
    S=A.pop()
    L=l[S]
    J(N,(-L.weight/R(L.duration),S))
   if d(N)==0:
    O=g(s(lambda task_id:(self.v(Y,l[task_id]),task_id),A))
    H=O[1]
    A.remove(H)
   else:
    _,H=q(N)
   L=l[H]
   r.append(H)
   p=0
   for n in a(m):
    Y[n]=I(Y[n],p)+L.duration[n]
    p=Y[n]
  r=[e+1 for e in r]
  U=Schedule(in_data.no_tasks,r)
  y=Evaluator136775().score(in_data,U)
  return SS(score=y,schedule=U)

# Created by pyminifier (https://github.com/liftoff/pyminifier)

