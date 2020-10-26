#!/usr/bin/env python3

##import matplotlib for plotting
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import rc
##import numpy for linear algebra
import numpy as np
import math
ext='.eps'



##Couple of property constants. prop1 is the constant about which the triangles are inserted, prop2 is the perpendicular distance from the line for the peak of the triangle
prop1=1/3
prop2=math.sqrt(3)/6

##Set a max iteration for the snowflake
Maxiterations=7


##Get a plotting colourmap
cmap = plt.get_cmap('gnuplot',Maxiterations)


##Create a class object for each line, storing within the points about which to add new triangles
class Line:
    ##Class only needs to create a constructor as that will generate all the points
    def __init__(self,Startpoint,Endpoint,Depth):
        ##Find X and Y distances
        Lx=Endpoint[0]-Startpoint[0]
        Ly=Endpoint[1]-Startpoint[1]
        ##Calculate vector, corresponding to a third of the way up the line
        Dist=[(Lx)*prop1,(Ly)*prop1]
        ##Calculate transpose vector, corresponding to the vector where the point in the iterated fractal lies
        DistT=[-(Ly)*prop2,(Lx)*prop2]
        ##Calculate and store the 5 points as class members for the next iteration of the fractal
        self.stp=Startpoint
        self.edp=Endpoint
        self.p1=[x + y for x, y in zip(Startpoint, Dist)]
        self.p3=[x - y for x, y in zip(Endpoint, Dist)]
        self.p2=[(x + y)*0.5 + z for x, y, z in zip(Startpoint, Endpoint, DistT)]
        ##Depth corresponds to the iteration that the fractal was generated in
        self.colour=Depth

##Function to plot lines out from the list of l
def plot(LineList,ax):
    for Li in LineList:
        ax.plot([Li.stp[0],Li.edp[0]],[Li.stp[1],Li.edp[1]],c=cmap(Li.colour),linewidth=2/(Li.colour+1),solid_capstyle='round')



##Function to update list at each iteration.
def ListUpdate(LSti,i):
    LSt=[]
    for j in LSti:
        LSt.append(Line(j.stp,j.p1,j.colour))
        LSt.append(Line(j.p1,j.p2,i))
        LSt.append(Line(j.p2,j.p3,i))
        LSt.append(Line(j.p3,j.edp,j.colour))
    return LSt


##Create empty list
LSt=[]
##Create the 0th iteration corresponding to an equilateral triangle
LSt.append(Line([0,0],[0,10],0))
LSt.append(Line([0,10],[5*math.sqrt(3),5],0))
LSt.append(Line([5*math.sqrt(3),5],[0,0],0))


##Set some plotting variables in matplotlib, for the colourmap
norm = mpl.colors.Normalize(vmin=0,vmax=Maxiterations)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
##Loop through the iterations
for i in range(0,Maxiterations):
    ##Upadate the linelist if not on the 0th iterartion
    if i !=0:
        LSt=ListUpdate(LSt,i)
    ##Plot figure
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1, adjustable='box', aspect=1)
    ##Call out plot function for the linelist at a particular iteration
    plot(LSt,ax1)
    ax1.set_title(r'Koch Snowflake, Order: %s' %(str(i)))
    ##Turn off axis as an image
    ax1.set_axis_off()
    ##Create colourbar
    cax=plt.colorbar(sm, ticks=range(0,Maxiterations),boundaries=np.arange(-0.5,Maxiterations+0.5,1))
    ##Save figure and close
    plt.savefig('Image_Out/Snowflake_Ord_'+str(i)+ext, interpolation='none')
    plt.close()
