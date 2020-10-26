#!/usr/bin/env python3
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import rc
line = [0,1]
depth = 5
cmap = plt.get_cmap('gnuplot_r',depth+1)

##Set some plotting variables in matplotlib, for the colourmap
norm = mpl.colors.Normalize(vmin=0,vmax=depth)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
def divide(line, level=0):
    plt.plot(line,[level,level], color=cmap(level), lw=5, solid_capstyle="butt")
    if level < depth:
        s = np.linspace(line[0],line[1],4)
        divide(s[:2], level+1)
        divide(s[2:], level+1)
divide(line)
plt.gca().invert_yaxis()
cax=plt.colorbar(sm, ticks=range(0,depth+1),boundaries=np.arange(-0.5,depth+1.5,1))
cax.ax.invert_yaxis()
plt.savefig('cantor.eps', interpolation='none')
plt.close()