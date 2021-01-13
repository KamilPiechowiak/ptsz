from p3.properties import EPS
b=enumerate
c=sorted
V=None
p=range
P=max
w=sum
f=abs
t=True
from p3.src.algorithm_api import Algorithm
from p3.src.data_api import Instance,Solution,Schedule
from p3.src.evaluator_api import EvaluatorOutput
class Algorithm136715(Algorithm):
 def run(self,q:Instance)->Solution:
  H=b(q.tasks,start=1)
  l=Schedule(q.no_tasks,[i[0]for i in c(H,key=lambda x:(x[1].due_date+10*x[1].duration[0]+5*x[1].duration[1])/(x[1].weight))])
  return Solution(self.v(q,Solution(0.0,l)).value,l)
 def v(self,q:Instance,output:Solution,time:float=V)->EvaluatorOutput:
  F=0.0
  x=[0 for _ in p(q.no_machines)]
  for I in output.schedule:
   r=q.tasks[I-1]
   x[0]+=r.duration[0]
   x[1]=P(x[0],x[1])+r.duration[1]
   x[2]=P(x[1],x[2])+r.duration[2]
   F+=P(0,x[2]-r.due_date)*r.weight
  F/=w([r.weight for r in q.tasks])
  o=f(F-output.score)<=EPS
  if F!=0:
   o=o or f(F-output.score)/F<=EPS
  return EvaluatorOutput(t,F,time)
