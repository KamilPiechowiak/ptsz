from p2.src.algorithm_api import Algorithm
from p2.src.data_api import Instance,Solution,Schedule
from p2.src.id136780.utils import Task,compute_loss,read_instance
import heapq,sys
class Algorithm136780(Algorithm):
	INF=1e+18
	class Machine:
		def __init__(A,b):A.t,A.next_i,A.queue,A.b=0,0,[],b
	@staticmethod
	def minimal_expected_loss_first(tasks,b):
		E=tasks;D=len(E);F=[Algorithm136780.Machine(A)for A in b];I=[0]*D;J=[[]for A in b];K=D;L=0
		for A in F:L+=1/A.b
		for Q in range(D):
			C,M,G=-1,0,-1
			for H in range(D):
				if I[H]!=0:continue
				B=E[H]
				for (O,A) in enumerate(F):
					P=(K-1)/L/A.b;N=max(A.t,B.r)+B.p*A.b+0.06*max(0,B.r-A.t)*P
					if C==-1 or N<M:C,G,M=H,O,N
			J[G].append(C);I[C]=1;B=E[C];A=F[G];A.t=max(A.t,B.r)+B.p*A.b;K-=1
		return J
	def run(E,in_data):A=in_data;B,C=read_instance(A);D=E.minimal_expected_loss_first(C,B);F=compute_loss(D,C,B);return Solution(score=F,schedule=Schedule(n=A.no_tasks,m=A.no_machines,schedule=[[B+1 for B in A]for A in D]))