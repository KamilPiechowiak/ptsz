from itertools import takewhile as lxpDwtEkCfBQUiO
lxpDwtEkCfBQUie=float
lxpDwtEkCfBQUHi=int
lxpDwtEkCfBQUHN=min
lxpDwtEkCfBQUHM=len
lxpDwtEkCfBQUHo=max
lxpDwtEkCfBQUHs=range
lxpDwtEkCfBQUHg=enumerate
lxpDwtEkCfBQUHj=list
from typing import NamedTuple
from numpy import average
from p2.src.algorithm_api import Algorithm
from p2.src.data_api import Instance,Solution,Schedule,Task
lxpDwtEkCfBQUiH=1
lxpDwtEkCfBQUiN=0
lxpDwtEkCfBQUiM=3
lxpDwtEkCfBQUio=1.5
lxpDwtEkCfBQUis=0
class lxpDwtEkCfBQUiu(NamedTuple):
 lxpDwtEkCfBQUig:lxpDwtEkCfBQUie
 lxpDwtEkCfBQUiv:lxpDwtEkCfBQUie
 index:lxpDwtEkCfBQUHi
def lxpDwtEkCfBQUib(lxpDwtEkCfBQUiL):
 return lxpDwtEkCfBQUiL.lxpDwtEkCfBQUig
def lxpDwtEkCfBQUiF(lxpDwtEkCfBQUid):
 return lxpDwtEkCfBQUid[lxpDwtEkCfBQUiH].duration
def lxpDwtEkCfBQUiR(lxpDwtEkCfBQUid:Task):
 return lxpDwtEkCfBQUid.ready
def lxpDwtEkCfBQUiX(lxpDwtEkCfBQUij,lxpDwtEkCfBQUiA,lxpDwtEkCfBQUic,lxpDwtEkCfBQUiT,lxpDwtEkCfBQUiq,enumerated,lxpDwtEkCfBQUir):
 lxpDwtEkCfBQUij.sort(key=lxpDwtEkCfBQUib)
 lxpDwtEkCfBQUiA.sort(key=lxpDwtEkCfBQUiF)
 lxpDwtEkCfBQUiz=lxpDwtEkCfBQUHN(lxpDwtEkCfBQUiT,key=lambda m:m.lxpDwtEkCfBQUig)
 lxpDwtEkCfBQUih=lxpDwtEkCfBQUHN(lxpDwtEkCfBQUij,key=lambda m:m.lxpDwtEkCfBQUig)
 for lxpDwtEkCfBQUiL in lxpDwtEkCfBQUij:
  if lxpDwtEkCfBQUHM(lxpDwtEkCfBQUiA)>0:
   if lxpDwtEkCfBQUiz.lxpDwtEkCfBQUiv>lxpDwtEkCfBQUir and lxpDwtEkCfBQUiz.lxpDwtEkCfBQUiv<lxpDwtEkCfBQUir+lxpDwtEkCfBQUiM and lxpDwtEkCfBQUih.lxpDwtEkCfBQUig>lxpDwtEkCfBQUio and lxpDwtEkCfBQUHo(lxpDwtEkCfBQUiA,key=lambda t:t[lxpDwtEkCfBQUiH].duration)[lxpDwtEkCfBQUiH].duration>1.1*lxpDwtEkCfBQUis and lxpDwtEkCfBQUih.lxpDwtEkCfBQUig*lxpDwtEkCfBQUiA[0][lxpDwtEkCfBQUiH].duration-lxpDwtEkCfBQUiA[0][lxpDwtEkCfBQUiH].ready>lxpDwtEkCfBQUiA[0][lxpDwtEkCfBQUiH].duration+lxpDwtEkCfBQUiM-lxpDwtEkCfBQUiA[0][lxpDwtEkCfBQUiH].ready:
    break
   if lxpDwtEkCfBQUiL.lxpDwtEkCfBQUig<lxpDwtEkCfBQUio:
    lxpDwtEkCfBQUiY=lxpDwtEkCfBQUiA.pop()
   else:
    lxpDwtEkCfBQUiY=lxpDwtEkCfBQUiA.pop(0)
   lxpDwtEkCfBQUiv=lxpDwtEkCfBQUir+lxpDwtEkCfBQUiY[lxpDwtEkCfBQUiH].duration*lxpDwtEkCfBQUiL.lxpDwtEkCfBQUig
   lxpDwtEkCfBQUic.append(lxpDwtEkCfBQUiY[0])
   lxpDwtEkCfBQUiT[lxpDwtEkCfBQUiL.index]=lxpDwtEkCfBQUiT[lxpDwtEkCfBQUiL.index]._replace(lxpDwtEkCfBQUiv=lxpDwtEkCfBQUiv)
   lxpDwtEkCfBQUiq[lxpDwtEkCfBQUiL.index].append(lxpDwtEkCfBQUiY[0])
   enumerated.remove(lxpDwtEkCfBQUiY)
