########################################################################
#This script generates data for Figure 4 in the following manuscript:

#Shobe, C.M., Bower, S.J., Maxwell, A.E., Glade, R.C., and Samassi, N.M. (2023) The 
#uncertain future of mountaintop-removal-mined landscapes 1: How mining changes erosion 
#processes and variables. Geomorphology.

#Please cite the paper if you use this code in any way.

#Brief description: this script generates data for a figure that compares the topography 
#of pre- and post- mining topography (elevation, slope, and area-slope product) for 88
#Hydrologic Unit Code 12 (HUC-12) watersheds as a function of proportion of the 
#watershed mined. These calculations use a number of existing datasets that are already
#freely available due to the efforts of others. The HUC-12 watershed boundaries come
#from the USGS Watershed boundary Dataset. The mined area polygons come from Skytruth
#(https://skytruth.org/mountaintop-mining/) as reported in Pericak et al. (2018). The 
#pre- and post-mining digital elevation models were created by Ross et al. (2016) and can 
#be found at https://doi.org/10.6084/m9.figshare.12846764.v1 and 
#https://doi.org/10.6084/m9.figshare.12846788.v1, respectively. This script also uses
#functionality from Landlab (https://landlab.readthedocs.io/en/master/; 
#Barnhart et al., 2020).

########################################################################

import time
import copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import landlab
from landlab.plot import imshow_grid, imshowhs_grid
from landlab import RasterModelGrid
from landlab.io.esri_ascii import read_esri_ascii
from landlab.components import (PriorityFloodFlowRouter,
                                DepressionFinderAndRouter,
                                FlowAccumulator)
import seaborn as sbn
import geopandas as gpd
import rasterio
from rasterio import features
from rasterio.enums import MergeAlg
import fiona
from rasterio.mask import mask
import ot

#input path must contain the pre- and post-mining DEMS as well as the mine extent dataset
#available from archives by Ross et al. (2016) and Pericak et al. (2018) as noted above.
input_path = ''

#shp path must contain the HUC-12 basin outlines from the Watershed Boundary Dataset
#available from the USGS as noted above. This polygon file should be clipped such that
#it contains only polygons at at least partially overlap the DEM(s) of interest.
shp_path = ''

#read the shapefile of HUC12 watersheds that overlap the Ross DEM data extent
#and create an empty dataframe to add our calculated data

#n is the number of HUC-12 watersheds that overlap the DEMs of interest.
n = 158

shapes = gpd.gpd.read_file(shp_path)
shapes['huc12'].head()
df = pd.DataFrame()
df['huc12']=shapes['huc12']
df['geometry'] = shapes['geometry']
df['per_mined'] = 0 
df['pre_mean_elev'] = 0
df['pre_mean_slope'] = 0
df['pre_mean_d8'] = 0
df['post_mean_elev'] = 0
df['post_mean_slope'] = 0
df['post_mean_d8']= 0
df['per_mined']=0
df['W2_elev'] =0
df['W2_d8']=0
df['W2_slope'] = 0
df['pre_mean_SA'] = 0
df['post_mean_SA'] = 0
df['counter'] = np.arange(0, n, 1)

#The full Ross DEM files are too large for landlab, so this loop will split the full DEM 
#into bite-size HUC12 watersheds to process with Landlab
#1. Open large DEM with Rasterio
#2. Mask by HUC-12
#3. Create landlab RasterModelGrids
#4. Accumulate flow and calculate slope
#5. Calculate variables 

shapefile = fiona.open(shp_path, "r") 
pre_elev = rasterio.open(input_path+'TauOld.asc') #pre-mining DEM (Ross et al., 2016)
post_elev = rasterio.open(input_path+'TauNew.asc') #post-mining DEM (Ross et al., 2016)
mine_mask = rasterio.open(input_path+'mine_mask.asc') #mined extent dataset (Pericak et al., 2018)

