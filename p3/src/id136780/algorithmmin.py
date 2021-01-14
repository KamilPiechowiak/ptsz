R=max
Q=sum
J=len
B=range
from p3.src.algorithm_api import Algorithm as A
from p3.src.data_api import Instance,Solution as M,Schedule as N,Task
from p3.src.id136780.utils import compute_loss as O
import numpy as F,heapq as P
I=0.08
class U:
	def r(W,ind):
		E=ind;S,I=E.no_tasks,E.no_machines;A=E.tasks;C=[];K=[];D=list(B(S));D.sort(key=lambda idx:-A[idx].due_date);F=[0 for A in B(I)]
		for V in B(S):
			while J(D)>0 and F[2]>=A[D[-1]].due_date:T=D.pop();G=A[T];P.heappush(K,(-G.weight/Q(G.duration),T))
			if J(K)==0:L=D.pop()
			else:V,L=P.heappop(K)
			G=A[L];C.append(L);U=0
			for H in B(I):F[H]=R(F[H],U)+G.duration[H];U=F[H]
		C=[A+1 for A in C];return M(score=O(C,A,I),schedule=N(E.no_tasks,C))
	def s(C,ind,solution):A=solution;B=C.r(ind);return B if False else A
class C136780(A):
	def get_partial_loss(K,tasks,t,w_sum):
		G=tasks;A=t.copy();H=0.0
		for C in G:
			D=0
			for E in B(J(A)):A[E]=R(A[E],D)+C.duration[E];D=A[E]
			if D>C.due_date:H+=(D-C.due_date)*C.weight
		return H+I*(w_sum-G[0].weight-G[1].weight)*F.max(F.array(A)-F.array(t))
	def first_wins(A,a,b,tasks,w_sum,t):C=w_sum;B=tasks;D,E=B[a],B[b];return A.get_partial_loss([D,E],t,C)<A.get_partial_loss([E,D],t,C)
	def run(V,in_data):
		D=in_data;L,K=D.no_tasks,D.no_machines;C=D.tasks;E=[];F=[A for A in B(L)];G=[0 for A in B(K)];P=Q([A.weight for A in C]);F.sort(key=lambda idx:C[idx].weight/Q(C[idx].duration))
		for W in B(L):
			X=J(F);H=[]
			for A in F:
				if G[2]>=C[A].due_date:H.append(A)
			if J(H)==0:H=F
			I=H[0]
			for A in H[1:]:
				if V.first_wins(I,A,C,P,G)==False:I=A
			S=C[I];E.append(I);F.remove(I);P-=S.weight;T=0
			for A in B(K):G[A]=R(G[A],T)+S.duration[A];T=G[A]
		E=[A+1 for A in E];return U().s(D,M(score=O(E,C,K),schedule=N(D.no_tasks,E)))