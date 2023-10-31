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

from landlab.io.esri_ascii import read_esri_ascii
from landlab.plot.imshow import imshow_grid
from landlab.components import (
    PriorityFloodFlowRouter
)
import matplotlib.pyplot as plt
from landlab.io.esri_ascii import write_esri_ascii
from landlab.components.depression_finder.lake_mapper import _FLOODED

path = './input_dems/'

#input DEMs: pre is pre-mined and post is post-mined
filenames = ['ben_pre_10m', 
'ben_post_10m', 
'laurel_pre_10m', 
'laurel_post_10m',
'mud_pre_10m',
'mud_post_10m',
'spruce_pre_10m',
'spruce_post_10m',
'whiteoak_pre_10m',
'whiteoak_post_10m']

#iterate through files and route flow to find depressions on each one
for name in filenames:
	filepath = path + name + '.asc'
	mg, z = read_esri_ascii(filepath, name='topographic__elevation') 

	outlet_id = mg.set_watershed_boundary_condition(z,
                                                nodata_value = -99999, 
                                                return_outlet_id=True,
                                               remove_disconnected=True)

	fr=PriorityFloodFlowRouter(mg,'topographic__elevation',
                                                flow_metric='Dinf',
                                                runoff_rate= None,
                           						update_flow_depressions=True,
                                                depression_handler = 'fill',
                                                exponent = 1,
                                                epsilon=True,
                                                accumulate_flow = True, 
                                                accumulate_flow_hill = False,
                                                suppress_out=True)

	fr.run_one_step()
	fr.remove_depressions()
	fs = mg.add_zeros('flood_status', at='node')
	mg.at_node['flood_status'][mg.at_node['depression_free_elevation'] > mg.at_node['topographic__elevation']] = 1

	#save depression-free elevation (surface as if all sinks are filled)
	write_esri_ascii("./flowrouting_output/" + name + "_depression_free_elev.asc", mg, names = ['depression_free_elevation'])
	
	#save flood status (1 for flooded areas, 0 elsewhere)
	write_esri_ascii("./flowrouting_output/" + name + "_flood_status.asc", mg, names = ['flood_status'])