counter = 0   
#iterate through each HUC-12 watershed that at least partially overlaps the DEM
for feature in shapefile:
    shape = [feature["geometry"]]
    
	#MASK THE RASTERS TO THE WATERSHED, and then use Landlab to accumulate flow
	#and extract elevation, slope, and drainage area
	out_pre_elev, out_transform = mask(pre_elev, shape, crop=True)
	out_post_elev, out_transform = mask(post_elev, shape, crop=True)
	out_mine_mask, out_transform = mask(mine_mask,shape,crop=True)

	pre_elev_ar = (out_pre_elev[0,:,:].astype('float64'))
	post_elev_ar = (out_post_elev[0,:,:].astype('float64'))
	mine_mask_ar = (out_mine_mask[0,:,:].astype('float64'))

	pre_mg = RasterModelGrid((len(pre_elev_ar[:,]),len(pre_elev_ar[0])),10)
	pre_mg.add_zeros("topographic__elevation", at="node")

	post_mg = RasterModelGrid((len(post_elev_ar[:,]),len(post_elev_ar[0])),10)
	post_mg.add_zeros("topographic__elevation", at="node")

	pre_elev_ar_flat = pre_elev_ar.flatten()
	post_elev_ar_flat = post_elev_ar.flatten()
	mine_mask_ar_flat = mine_mask_ar.flatten()

	pre_mg.at_node["topographic__elevation"][:] = pre_elev_ar_flat
	post_mg.at_node["topographic__elevation"][:] = post_elev_ar_flat

	pre_mg.set_closed_boundaries_at_grid_edges(True,True,True,True)
	pre_mg.set_nodata_nodes_to_closed(pre_elev_ar_flat, -9999)
	pre_mg.set_watershed_boundary_condition(pre_elev_ar_flat, nodata_value = -9999, return_outlet_id=True)
	post_mg.set_closed_boundaries_at_grid_edges(True,True,True,True)
	post_mg.set_nodata_nodes_to_closed(post_elev_ar_flat, -9999)
	post_mg.set_watershed_boundary_condition(post_elev_ar_flat, nodata_value = -9999, return_outlet_id=True)

	fa_pre = PriorityFloodFlowRouter(pre_mg,flow_metric="D8", suppress_out=True)
	fa_post = PriorityFloodFlowRouter(post_mg,flow_metric="D8", suppress_out=True)

	fa_pre.run_one_step()
	fa_post.run_one_step()

	pre_mg.calc_slope_at_node()
	post_mg.calc_slope_at_node()

	pre_elev_clipped = pre_mg.at_node['topographic__elevation'][pre_mg.core_nodes]
	pre_slope_clipped = pre_mg.at_node['topographic__steepest_slope'][pre_mg.core_nodes]
	pre_area_clipped = pre_mg.at_node['drainage_area'][pre_mg.core_nodes]
	post_elev_clipped = post_mg.at_node['topographic__elevation'][post_mg.core_nodes]
	post_slope_clipped = post_mg.at_node['topographic__steepest_slope'][post_mg.core_nodes]
	post_area_clipped = post_mg.at_node['drainage_area'][post_mg.core_nodes]


    #CALCULATIONS

    #percent mined
    per_mined = len(mine_mask_ar_flat[mine_mask_ar_flat == 1]) / len(mine_mask_ar_flat)

    #mean values
    pre_mean_elev = np.mean(pre_elev_clipped)
    pre_mean_slope = np.mean(pre_slope_clipped)
    pre_mean_area = np.mean(pre_area_clipped)
    pre_mean_SA = (np.mean(pre_area_clipped)**0.5) * (np.mean(pre_slope_clipped))
    post_mean_elev = np.mean(post_elev_clipped)
    post_mean_slope = np.mean(post_slope_clipped)
    post_mean_area = np.mean(post_area_clipped)
    post_mean_SA = (np.mean(post_area_clipped)**0.5) * (np.mean(post_slope_clipped))


    #Wasserstein numbers for all variables
    W2_2_elev = ot.wasserstein_1d(pre_elev_clipped, post_elev_clipped, p=2)
    W2_elev = np.sqrt(W2_2_elev)

    W2_2_d8 = ot.wasserstein_1d(pre_area_clipped, pre_area_clipped, p=2)
    W2_d8 = np.sqrt(W2_2_d8)

    W2_2_slope = ot.wasserstein_1d(pre_slope_clipped, post_slope_clipped, p=2)
    W2_slope = np.sqrt(W2_2_slope)

    W2_2_SA = ot.wasserstein_1d((pre_area_clipped**0.5*pre_slope_clipped),(post_area_clipped**0.5*post_slope_clipped),p=2)
    W2_SA = np.sqrt(W2_2_SA)


    df.loc[df.counter == counter, 'per_mined'] = per_mined
    df.loc[df.counter == counter, 'pre_mean_elev'] = pre_mean_elev
    df.loc[df.counter == counter, 'pre_mean_slope'] = pre_mean_slope
    df.loc[df.counter == counter, 'pre_mean_d8'] = pre_mean_area
    df.loc[df.counter == counter, 'post_mean_elev'] = post_mean_elev
    df.loc[df.counter == counter, 'post_mean_slope'] = post_mean_slope
    df.loc[df.counter == counter, 'post_mean_d8'] = post_mean_area
    df.loc[df.counter == counter, 'W2_elev'] = W2_elev
    df.loc[df.counter == counter, 'W2_d8'] = W2_d8
    df.loc[df.counter == counter, 'W2_slope'] = W2_slope
    df.loc[df.counter == counter, 'W2_SA'] = W2_SA
    df.loc[df.counter == counter, 'pre_mean_SA'] = pre_mean_SA                                                   
    df.loc[df.counter == counter, 'post_mean_SA'] = post_mean_SA 
    
    
    print(counter)
    counter += 1   

#save results to csv
df.to_csv('full_mining_stats.csv')

