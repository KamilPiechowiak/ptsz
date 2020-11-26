import numpy as B
from p2.src.algorithm_api import Algorithm as A
from p2.src.data_api import Solution as I,Schedule as J
class TestAlgorithm136775(A):
	def run(M,in_data):
		A=in_data;D=B.zeros(A.no_machines);G=[[]for B in range(A.no_machines)];K=B.array(A.machine_speeds);E=0
		for (L,F) in enumerate(A.tasks):H=B.maximum(D,B.full(A.no_machines,F.ready))+F.duration*K;C=B.argmin(H).item();D[C]=H[C];G[C].append(L+1);E+=D[C]-F.ready
		E/=A.no_tasks;return I(schedule=J(schedule=G,m=A.no_machines,n=A.no_tasks),score=E)