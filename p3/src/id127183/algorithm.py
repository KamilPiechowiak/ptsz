from p3.src.algorithm_api import Algorithm
from p3.src.data_api import Instance,Solution,Schedule
from p3.src.id127183.evaluator import Evaluator127183
class Job:
 def __init__(p,id,W,i,S):
  p.id=id
  p.duration=W
  p.due_date=i
  p.weight=S
class Algorithm127183(Algorithm):
 def H2I(p,jobs):
  J1,J2=[],[]
  for v in jobs:
   p1,p2,p3=v.duration
   if p1<=p2+p3:
    J1.append(v)
   else:
    J2.append(v)
  J1.sort(key=lambda x:(x.duration[0]*float(x.due_date/x.weight)))
  J2.sort(key=lambda x:(x.duration[1]+x.duration[2])*float(x.weight/(x.due_date+0.00000001)),reverse=True)
  return J1,J2
 def run(p,in_data:Instance)->Solution:
  jobs=[Job(counter+1,task.duration,task.due_date,task.weight)for counter,task in enumerate(in_data.tasks)]
  jobs.sort(key=lambda x:(sum(x.duration)*float(x.due_date/x.weight)))
  J=Schedule(in_data.no_tasks,[v.id for v in jobs])
  s=Evaluator127183().evaluate(in_data,Solution(0.0,J)).value
  return Solution(s,J)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
