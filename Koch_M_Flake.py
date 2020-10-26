#!/usr/bin/env python3
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import math
import os
ext='.png'

M_Fmax=7


def plot(LineList,ax):
    for Li in LineList:
        ax.plot([Li.stp[0],Li.edp[0]],[Li.stp[1],Li.edp[1]],c=cmap(Li.colour),linewidth=2/(Li.colour+1),solid_capstyle='round')
        #for i in range(0,4):
            #ax.scatter(x=[Li.p[i][0]],y=[Li.p[i][1]])



def ListUpdate(LSti,i):
    LSt=[]
    for j in LSti:

        for num,k in enumerate(j.p):
            if num == 0:
                LSt.append(Line(j.stp,j.p[0],j.colour))
            else:
                LSt.append(Line(j.p[num-1],k,i))
        LSt.append(Line(j.p[-1],j.edp,j.colour))
    return LSt

##Set a max iteration for the snowflake
Maxiterations=5

for M_F in range(3,M_Fmax+1):
    In_A=2*math.pi/M_F
    c,s=math.cos(In_A),math.sin(In_A)
    c2,s2=math.cos(math.pi-In_A),math.sin(math.pi-In_A)
    R_M=np.array([[c,-s],[s,c]])
    R_M2=np.array([[c2,s2],[-s2,c2]])
    # Get a pllotting colourmap
    cmap = plt.get_cmap('gnuplot',Maxiterations)
    
    
    if not os.path.exists(str(M_F)+'_Flake'):
        os.makedirs(str(M_F)+'_Flake')
    prop1=(M_F-1)/(2*M_F)
    prop2=math.sqrt(3)/6
    class Line:
        def __init__(self,Startpoint,Endpoint,Depth):
            Lx=Endpoint[0]-Startpoint[0]
            Ly=Endpoint[1]-Startpoint[1]
            Dist=np.array([(Lx)*prop1,(Ly)*prop1])
            self.vec=np.array([Lx,Ly])
            self.stp=Startpoint
            self.edp=Endpoint
            len=Endpoint-Startpoint-2*Dist
            self.p=[]
            self.p.append(Startpoint + Dist)
            Rotlen=len
            for i in range(M_F-1):
                Rotlen=np.dot(R_M,Rotlen)
                TD=self.p[i]-Rotlen
                self.p.append(TD)
            self.colour=Depth
    

    
    
    LSt=[]
    
    
    LSt.append(Line(np.array([0,0]),np.array([0,1]),0))
    for i in range(M_F-1):
        p1=LSt[i].edp
        p2=np.dot(R_M,LSt[i].vec)
        LSt.append(Line(p1,p1+p2,0))
    
    ##Set some plotting variables in matplotlib, for the colourmap
    norm = mpl.colors.Normalize(vmin=0,vmax=Maxiterations)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    for i in range(0,Maxiterations):
        if i != 0:
            LSt=ListUpdate(LSt,i)
        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1, adjustable='box', aspect=1)
    
        plot(LSt,ax1)
        ax1.set_title(r'Koch %s_flake, Order: %s' %(str(M_F),str(i)))
        ax1.set_axis_off()
        cax=plt.colorbar(sm, ticks=range(0,Maxiterations),boundaries=np.arange(-0.5,Maxiterations+0.5,1))
        plt.savefig(str(M_F)+'_Flake/'+str(M_F)+'_Flake_ord'+str(i)+ext, interpolation='none')
        plt.close()
        
