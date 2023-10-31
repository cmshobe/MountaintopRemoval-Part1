########################################################################
#This script generates Figure 7 in the following manuscript:

#Shobe, C.M., Bower, S.J., Maxwell, A.E., Glade, R.C., and Samassi, N.M. (2023) The 
#uncertain future of mountaintop-removal-mined landscapes 1: How mining changes erosion 
#processes and variables. Geomorphology.

#Please cite the paper if you use this code in any way.

#Brief description: this script generates Figure 7, which documents the distribution
#of closed depression sizes in our five pre- and post-mining study watersheds. Pre- and 
#Post-mining DEMs of these watersheds were clipped from regional DEMs created by Ross et 
#al. (2016), which can be found at 
#https://doi.org/10.6084/m9.figshare.12846764.v1 (pre-mining) and 
#https://doi.org/10.6084/m9.figshare.12846788.v1 (post-mining). Mined extents were
#derived from the dataset of Pericak et al. (2018; https://skytruth.org/mountaintop-mining/).
#Depressions were identified using the PriorityFlood algorithm 
#(https://richdem.readthedocs.io/en/latest/flow_metrics.html; Barnes, 2017) in Landlab 
#(https://landlab.readthedocs.io/en/master/; Barnhart et al., 2020).

########################################################################

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.gridspec import GridSpec

#thresholds: if >90% of a given depression is mapped as mined, we call it "mined."
#if <10% of a depression has been mined, we call it "unmined."
mined_threshold = 0.9
unmined_threshold = 0.1

#import DEMs
ben_pre_topo = np.genfromtxt("input_dems/bencreek/bencreek_pre_10m.asc", skip_header = 6)
ben_post_topo = np.genfromtxt("input_dems/bencreek/bencreek_post_10m.asc", skip_header = 6)
laurel_pre_topo = np.genfromtxt("input_dems/laurelcreek/laurelcreek_pre_10m.asc", skip_header = 6)
laurel_post_topo = np.genfromtxt("input_dems/laurelcreek/laurelcreek_post_10m.asc", skip_header = 6)
mud_pre_topo = np.genfromtxt("input_dems/mudriver/mudriver_pre_10m.asc", skip_header = 6)
mud_post_topo = np.genfromtxt("input_dems/mudriver/mudriver_post_10m.asc", skip_header = 6)
spruce_pre_topo = np.genfromtxt("input_dems/sprucefork/sprucefork_pre_10m.asc", skip_header = 6)
spruce_post_topo = np.genfromtxt("input_dems/sprucefork/sprucefork_post_10m.asc", skip_header = 6)
white_pre_topo = np.genfromtxt("input_dems/whiteoak/whiteoak_pre_10m.asc", skip_header = 6)
white_post_topo = np.genfromtxt("input_dems/whiteoak/whiteoak_post_10m.asc", skip_header = 6)

#calculate the xxth percentile of pre-mining elevation for each basin. This will be used 
#to mask out closed depressions that fall low in the landscape because they are in
#river valleys which are 1) unmined and 2) very subject to DEM errors that generate sinks.

percentile = 20
ben_elev_threshold = np.percentile(ben_pre_topo[ben_pre_topo > 0], percentile)
laurel_elev_threshold = np.percentile(laurel_pre_topo[laurel_pre_topo > 0], percentile)
mud_elev_threshold = np.percentile(mud_pre_topo[mud_pre_topo > 0], percentile)
spruce_elev_threshold = np.percentile(spruce_pre_topo[spruce_pre_topo > 0], percentile)
white_elev_threshold = np.percentile(white_pre_topo[white_pre_topo > 0], percentile)

