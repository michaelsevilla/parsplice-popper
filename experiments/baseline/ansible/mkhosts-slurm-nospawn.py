import sys
import string
import glob
import shutil
import os
import socket
import re
import random


def allocate(nMPISlots,description,parent,nSlots):
    global nodes
    global rank
    global task
    global hfile
    global lfile


    a=[]
    p=True
    while len(nodes)>0:
        if nodes[0][1]>=nSlots:
            nodes[0][1]-= nSlots
            allocated=True
            a=[nodes[0],nMPISlots,description]
            p=False
            if nodes[0][1]<=0:
                nodes.pop(0)
                p=True
            break
        else:
            nodes.pop(0)
            p=True

    if len(a)>0:
        hfile.write(a[0][0]+(":%i\n" % a[1]))
        s=random.randint(1, 1000000000)
        for i in range(a[1]):
            lfile.write("%i %i %i %s %i\n" % (rank,task,parent,a[2],s))
            rank+=1
        task+=1

    return p



random.seed()

for h in glob.glob("hosts*"):
  os.remove(h)

nSlotsPerNode=int(sys.argv[1])
nMPISlotsPerWorker=int(sys.argv[2])
nSlotsPerWorker=int(sys.argv[3])
nWM=int(sys.argv[4])

if len(sys.argv) <5:
    print "mkhosts: nSlotsPerNode nMPISlotsPerWorker nSlotsPerWorker nWorkManagers"

hostname=socket.gethostname()


slurm_nodelist = os.getenv('SLURM_NODELIST', hostname)

print "HOSTNAME: ", hostname
print "NODE LIST: ", slurm_nodelist


sl= re.split('\]|\[',slurm_nodelist)

nodes=[]
if len(sl)>1:
    prefix=sl[0]
    n=re.split(',',sl[1])

    for nn in n:
        #check if this is a range

        if nn.count("-")>0:
            s=re.split('-',nn)
            begin=int(s[0])
            end=int(s[1])
            for i in range(begin,end+1):
                nodes.append([prefix+ ("%04d" % i ),nSlotsPerNode])
        else:
            nodes.append([prefix+nn,nSlotsPerNode])
else:
    nodes.append([slurm_nodelist,nSlotsPerNode])

nNodes=len(nodes)
print "NODES: ",nodes


hfile=open('hosts','w')
lfile=open('layout','w')



rank=0
task=0
splicerRank=rank
allocate(1,"Splicer",-1,1)
allocate(nMPISlotsPerWorker,"Worker",splicerRank,nSlotsPerWorker)
allocate(1,"PersistentDB",-1,1)
allocate(1,"InMemoryDB",-1,1)

if len(nodes)>1:
    nodes.pop(0)



nNodes=len(nodes)
stride=int(nNodes/nWM)
nc=nNodes % nWM
#print stride,nc
j=0
for i in range(nWM):
    wmRank=rank
    np=0
    if i < nc:
        np=1

    allocate(1,"WorkManager",-1,1)
    if len(nodes)>1:
        nodes.pop(0)
    for k in range(stride+np):
        p=False
        while not p==True:
            p=allocate(nMPISlotsPerWorker,"Worker",wmRank,nSlotsPerWorker)








hfile.close()
lfile.close()
sys.exit()
