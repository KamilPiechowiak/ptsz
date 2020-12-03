# R=max
# Q=range
# P=len
# from p2.src.algorithm_api import Algorithm as A
# from p2.src.data_api import Instance,Solution as E,Schedule as F
# from p2.src.id136780.utils import Task,compute_loss as H,read_instance as I
# import heapq as G
# class O136780(A):
# 	class Machine:
# 		def __init__(A,b):A.t,A.next_i,A.queue,A.b=0,0,[],b
# 	@staticmethod
# 	def f(tasks,b):
# 		C=tasks;H=P(C);I=[A for A in Q(H)];I.sort(key=lambda idx:(C[idx].r,C[idx].p));J=[O136780.Machine(A)for A in b];K=[0]*H;L=[[]for A in b]
# 		for T in Q(H):
# 			E,M,F=-1,0,0
# 			for (S,A) in enumerate(J):
# 				while True:
# 					if P(A.queue)==0:D=I[A.next_i];B=C[D];G.heappush(A.queue,(B.p,D));A.next_i+=1
# 					D=A.queue[0][1]
# 					if K[D]!=0:G.heappop(A.queue);continue
# 					B=C[D];N=R(A.t,B.r)+B.p*A.b
# 					if E==-1 or N<M:E,M,F=S,N,D
# 					break
# 			L[E].append(F);K[F]=1;B=C[F];A=J[E];A.t=R(A.t,B.r)+B.p*A.b;G.heappop(A.queue)
# 		return L
# 	def run(G,in_data):A=in_data;B,C=I(A);D=G.f(C,B);J=H(D,C,B);return E(score=J,schedule=F(n=A.no_tasks,m=A.no_machines,schedule=[[B+1 for B in A]for A in D]))