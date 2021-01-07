S=len
H=range
from p3.src.algorithm_api import Algorithm as A
from p3.src.data_api import Instance,Solution as P,Schedule as Q,Task
from p3.src.id136780.utils import compute_loss as R
import numpy as B,heapq as L
class C136780(A):
	def run(U,in_data):
		D=in_data;M,I=D.no_tasks,D.no_machines;A=D.tasks;B=[];J=[];C=list(H(M));C.sort(key=lambda idx:-A[idx].due_date);E=[0 for A in H(I)]
		for T in H(M):
			while S(C)>0 and E[2]>=A[C[-1]].due_date:N=C.pop();F=A[N];L.heappush(J,(-F.weight/sum(F.duration),N))
			if S(J)==0:K=C.pop()
			else:T,K=L.heappop(J)
			F=A[K];B.append(K);O=0
			for G in H(I):E[G]=max(E[G],O)+F.duration[G];O=E[G]
		B=[A+1 for A in B];return P(score=R(B,A,I),schedule=Q(D.no_tasks,B))