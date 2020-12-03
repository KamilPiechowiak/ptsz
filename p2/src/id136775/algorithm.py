import numpy as np
from p2.src.algorithm_api import Algorithm
from p2.src.data_api import Instance,Solution,Schedule,Task
def lmap(f,it):
 return list(map(f,it))
def calc_score(in_data,AjbFt):
 AjbFQ=0
 for i,machine_scheduling in enumerate(AjbFt):
  AjbFB=0
  AjbFX=in_data.machine_speeds[i]
  for AjbFM in machine_scheduling:
   AjbFM=in_data.tasks[AjbFM-1]
   AjbFB=max(AjbFB,AjbFM.ready)+AjbFM.duration*AjbFX
   AjbFQ+=AjbFB-AjbFM.ready
 return AjbFQ/in_data.no_tasks
class Machine:
 def __init__(AjbFo,AjbFy):
  AjbFo.schedule_tasks=[]
  AjbFo.schedule_ids=[]
  AjbFo.speed=AjbFy
  AjbFo.time=0
  AjbFo.previous_time=0
 def swap(AjbFo,AjbFx,AjbFM,AjbFi):
  AjbFo.time+=AjbFx
  AjbFo.schedule_tasks[-1]=AjbFM
  AjbFo.schedule_ids[-1]=AjbFi
 def finish_time(AjbFo,AjbFM:Task):
  return max(AjbFo.time,AjbFM.ready)+(AjbFM.duration*AjbFo.speed)
 def do_schedule(AjbFo,AjbFM:Task,AjbFi:int,finish_time:float):
  AjbFo.previous_time=AjbFo.time
  AjbFo.time=finish_time
  AjbFo.schedule_ids.append(AjbFi)
  AjbFo.schedule_tasks.append(AjbFM)
 def criterium_change_on_swap(AjbFo,AjbFM:Task):
  return max(AjbFo.previous_time,AjbFM.ready)+(AjbFM.duration*AjbFo.speed)-AjbFo.time
AjbFu=(2**31)-1
class Algorithm136775(Algorithm):
 def run(AjbFo,in_data:Instance):
  AjbFa=[Machine(AjbFy)for AjbFy in in_data.machine_speeds]
  AjbFv=sorted(enumerate(in_data.tasks),key=lambda AjbFM:(AjbFM[1].ready,AjbFM[1].duration))
  for AjbFi,AjbFM in AjbFv:
   AjbFD=lmap(lambda machine:machine.finish_time(AjbFM),AjbFa)
   AjbFU=np.argmin(AjbFD).item()
   AjbFa[AjbFU].do_schedule(AjbFM,AjbFi+1,AjbFD[AjbFU])
   AjbFe=AjbFu
   AjbFP=-1
   for i,machine in enumerate(AjbFa):
    if machine.time>AjbFM.ready and i!=AjbFU:
     AjbFx=machine.criterium_change_on_swap(AjbFM)
     AjbFO=AjbFa[AjbFU].criterium_change_on_swap(machine.schedule_tasks[-1])
     AjbFg=AjbFx+AjbFO
     if AjbFe>AjbFg and AjbFg<0:
      AjbFe=AjbFg
      AjbFP=(i,AjbFx,AjbFO)
   if AjbFP!=-1:
    AjbFE,AjbFn=AjbFa[AjbFP[0]].schedule_tasks[-1],AjbFa[AjbFP[0]].schedule_ids[-1]
    AjbFa[AjbFP[0]].swap(AjbFP[1],AjbFa[AjbFU].schedule_tasks[-1],AjbFa[AjbFU].schedule_ids[-1])
    AjbFa[AjbFU].swap(AjbFP[2],AjbFE,AjbFn)
  AjbFt=[machine.schedule_ids for machine in AjbFa]
  AjbFQ=calc_score(in_data,AjbFt)
  return Solution(schedule=Schedule(schedule=AjbFt,m=in_data.no_machines,n=in_data.no_tasks),score=AjbFQ)
# Created by pyminifier (https://github.com/liftoff/pyminifier)

