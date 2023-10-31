########################################################################
#This script generates data for Figures 6-8 in the following manuscript:

#Shobe, C.M., Bower, S.J., Maxwell, A.E., Glade, R.C., and Samassi, N.M. (2023) The 
#uncertain future of mountaintop-removal-mined landscapes 1: How mining changes erosion 
#processes and variables. Geomorphology.

#Please cite the paper if you use this code in any way.

#Brief description: this script generates data for figures that calculate the size, area,
#and volume of closed depressions in pre- and post-mining digital elevation models. We
#completed this analysis for five watersheds: Ben Creek, Laurel Creek, Mud River, 
#Spruce Fork, and White Oak Creek. Pre- and Post-mining DEMs of these watersheds were 
#clipped from regional DEMs created by Ross et al. (2016), which can be found at 
#https://doi.org/10.6084/m9.figshare.12846764.v1 (pre-mining) and 
#https://doi.org/10.6084/m9.figshare.12846788.v1 (post-mining). Flow routing in this 
#script uses the PriorityFlood algorithm 
#(https://richdem.readthedocs.io/en/latest/flow_metrics.html; Barnes, 2017) in Landlab 
#(https://landlab.readthedocs.io/en/master/; Barnhart et al., 2020).

#NOTE: the folder 'flowrouting_output', which holds the results of this analysis, is
#empty in our archived version because the file sizes are too large to archive (total 
#several GB). This script will generate those outputs.

########################################################################

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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

#calculate the volume of each depression by multiplying its area by the difference between
#its mean elevation and its filled elevation
ben_pre['dep_volume'] = ben_pre['area (m^2)'] * (ben_pre['_ELEVFILLEDmean'] - ben_pre['_ELEVmean'])
ben_post['dep_volume'] = ben_post['area (m^2)'] * (ben_post['_ELEVFILLEDmean'] - ben_post['_ELEVmean'])
laurel_pre['dep_volume'] = laurel_pre['area (m^2)'] * (laurel_pre['_ELEVFILLEDmean'] - laurel_pre['_ELEVmean'])
laurel_post['dep_volume'] = laurel_post['area (m^2)'] * (laurel_post['_ELEVFILLEDmean'] - laurel_post['_ELEVmean'])
mud_pre['dep_volume'] = mud_pre['area (m^2)'] * (mud_pre['_ELEVFILLEDmean'] - mud_pre['_ELEVmean'])
mud_post['dep_volume'] = mud_post['area (m^2)'] * (mud_post['_ELEVFILLEDmean'] - mud_post['_ELEVmean'])
spruce_pre['dep_volume'] = spruce_pre['area (m^2)'] * (spruce_pre['_ELEVFILLEDmean'] - spruce_pre['_ELEVmean'])
spruce_post['dep_volume'] = spruce_post['area (m^2)'] * (spruce_post['_ELEVFILLEDmean'] - spruce_post['_ELEVmean'])
white_pre['dep_volume'] = white_pre['area (m^2)'] * (white_pre['_ELEVFILLEDmean'] - white_pre['_ELEVmean'])
white_post['dep_volume'] = white_post['area (m^2)'] * (white_post['_ELEVFILLEDmean'] - white_post['_ELEVmean'])

#calculate the xxth percentile of pre-mining elevation for each basin. This will be used 
#to mask out closed depressions that fall low in the landscape because they are in
#river valleys which are 1) unmined and 2) very subject to DEM errors that generate sinks.

percentile = 20
ben_elev_threshold = np.percentile(ben_pre_topo[ben_pre_topo > 0], percentile)
laurel_elev_threshold = np.percentile(laurel_pre_topo[laurel_pre_topo > 0], percentile)
mud_elev_threshold = np.percentile(mud_pre_topo[mud_pre_topo > 0], percentile)
spruce_elev_threshold = np.percentile(spruce_pre_topo[spruce_pre_topo > 0], percentile)
white_elev_threshold = np.percentile(white_pre_topo[white_pre_topo > 0], percentile)

#make Figure 8
x = np.arange(5)
width = 0.4
names = ['Ben\n' 'Creek', 'Laurel\n' 'Creek', 'Mud\n' 'River', 'Spruce\n' 'Fork', 'White\n' 'Oak']
pre_mine_volumes = [ben_pre['dep_volume'][ben_pre['_ELEVmean'] > ben_elev_threshold].sum(),
                   laurel_pre['dep_volume'][laurel_pre['_ELEVmean'] > laurel_elev_threshold].sum(),
                   mud_pre['dep_volume'][mud_pre['_ELEVmean'] > mud_elev_threshold].sum(),
                   spruce_pre['dep_volume'][spruce_pre['_ELEVmean'] > spruce_elev_threshold].sum(),
                   white_pre['dep_volume'][white_pre['_ELEVmean'] > white_elev_threshold].sum()]
post_mine_volumes = [ben_post['dep_volume'][ben_post['_ELEVmean'] > ben_elev_threshold].sum(),
                   laurel_post['dep_volume'][laurel_post['_ELEVmean'] > laurel_elev_threshold].sum(),
                   mud_post['dep_volume'][mud_post['_ELEVmean'] > mud_elev_threshold].sum(),
                   spruce_post['dep_volume'][spruce_post['_ELEVmean'] > spruce_elev_threshold].sum(),
                   white_post['dep_volume'][white_post['_ELEVmean'] > white_elev_threshold].sum()]
                   
fig = plt.figure(figsize=(6,4))
ax = plt.subplot()
ax.bar(x-0.2, pre_mine_volumes, width, color = '#8da0cb', edgecolor = 'k', label = 'Pre-mining DEM')
ax.bar(x+0.2, post_mine_volumes, width, color = '#fc8d62', edgecolor = 'k', label = 'Post-mining DEM')
ax.set_yscale('log')
ax.set_xticks(x)
ax.set_xticklabels(names)
ax.legend(loc = (0.46,0.84))
ax.set_ylabel('Total volume of closed\n' 'depressions above $z_{20}$ [m$^3$]')
fig.savefig('fig8_depression_volume.png', dpi=1000, bbox_inches='tight')