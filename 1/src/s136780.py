#!/usr/bin/env python3
R=' '
P=print
Q=min
C=int
I=max
H=range
E=len
import sys
N=C(1e+18)
class D:
	def __init__(A,p,r,d,w):A.p,A.r,A.d,A.w=p,r,d,w
def F(file):
	B=C(file.readline());A=[]
	for E in H(B):A.append(D(*[C(A)for A in file.readline().split(R)if A!='\n']))
	return A
def G(order,tasks):
	C=0;A=0
	for D in order:
		B=tasks[D];A=I(A,B.r);A+=B.p
		if A>B.d:C+=B.w
	return C
def B(order,tasks):
	D=[];E=[];B=0
	for C in order:
		A=tasks[C]
		if I(B,A.r)+A.p<=A.d:D.append(C);B=I(B,A.r)+A.p
		else:E.append(C)
	return D+E
def J(tasks):A=tasks;D=E(A);C=[A for A in H(D)];C.sort(key=lambda idx:A[idx].r);return B(C,A)
def K(tasks):A=tasks;D=E(A);C=[A for A in H(D)];C.sort(key=lambda idx:A[idx].d);return B(C,A)
def A(tasks,choose_place):
	D=tasks;R=E(D);O=[A for A in H(R)];O.sort(key=lambda idx:-D[idx].w/D[idx].p);A=[];P=[]
	for L in O:
		F=D[L];M=0;C=-1
		for B in H(E(A)+1):
			if B!=E(A):J=A[B]
			else:J=-1,N
			if I(M,F.r)+F.p<=Q(F.d,J[1]):C=choose_place(C,B)
			if J[0]==-1:continue
			G=D[J[0]];M=I(M,G.r)+G.p
		if C!=-1:
			K=F.d
			if C<E(A):K=Q(K,A[C][1])
			K-=F.p;A.insert(C,[L,K]);B=C-1
			while B>=0:
				G=D[A[B][0]]
				if A[B+1][1]-G.p>=A[B][1]:break
				A[B][1]=A[B+1][1]-G.p;B-=1
		else:P.append(L)
	return[B[0]for B in A]+P
def L(tasks):
	def B(chosen_place,i):A=chosen_place;return i if A==-1 else A
	return A(tasks,B)
def M(tasks):
	def B(chosen_place,i):return i
	return A(tasks,B)
def O():
	B=F(sys.stdin);H=[J,K,L,M];C=[];A=N
	for I in H:
		D=I(B);E=G(D,B)
		if E<A:A=E;C=D
	P(A);P(R.join([str(A+1)for A in C]))
if __name__=='__main__':O()