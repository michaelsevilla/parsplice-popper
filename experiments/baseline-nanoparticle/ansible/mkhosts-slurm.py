import sys
import string
import glob
import shutil
import os
import socket
import re


for h in glob.glob("hosts*"):
  os.remove(h)

nSocketsPerNode=int(sys.argv[1])
nWM=int(sys.argv[2])
#nWM=2
#nSocketsPerNode=36

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
                nodes.append(prefix+ ("%04d" % i ))
        else:
            nodes.append(prefix+nn)
else:
    nodes.append(slurm_nodelist)

nNodes=len(nodes)
if nNodes<nWM+2:
    print "INSUFFICIENT ALLOCATION"
    sys.exit()

print "NODES: ",nodes

hfile=open('hosts','w')
#Splicer
#print nodes[0]+":1"
hfile.write(nodes[0]+":1\n")
nodes.pop(0)
#db master
#print nodes[0]+":1"
hfile.write(nodes[0]+":2\n")
nodes.pop(0)

nNodes=len(nodes)

stride=int(nNodes/nWM)
nc=nNodes % nWM

nn=[]

j=0
for i in range(nWM):
    np=0
    if i < nc:
        np=1
    nnn=[]
    for k in range(stride+np):
        nnn.append(nodes[j])
        j+=1

    nn.append(nnn)
    #print nnn,nn

#print nn, nodes


for i in range(nWM):
    #print nn[i][0]+":1"
    hfile.write(nn[i][0]+":1\n")

    hfile2=open('hosts.'+str(i+1),'w')
    hfile2.write(nn[i][0]+" "+str(nSocketsPerNode-1)+"\n")
    for k in range(1,len(nn[i])):
        hfile2.write(nn[i][k]+" "+str(nSocketsPerNode)+"\n")
    hfile2.close()

hfile.close()
sys.exit()