class Algorithm136705(Algorithm):
 def run(self,lxpDwtEkCfBQUiJ:Instance)->Solution:
  global lxpDwtEkCfBQUis
  lxpDwtEkCfBQUir:lxpDwtEkCfBQUie=0
  lxpDwtEkCfBQUic=[]
  lxpDwtEkCfBQUiq=[[]for _ in lxpDwtEkCfBQUHs(lxpDwtEkCfBQUiJ.no_machines)]
  lxpDwtEkCfBQUiT=[lxpDwtEkCfBQUiu(lxpDwtEkCfBQUig,0,i)for i,lxpDwtEkCfBQUig in lxpDwtEkCfBQUHg(lxpDwtEkCfBQUiJ.machine_speeds)]
  lxpDwtEkCfBQUis=average([lxpDwtEkCfBQUid.duration for lxpDwtEkCfBQUid in lxpDwtEkCfBQUiJ.tasks])
  lxpDwtEkCfBQUia=lxpDwtEkCfBQUiJ.tasks
  lxpDwtEkCfBQUia.sort(key=lxpDwtEkCfBQUiR)
  lxpDwtEkCfBQUiK=[[i,val]for i,val in lxpDwtEkCfBQUHg(lxpDwtEkCfBQUia,start=1)]
  while lxpDwtEkCfBQUHM(lxpDwtEkCfBQUic)<lxpDwtEkCfBQUiJ.no_tasks:
   lxpDwtEkCfBQUij=lxpDwtEkCfBQUin(lxpDwtEkCfBQUiT,lxpDwtEkCfBQUir)
   lxpDwtEkCfBQUiA=lxpDwtEkCfBQUiS(lxpDwtEkCfBQUiK,lxpDwtEkCfBQUir)
   if lxpDwtEkCfBQUHM(lxpDwtEkCfBQUij)>0 and lxpDwtEkCfBQUHM(lxpDwtEkCfBQUiA)>0:
    lxpDwtEkCfBQUiX(lxpDwtEkCfBQUij,lxpDwtEkCfBQUiA,lxpDwtEkCfBQUic,lxpDwtEkCfBQUiT,lxpDwtEkCfBQUiq,lxpDwtEkCfBQUiK,lxpDwtEkCfBQUir)
    lxpDwtEkCfBQUir+=1
   elif lxpDwtEkCfBQUHM(lxpDwtEkCfBQUij)==0:
    lxpDwtEkCfBQUir=lxpDwtEkCfBQUHo(lxpDwtEkCfBQUHN(lxpDwtEkCfBQUiT,key=lambda lxpDwtEkCfBQUiL:lxpDwtEkCfBQUiL.lxpDwtEkCfBQUiv).lxpDwtEkCfBQUiv,lxpDwtEkCfBQUir)
   elif lxpDwtEkCfBQUHM(lxpDwtEkCfBQUiA)==0:
    lxpDwtEkCfBQUir=lxpDwtEkCfBQUHN(lxpDwtEkCfBQUiK,key=lambda lxpDwtEkCfBQUid:lxpDwtEkCfBQUid[lxpDwtEkCfBQUiH].ready)[lxpDwtEkCfBQUiH].ready
   else:
    lxpDwtEkCfBQUir+=1
  return lxpDwtEkCfBQUiy(lxpDwtEkCfBQUiJ,lxpDwtEkCfBQUiq)
def lxpDwtEkCfBQUiS(lxpDwtEkCfBQUia,lxpDwtEkCfBQUir:lxpDwtEkCfBQUie):
 return lxpDwtEkCfBQUHj(lxpDwtEkCfBQUiO(lambda lxpDwtEkCfBQUid:lxpDwtEkCfBQUid[lxpDwtEkCfBQUiH].ready<=lxpDwtEkCfBQUir,lxpDwtEkCfBQUia))
def lxpDwtEkCfBQUin(lxpDwtEkCfBQUiT,lxpDwtEkCfBQUir:lxpDwtEkCfBQUie):
 return[lxpDwtEkCfBQUiL for lxpDwtEkCfBQUiL in lxpDwtEkCfBQUiT if lxpDwtEkCfBQUiL.lxpDwtEkCfBQUiv<=lxpDwtEkCfBQUir]
def lxpDwtEkCfBQUiy(lxpDwtEkCfBQUiJ,lxpDwtEkCfBQUiq):
 lxpDwtEkCfBQUiG=0
 for lxpDwtEkCfBQUiW in lxpDwtEkCfBQUHs(lxpDwtEkCfBQUiJ.no_machines):
  lxpDwtEkCfBQUir=0
  for lxpDwtEkCfBQUiI in lxpDwtEkCfBQUiq[lxpDwtEkCfBQUiW]:
   lxpDwtEkCfBQUir+=lxpDwtEkCfBQUHo(lxpDwtEkCfBQUiJ.tasks[lxpDwtEkCfBQUiI-1].ready-lxpDwtEkCfBQUir,0)
   lxpDwtEkCfBQUir+=lxpDwtEkCfBQUiJ.machine_speeds[lxpDwtEkCfBQUiW]*lxpDwtEkCfBQUiJ.tasks[lxpDwtEkCfBQUiI-1].duration
   lxpDwtEkCfBQUiG+=lxpDwtEkCfBQUir-lxpDwtEkCfBQUiJ.tasks[lxpDwtEkCfBQUiI-1].ready
 lxpDwtEkCfBQUiG=lxpDwtEkCfBQUiG/lxpDwtEkCfBQUiJ.no_tasks
 return Solution(lxpDwtEkCfBQUiG,Schedule(lxpDwtEkCfBQUiJ.no_tasks,lxpDwtEkCfBQUiJ.no_machines,lxpDwtEkCfBQUiq))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
