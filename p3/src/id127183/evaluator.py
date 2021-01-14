from p3.src.data_api import Instance,Solution
from p3.src.evaluator_api import EvaluatorOutput,Evaluator
from p3.properties import EPS
class Evaluator127183(Evaluator):
 def evaluate(self,in_data:Instance,output:Solution,time:float=None)->EvaluatorOutput:
  P=[0,0,0]
  D,F=0,0
  for T in output.schedule:
   O=in_data.tasks[T-1]
   for A,machineMoment in enumerate(P):
    if A==0:
     P[A]+=O.duration[A]
    else:
     w=max(P[A-1],P[A])
     P[A]=w+O.duration[A]
   H=max(P)
   Q=max(0,H-O.due_date)
   D+=Q*O.weight
   F+=O.weight
  D/=F
  C=abs(D-output.score)<=EPS
  E=D
  return EvaluatorOutput(C,E,time)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