#import dataset of closed depressions with proportion mined and average elevation;
#these data derive from flow routing ('see depression_identification.py') and have had
#proportion mined, depression mean elevation, and depression filled surface elevation 
#data added by using the zonal statistics tool in QGIS.
ben_pre = pd.read_csv('bencreek_pre_depressions_prop_mined_elev_filled.csv')
ben_post = pd.read_csv('bencreek_post_depressions_prop_mined_elev_filled.csv')
laurel_pre = pd.read_csv('laurelcreek_pre_depressions_prop_mined_elev_filled.csv')
laurel_post = pd.read_csv('laurelcreek_post_depressions_prop_mined_elev_filled.csv')
mud_pre = pd.read_csv('mudriver_pre_depressions_prop_mined_elev_filled.csv')
mud_post = pd.read_csv('mudriver_post_depressions_prop_mined_elev_filled.csv')
spruce_pre = pd.read_csv('sprucefork_pre_depressions_prop_mined_elev_filled.csv')
spruce_post = pd.read_csv('sprucefork_post_depressions_prop_mined_elev_filled.csv')
white_pre = pd.read_csv('whiteoak_pre_depressions_prop_mined_elev_filled.csv')
white_post = pd.read_csv('whiteoak_post_depressions_prop_mined_elev_filled.csv')

#generate Figure 7
fig = plt.figure(figsize=(8,10))

gs = GridSpec(5, 2, width_ratios=[1, 1], height_ratios=[1, 1, 1, 1, 1])
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1], sharex = ax1, sharey = ax1)
ax3 = fig.add_subplot(gs[2], sharex = ax1, sharey = ax1)
ax4 = fig.add_subplot(gs[3], sharex = ax1, sharey = ax1)
ax5 = fig.add_subplot(gs[4], sharex = ax1, sharey = ax1)
ax6 = fig.add_subplot(gs[5], sharex = ax1, sharey = ax1)
ax7 = fig.add_subplot(gs[6], sharex = ax1, sharey = ax1)
ax8 = fig.add_subplot(gs[7], sharex = ax1, sharey = ax1)
ax9 = fig.add_subplot(gs[8], sharex = ax1, sharey = ax1)
ax10 = fig.add_subplot(gs[9], sharex = ax1, sharey = ax1)

#plot 1: ben creek, mined areas
bins = np.logspace(2, 6, num=20)
ax1.hist(ben_post['area (m^2)'][ben_post['prop_of_sink_minedmean'] >= mined_threshold][ben_post['_ELEVmean'] > ben_elev_threshold], bins, histtype='stepfilled', color = '#fc8d62', alpha = 0.5, label = 'Post-mining DEM')
ax1.hist(ben_post['area (m^2)'][ben_post['prop_of_sink_minedmean'] >= mined_threshold][ben_post['_ELEVmean'] > ben_elev_threshold], bins, histtype='step', color = '#fc8d62', linewidth = 2)
ax1.hist(ben_pre['area (m^2)'][ben_pre['prop_of_sink_minedmean'] >= mined_threshold][ben_pre['_ELEVmean'] > ben_elev_threshold], bins, histtype='stepfilled', color = '#8da0cb', alpha = 0.5, label = 'Pre-mining DEM')
ax1.hist(ben_pre['area (m^2)'][ben_pre['prop_of_sink_minedmean'] >= mined_threshold][ben_pre['_ELEVmean'] > ben_elev_threshold], bins, histtype='step', color = '#8da0cb', linewidth = 2)

ax1.set_xlim(90, 1e6)
ax1.set_ylim(0.5, 5e3)

ax1.set_xscale('log')
ax1.set_yscale('log')

#plot 2: ben creek, unmined areas
bins = np.logspace(2, 6, num=20)
ax2.hist(ben_post['area (m^2)'][ben_post['prop_of_sink_minedmean'] < unmined_threshold][ben_post['_ELEVmean'] > ben_elev_threshold], bins, histtype='stepfilled', color = '#fc8d62', alpha = 0.5, label = 'Post-mining DEM')
ax2.hist(ben_post['area (m^2)'][ben_post['prop_of_sink_minedmean'] < unmined_threshold][ben_post['_ELEVmean'] > ben_elev_threshold], bins, histtype='step', color = '#fc8d62', linewidth = 2)
ax2.hist(ben_pre['area (m^2)'][ben_pre['prop_of_sink_minedmean'] < unmined_threshold][ben_pre['_ELEVmean'] > ben_elev_threshold], bins, histtype='stepfilled', color = '#8da0cb', alpha = 0.5, label = 'Pre-mining DEM')
ax2.hist(ben_pre['area (m^2)'][ben_pre['prop_of_sink_minedmean'] < unmined_threshold][ben_pre['_ELEVmean'] > ben_elev_threshold], bins, histtype='step', color = '#8da0cb', linewidth = 2)
ax2.set_xscale('log')
ax2.set_yscale('log')

