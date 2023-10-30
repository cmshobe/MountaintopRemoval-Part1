########################################################################
#This script generates Figure 11 in the following manuscript:

#Shobe, C.M., Bower, S.J., Maxwell, A.E., Glade, R.C., and Samassi, N.M. (2023) The 
#uncertain future of mountaintop-removal-mined landscapes 1: How mining changes erosion 
#processes and variables. Geomorphology.

#Please cite the paper if you use this code in any way.

#Brief description: this script lays out a conceptual model for changes to land-surface
#erodibility driven by mountaintop removal coal mining, and plots different erodibility
#`recovery curves' based on different hypothetical vegetation regrowth efficiencies.`

########################################################################


import numpy as np 
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams.update({'font.size': 22})

time = np.arange(0,1.01,.01)
erodibility = 1
linewidth = 5

fig, (axs) = plt.subplots(figsize=(18, 5.5), ncols = 3)
ax0 = axs[0]
ax1 = axs[1]
ax2 = axs[2]

#erodibility reaches higher eq
dash = np.zeros(len(time))
dash += 1.5
erode1 = 1.5+1.5*np.exp(-5*time)
erode2 = 1.5+1.5*np.exp(-8*time)
erode3 = 1.5+1.5*np.exp(-15*time)
ax0.plot(time, erode1,'sienna',linestyle='dotted', linewidth = linewidth, label = 'Low')
ax0.plot(time,erode2,'olive',linestyle='dashdot', linewidth = linewidth, label = 'Medium')
ax0.plot(time,erode3,'darkgreen', linewidth = linewidth, label = 'High')
ax0.plot(time,dash,'--k', linewidth = linewidth)
ax0.set_xlim(-0.5,1)
ax0.set_ylim(0,3)
h, l = ax0.get_legend_handles_labels()
ph = [plt.plot([],marker="", ls="")[0]] # Canvas
handles = ph + h
labels = ["Vegetation regrowth efficiency:"] + l  # Merging labels
leg = ax0.legend(handles, labels, ncol=4, loc = (0.2,1.05))
ax0.set_xticks(np.arange(-0.5, 1.1, 0.1))
ax0.tick_params(labelbottom=False)   
ax0.set_xticks([])
ax0.set_yticks([])
ax0.set_xlabel('Relative time $T$')
ax0.set_ylabel('Relative erodibility $E$')
ax0.axvspan(-0.2, 0, facecolor='grey', alpha=0.5)
ax0.axhline(1,-0.5, 0.195, color = 'k', linewidth = linewidth)
ax0.text(0.85, -0.2, '$T_{eq}$')

for vpack in leg._legend_handle_box.get_children()[:1]:
    for hpack in vpack.get_children():
        hpack.get_children()[0].set_width(0)
        
frame = leg.get_frame()
frame.set_edgecolor('k')


#erodibility reaches original eq
dash = np.zeros(len(time))
dash += 1
erode1 = 1+2*np.exp(-5*time)
erode2 = 1+2*np.exp(-8*time)
erode3 = 1+2*np.exp(-15*time)
ax1.plot(time, erode1,'sienna',linestyle='dotted', linewidth = linewidth)
ax1.plot(time,erode2,'olive',linestyle='dashdot', linewidth = linewidth)
ax1.plot(time,erode3,'darkgreen', linewidth = linewidth)
ax1.plot(time,dash,'--k', linewidth = linewidth)
ax1.set_xlim(-0.5,1)
ax1.set_ylim(0,3)
ax1.set_xticks(np.arange(-0.5, 1.1, 0.1))
ax1.set_xticks([])
ax1.set_yticks([]) 
ax1.set_xlabel('Relative time $T$')
ax1.axvspan(-0.2, 0, facecolor='grey', alpha=0.5)
ax1.axhline(1,-0.5, 0.195, color = 'k', linewidth = linewidth)
ax1.text(0.85, -0.2, '$T_{eq}$')


#erodibility reaches lower eq
dash = np.zeros(len(time))
dash += 0.5
erode1 = 0.5+2.5*np.exp(-5*time)
erode2 = 0.5+2.5*np.exp(-8*time)
erode3 = 0.5+2.5*np.exp(-15*time)
ax2.plot(time, erode1,'sienna',linestyle='dotted', linewidth = linewidth, label = 'Low')
ax2.plot(time,erode2,'olive',linestyle='dashdot', linewidth = linewidth, label = 'Medium')
ax2.plot(time,erode3,'darkgreen', linewidth = linewidth, label = 'High')
ax2.plot(time,dash,'--k', linewidth = linewidth)
ax2.set_xlim(-0.5,1)
ax2.set_ylim(0,3)
ax2.set_xticks(np.arange(-0.5, 1.1, 0.1))
ax2.set_xticks([])
ax2.set_yticks([])
ax2.set_xlabel('Relative time $T$')
ax2.axvspan(-0.2, 0, facecolor='grey', alpha=0.5)
ax2.axhline(1,-0.5, 0.195, color = 'k', linewidth = linewidth)
ax2.text(0.85, -0.2, '$T_{eq}$')


ax0.annotate('$E_{unmined}$',
            xy=(-0.4, 1),  
            xytext=(0.08, 0.15),    # fraction, fraction
            textcoords='figure fraction',
            arrowprops=dict(facecolor='black', shrink=0.05),
            horizontalalignment='left',
            verticalalignment='bottom')

ax0.annotate('$E_{post mining}$',
            xy=(0.2, 1.5),  
            xytext=(0.15, 0.3),    # fraction, fraction
            textcoords='figure fraction',
            arrowprops=dict(facecolor='black', shrink=0.05),
            horizontalalignment='left',
            verticalalignment='bottom')

ax0.text(-0.15, 0.95, 'mining', rotation = 90)
ax0.text(-0.45, 2.7, 'A', fontsize = 30)
ax0.text(0.3, 2.1, 'mining\n' 'increases\n' 'background\n' 'erodibility')

ax1.text(-0.15, 0.95, 'mining', rotation = 90)
ax1.text(-0.45, 2.7, 'B', fontsize = 30)
ax1.text(0.3, 2.1, 'mining does\n' 'not change\n' 'background\n' 'erodibility')

ax2.text(-0.15, 0.95, 'mining', rotation = 90)
ax2.text(-0.45, 2.7, 'C', fontsize = 30)
ax2.text(0.3, 2.1, 'mining\n' 'decreases\n' 'background\n' 'erodibility')

plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.1, 
                    hspace=0.4)
plt.savefig('fig11_veg', dpi=1000, bbox_inches = 'tight')
