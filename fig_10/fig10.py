########################################################################
#This script generates Figure 10 in the following manuscript:

#Shobe, C.M., Bower, S.J., Maxwell, A.E., Glade, R.C., and Samassi, N.M. (2023) The 
#uncertain future of mountaintop-removal-mined landscapes 1: How mining changes erosion 
#processes and variables. Geomorphology.

#Please cite the paper if you use this code in any way.

#Brief description: this script plots the kernel density estimates for the normalized
#difference vegetation index (NDVI) in a mountaintop-removal-mined area as derived
#from two Landsat images. The images are publicly available from the Landsat archive.
#The earlier (1999) image is #LE07_L1TP_018034_19990818_20161002_01_T1. and the later 
#(2019) image is LC08_L1TP_018034_20190614_20190620_01_T1. The mine polygon was mapped by 
#Reed and Kite (2020) as part of the Holden mine complex; the polygon can be found in 
#their data archive at https://doi.org/10.5281/zenodo.2550664.

########################################################################


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams.update({'font.size': 24})

file_1999 = '1999_ndvi_epsg26917_clip_points.csv'
data_1999 = pd.read_csv(file_1999)
file_2019 = '2019_ndvi_epsg26917_clip_points.csv'
data_2019 = pd.read_csv(file_2019)


fig4 = plt.figure(figsize=(8, 5))
ax4 = plt.subplot()
sns.kdeplot(data_1999.NDVI, #bw=20, 
             color = 'darkblue', label='1999',
             linewidth=5,
           linestyle='--', common_norm = True)
sns.kdeplot(data_2019.NDVI, #bw=20, 
             color = 'darkgreen', label='2019',
             linewidth=5, common_norm = True)
ax4.set_xlabel('Summer NDVI')
ax4.set_ylabel('Probability density')
ax4.legend()

plt.tight_layout()
fig4.savefig('ndvi_histograms_rev1.eps', dpi=1000, bbox_inches='tight')