#plot 3: laurel creek, mined areas
bins = np.logspace(2, 6, num=20)
ax3.hist(laurel_post['area (m^2)'][laurel_post['prop_of_sink_minedmean'] >= mined_threshold][laurel_post['_ELEVmean'] > laurel_elev_threshold], bins, histtype='stepfilled', color = '#fc8d62', alpha = 0.5, label = 'Post-mining DEM')
ax3.hist(laurel_post['area (m^2)'][laurel_post['prop_of_sink_minedmean'] >= mined_threshold][laurel_post['_ELEVmean'] > laurel_elev_threshold], bins, histtype='step', color = '#fc8d62', linewidth = 2)
ax3.hist(laurel_pre['area (m^2)'][laurel_pre['prop_of_sink_minedmean'] >= mined_threshold][laurel_pre['_ELEVmean'] > laurel_elev_threshold], bins, histtype='stepfilled', color = '#8da0cb', alpha = 0.5, label = 'Pre-mining DEM')
ax3.hist(laurel_pre['area (m^2)'][laurel_pre['prop_of_sink_minedmean'] >= mined_threshold][laurel_pre['_ELEVmean'] > laurel_elev_threshold], bins, histtype='step', color = '#8da0cb', linewidth = 2)
ax3.set_xscale('log')
ax3.set_yscale('log')

ax3.legend()


#plot 4: laurel creek, unmined areas
bins = np.logspace(2, 6, num=20)
ax4.hist(laurel_post['area (m^2)'][laurel_post['prop_of_sink_minedmean'] < unmined_threshold][laurel_post['_ELEVmean'] > laurel_elev_threshold], bins, histtype='stepfilled', color = '#fc8d62', alpha = 0.5)
ax4.hist(laurel_post['area (m^2)'][laurel_post['prop_of_sink_minedmean'] < unmined_threshold][laurel_post['_ELEVmean'] > laurel_elev_threshold], bins, histtype='step', color = '#fc8d62', linewidth = 2)
ax4.hist(laurel_pre['area (m^2)'][laurel_pre['prop_of_sink_minedmean'] < unmined_threshold][laurel_pre['_ELEVmean'] > laurel_elev_threshold], bins, histtype='stepfilled', color = '#8da0cb', alpha = 0.5)
ax4.hist(laurel_pre['area (m^2)'][laurel_pre['prop_of_sink_minedmean'] < unmined_threshold][laurel_pre['_ELEVmean'] > laurel_elev_threshold], bins, histtype='step', color = '#8da0cb', linewidth = 2)
ax4.set_xscale('log')
ax4.set_yscale('log')

#plot 5: mud river, mined areas
bins = np.logspace(2, 6, num=20)
ax5.hist(mud_post['area (m^2)'][mud_post['prop_of_sink_minedmean'] >= mined_threshold][mud_post['_ELEVmean'] > mud_elev_threshold], bins, histtype='stepfilled', color = '#fc8d62', alpha = 0.5)
ax5.hist(mud_post['area (m^2)'][mud_post['prop_of_sink_minedmean'] >= mined_threshold][mud_post['_ELEVmean'] > mud_elev_threshold], bins, histtype='step', color = '#fc8d62', linewidth = 2)
ax5.hist(mud_pre['area (m^2)'][mud_pre['prop_of_sink_minedmean'] >= mined_threshold][mud_pre['_ELEVmean'] > mud_elev_threshold], bins, histtype='stepfilled', color = '#8da0cb', alpha = 0.5)
ax5.hist(mud_pre['area (m^2)'][mud_pre['prop_of_sink_minedmean'] >= mined_threshold][mud_pre['_ELEVmean'] > mud_elev_threshold], bins, histtype='step', color = '#8da0cb', linewidth = 2)
ax5.set_xscale('log')
ax5.set_yscale('log')

#plot 6: mud river, unmined areas
bins = np.logspace(2, 6, num=20)
ax6.hist(mud_post['area (m^2)'][mud_post['prop_of_sink_minedmean'] < unmined_threshold][mud_post['_ELEVmean'] > mud_elev_threshold], bins, histtype='stepfilled', color = '#fc8d62', alpha = 0.5)
ax6.hist(mud_post['area (m^2)'][mud_post['prop_of_sink_minedmean'] < unmined_threshold][mud_post['_ELEVmean'] > mud_elev_threshold], bins, histtype='step', color = '#fc8d62', linewidth = 2)
ax6.hist(mud_pre['area (m^2)'][mud_pre['prop_of_sink_minedmean'] < unmined_threshold][mud_pre['_ELEVmean'] > mud_elev_threshold], bins, histtype='stepfilled', color = '#8da0cb', alpha = 0.5)
ax6.hist(mud_pre['area (m^2)'][mud_pre['prop_of_sink_minedmean'] < unmined_threshold][mud_pre['_ELEVmean'] > mud_elev_threshold], bins, histtype='step', color = '#8da0cb', linewidth = 2)
ax6.set_xscale('log')
ax6.set_yscale('log')

#plot 7: spruce fork, mined areas
bins = np.logspace(2, 6, num=20)
ax7.hist(spruce_post['area (m^2)'][spruce_post['prop_of_sink_minedmean'] >= mined_threshold][spruce_post['_ELEVmean'] > spruce_elev_threshold], bins, histtype='stepfilled', color = '#fc8d62', alpha = 0.5)
ax7.hist(spruce_post['area (m^2)'][spruce_post['prop_of_sink_minedmean'] >= mined_threshold][spruce_post['_ELEVmean'] > spruce_elev_threshold], bins, histtype='step', color = '#fc8d62', linewidth = 2)
ax7.hist(spruce_pre['area (m^2)'][spruce_pre['prop_of_sink_minedmean'] >= mined_threshold][spruce_pre['_ELEVmean'] > spruce_elev_threshold], bins, histtype='stepfilled', color = '#8da0cb', alpha = 0.5)
ax7.hist(spruce_pre['area (m^2)'][spruce_pre['prop_of_sink_minedmean'] >= mined_threshold][spruce_pre['_ELEVmean'] > spruce_elev_threshold], bins, histtype='step', color = '#8da0cb', linewidth = 2)

ax7.set_xscale('log')
ax7.set_yscale('log')

#plot 8: spruce fork, unmined areas
bins = np.logspace(2, 6, num=20)
ax8.hist(spruce_post['area (m^2)'][spruce_post['prop_of_sink_minedmean'] < unmined_threshold][spruce_post['_ELEVmean'] > spruce_elev_threshold], bins, histtype='stepfilled', color = '#fc8d62', alpha = 0.5)
ax8.hist(spruce_post['area (m^2)'][spruce_post['prop_of_sink_minedmean'] < unmined_threshold][spruce_post['_ELEVmean'] > spruce_elev_threshold], bins, histtype='step', color = '#fc8d62', linewidth = 2)
ax8.hist(spruce_pre['area (m^2)'][spruce_pre['prop_of_sink_minedmean'] < unmined_threshold][spruce_pre['_ELEVmean'] > spruce_elev_threshold], bins, histtype='stepfilled', color = '#8da0cb', alpha = 0.5)
ax8.hist(spruce_pre['area (m^2)'][spruce_pre['prop_of_sink_minedmean'] < unmined_threshold][spruce_pre['_ELEVmean'] > spruce_elev_threshold], bins, histtype='step', color = '#8da0cb', linewidth = 2)
ax8.set_xscale('log')
ax8.set_yscale('log')

#plot 9: white oak, mined areas
bins = np.logspace(2, 6, num=20)
ax9.hist(white_post['area (m^2)'][white_post['prop_of_sink_minedmean'] >= mined_threshold][white_post['_ELEVmean'] > white_elev_threshold], bins, histtype='stepfilled', color = '#fc8d62', alpha = 0.5)
ax9.hist(white_post['area (m^2)'][white_post['prop_of_sink_minedmean'] >= mined_threshold][white_post['_ELEVmean'] > white_elev_threshold], bins, histtype='step', color = '#fc8d62', linewidth = 2)
ax9.hist(white_pre['area (m^2)'][white_pre['prop_of_sink_minedmean'] >= mined_threshold][white_pre['_ELEVmean'] > white_elev_threshold], bins, histtype='stepfilled', color = '#8da0cb', alpha = 0.5)
ax9.hist(white_pre['area (m^2)'][white_pre['prop_of_sink_minedmean'] >= mined_threshold][white_pre['_ELEVmean'] > white_elev_threshold], bins, histtype='step', color = '#8da0cb', linewidth = 2)

ax9.set_xscale('log')
ax9.set_yscale('log')

#plot 10: white oak, unmined areas
bins = np.logspace(2, 6, num=20)
ax10.hist(white_post['area (m^2)'][white_post['prop_of_sink_minedmean'] < unmined_threshold][white_post['_ELEVmean'] > white_elev_threshold], bins, histtype='stepfilled', color = '#fc8d62', alpha = 0.5)
ax10.hist(white_post['area (m^2)'][white_post['prop_of_sink_minedmean'] < unmined_threshold][white_post['_ELEVmean'] > white_elev_threshold], bins, histtype='step', color = '#fc8d62', linewidth = 2)
ax10.hist(white_pre['area (m^2)'][white_pre['prop_of_sink_minedmean'] < unmined_threshold][white_pre['_ELEVmean'] > white_elev_threshold], bins, histtype='stepfilled', color = '#8da0cb', alpha = 0.5)
ax10.hist(white_pre['area (m^2)'][white_pre['prop_of_sink_minedmean'] < unmined_threshold][white_pre['_ELEVmean'] > white_elev_threshold], bins, histtype='step', color = '#8da0cb', linewidth = 2)
ax10.set_xscale('log')
ax10.set_yscale('log')

#hide extra x-axes
ax1.get_xaxis().set_visible(False)
ax2.get_xaxis().set_visible(False)
ax3.get_xaxis().set_visible(False)
ax4.get_xaxis().set_visible(False)
ax5.get_xaxis().set_visible(False)
ax6.get_xaxis().set_visible(False)
ax7.get_xaxis().set_visible(False)
ax8.get_xaxis().set_visible(False)

#hide extra y-axes
ax2.get_yaxis().set_visible(False)
ax4.get_yaxis().set_visible(False)
ax6.get_yaxis().set_visible(False)
ax8.get_yaxis().set_visible(False)
ax10.get_yaxis().set_visible(False)

#titles
ax1.set_title('Depressions $\geq$90% mined')
ax2.set_title('Depressions <10% mined')

#xlabels
ax9.set_xlabel('Depression area [m$^2$]')
ax10.set_xlabel('Depression area [m$^2$]')

#ylabels
ax1.set_ylabel('Count')
ax3.set_ylabel('Count')
ax5.set_ylabel('Count')
ax7.set_ylabel('Count')
ax9.set_ylabel('Count')

#label the plots
ax1.text(100, 2500, 'Ben Creek')
ax2.text(100, 2500, 'Ben Creek')
ax3.text(100, 2500, 'Laurel Creek')
ax4.text(100, 2500, 'Laurel Creek')
ax5.text(100, 2500, 'Mud River')
ax6.text(100, 2500, 'Mud River')
ax7.text(100, 2500, 'Spruce Fork')
ax8.text(100, 2500, 'Spruce Fork')
ax9.text(100, 2500, 'White Oak Creek')
ax10.text(100, 2500, 'White Oak Creek')

#annotate
ax1.annotate('mining creates\n' 'large closed\n' 'depressions',
            xy=(2e4, 2.1),  
            xytext=(0.33, 0.86),    # fraction, fraction
            textcoords='figure fraction',
            arrowprops=dict(facecolor='black', shrink=0.05),
            horizontalalignment='left',
            verticalalignment='bottom')

ax2.annotate('no new large\n' 'depressions in\n' 'unmined areas',
            xy=(1.5e4, 2.1),  
            xytext=(0.8, 0.86),    # fraction, fraction
            textcoords='figure fraction',
            arrowprops=dict(facecolor='black', shrink=0.05),
            horizontalalignment='left',
            verticalalignment='bottom')


fig.tight_layout()
fig.savefig('fig7_depressions_rev1.png', dpi=1000, bbox_inches='tight')