########################################################################
#This script generates Figure 4 in the following manuscript:

#Shobe, C.M., Bower, S.J., Maxwell, A.E., Glade, R.C., and Samassi, N.M. (2023) The 
#uncertain future of mountaintop-removal-mined landscapes 1: How mining changes erosion 
#processes and variables. Geomorphology.

#Please cite the paper if you use this code in any way.

#Brief description: this script generates a figure that compare the topography of
#pre- and post- mining topography (elevation, slope, and area-slope product) for 88
#Hydrologic Unit Code 12 (HUC-12) watersheds as a function of proportion of the 
#watershed mined. These calculations use a number of existing datasets that are already
#freely available due to the efforts of others. The HUC-12 watershed boundaries come
#from the USGS Watershed boundary Dataset. The mined area polygons come from Skytruth
#(https://skytruth.org/mountaintop-mining/) as reported in Pericak et al. (2018). The 
#pre- and post-mining digital elevation models were created by Ross et al. (2016) and can 
#be found at https://doi.org/10.6084/m9.figshare.12846764.v1 and 
#https://doi.org/10.6084/m9.figshare.12846788.v1, respectively. This figure also reports
#the results of Bayesian rank correlations for each relationship tested.

########################################################################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('full_mining_stats.csv')

df_clip = df[df.per_Ross > 0.9]

elev_ratios = df_clip.post_mean_elev / df_clip.pre_mean_elev
slope_ratios = df_clip.post_mean_slope / df_clip.pre_mean_slope
SA_ratios = df_clip.post_mean_SA / df_clip.pre_mean_SA

#import MCMC sampling data from Bayesian Spearman correlation
df_MCMC_RATIO_elev = pd.read_csv('bayesian_rank_correlations/outputs/spearman_bayes_RATIO_elev_samples.csv')
df_MCMC_RATIO_slope = pd.read_csv('bayesian_rank_correlations/outputs/spearman_bayes_RATIO_slope_samples.csv')
df_MCMC_RATIO_SA = pd.read_csv('bayesian_rank_correlations/outputs/spearman_bayes_RATIO_SA_samples.csv')
df_MCMC_W2_elev = pd.read_csv('bayesian_rank_correlations/outputs/spearman_bayes_W2_elev_samples.csv')
df_MCMC_W2_slope = pd.read_csv('bayesian_rank_correlations/outputs/spearman_bayes_W2_slope_samples.csv')
df_MCMC_W2_SA = pd.read_csv('bayesian_rank_correlations/outputs/spearman_bayes_W2_SA_samples.csv')

#import MCMC summary stats
summ_stats_RATIO_elev = pd.read_csv('bayesian_rank_correlations/outputs/spearman_bayes_RATIO_elev.csv')
summ_stats_RATIO_slope = pd.read_csv('bayesian_rank_correlations/outputs/spearman_bayes_RATIO_slope.csv')
summ_stats_RATIO_SA = pd.read_csv('bayesian_rank_correlations/outputs/spearman_bayes_RATIO_SA.csv')
summ_stats_W2_elev = pd.read_csv('bayesian_rank_correlations/outputs/spearman_bayes_W2_elev.csv')
summ_stats_W2_slope = pd.read_csv('bayesian_rank_correlations/outputs/spearman_bayes_W2_slope.csv')
summ_stats_W2_SA = pd.read_csv('bayesian_rank_correlations/outputs/spearman_bayes_W2_SA.csv')

from matplotlib import gridspec
import seaborn as sb
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
ms = 75 #standard marker size

fig = plt.figure(figsize=(8, 6))
gs = gridspec.GridSpec(3, 4)
ax1 = fig.add_subplot(gs[0, 0:2])
ax2 = fig.add_subplot(gs[1, 0:2])
ax3 = fig.add_subplot(gs[2, 0:2])

#Wasserstein distance plots
ax4 = fig.add_subplot(gs[0, 2:])
ax5 = fig.add_subplot(gs[1, 2:])
ax6 = fig.add_subplot(gs[2, 2:])

ax1.scatter(df_clip.per_mined*100, elev_ratios, label = 'Mean elevation', color = 'firebrick', s = ms, edgecolor = 'firebrick', alpha = 0.5)
ax1.get_xaxis().set_visible(False)

ax2.scatter(df_clip.per_mined*100, slope_ratios, label = 'Mean slope', color = 'darkorange', s = ms, edgecolor = 'darkorange', alpha = 0.5)
ax2.get_xaxis().set_visible(False)


ax3.scatter(df_clip.per_mined*100, SA_ratios, label = r'Mean $\sqrt{A}S$', color = 'seagreen', s = ms, edgecolor = 'seagreen', alpha = 0.5)

ax1.set_xlim(0, 40)
ax2.set_xlim(0, 40)
ax3.set_xlim(0, 40)
ax4.set_xlim(0, 40)
ax5.set_xlim(0, 40)
ax6.set_xlim(0, 40)

ax1.tick_params(axis='y', which='major', labelsize=12)
ax2.tick_params(axis='y', which='major', labelsize=12)
ax3.tick_params(axis='both', which='major', labelsize=12)

ax4.tick_params(axis='y', which='major', labelsize=12)
ax5.tick_params(axis='y', which='major', labelsize=12)
ax6.tick_params(axis='both', which='major', labelsize=12)



ax1.set_ylabel(r'$\overline{E}_{\mathrm{post}}/\overline{E}_{\mathrm{pre}}$', fontsize = 14)
ax2.set_ylabel(r'$\overline{S}_{\mathrm{post}}/\overline{S}_{\mathrm{pre}}$', fontsize = 14)
ax3.set_ylabel(r'$\overline{\sqrt{A}S}_{\mathrm{post}} / \overline{\sqrt{A}S}_{\mathrm{pre}}$', fontsize = 14)
ax3.set_ylim(0.8, 1.5)

ax1.yaxis.set_ticks(np.arange(0.99, 1.01, 0.01))

#make wasserstein distance plots
ax4.scatter(df_clip.per_mined*100, df_clip.W2_elev, color = 'firebrick', s = ms, edgecolor = 'firebrick', alpha = 0.5)
ax5.scatter(df_clip.per_mined*100, df_clip.W2_slope, color = 'darkorange', s = ms, edgecolor = 'darkorange', alpha = 0.5)
ax6.scatter(df_clip.per_mined*100, df_clip.W2_SA, color = 'seagreen', s = ms, edgecolor = 'seagreen', alpha = 0.5)

ax4.get_xaxis().set_visible(False)
ax5.get_xaxis().set_visible(False)

ax4.set_ylabel(r'Elevation $W_2$', fontsize = 14)
ax5.set_ylabel(r'Slope $W_2$', fontsize = 14)
ax6.set_ylabel(r'$\sqrt{A}S$ $W_2$', fontsize = 14)

#one xlabel
fig.text(0.38, -0.02, 'Percent of watershed mined', fontsize = 14)

#insets for Bayesian rank correlations
start_x = 22 #x starting value for inset
len_x = 16
markersize = 75 #for HDPI99 markers
hdpi_pad = -14 #distance below point for numeric label

ax1_ins = ax1.inset_axes([start_x, 0.995, len_x, .01], transform = ax1.transData)
ax1_ins.get_yaxis().set_visible(False)
ax1_ins.spines['top'].set_visible(False)
ax1_ins.spines['left'].set_visible(False)
ax1_ins.spines['right'].set_visible(False)
sb.kdeplot(df_MCMC_RATIO_elev.x, ax = ax1_ins, color = 'k', zorder = 0)
ax1_ins.set_xlabel('')
ax1_ins.get_xaxis().set_ticks([])
ax1_ins.scatter([summ_stats_RATIO_elev.values_column[2], summ_stats_RATIO_elev.values_column[3]], [0,0], clip_on=False, zorder = 4, edgecolor = 'k', facecolor = 'w', s = markersize)
ax1_ins.patch.set_alpha(0.)
ax1_ins.annotate(str(np.round(summ_stats_RATIO_elev.values_column[2], 2)), 
                 (summ_stats_RATIO_elev.values_column[2],0), 
                 textcoords="offset points", 
                 xytext=(0,hdpi_pad), 
                 ha='center') 
ax1_ins.annotate(str(np.round(summ_stats_RATIO_elev.values_column[3], 2)), 
                 (summ_stats_RATIO_elev.values_column[3],0), 
                 textcoords="offset points", 
                 xytext=(0,hdpi_pad), 
                 ha='center') 

#insets for Bayesian rank correlations
ax2_ins = ax2.inset_axes([start_x, 1.03, len_x, 0.12], transform = ax2.transData)
ax2_ins.get_yaxis().set_visible(False)
ax2_ins.spines['top'].set_visible(False)
ax2_ins.spines['left'].set_visible(False)
ax2_ins.spines['right'].set_visible(False)
sb.kdeplot(df_MCMC_RATIO_slope.x, ax = ax2_ins, color = 'k', zorder = 0)
ax2_ins.set_xlabel('')
ax2_ins.get_xaxis().set_ticks([])
ax2_ins.patch.set_alpha(0.)
ax2_ins.scatter([summ_stats_RATIO_slope.values_column[2], summ_stats_RATIO_slope.values_column[3]], [0,0], clip_on=False, zorder = 4, edgecolor = 'k', facecolor = 'w', s = markersize)

ax2_ins.annotate(str(np.round(summ_stats_RATIO_slope.values_column[2], 2)), 
                 (summ_stats_RATIO_slope.values_column[2],0), 
                 textcoords="offset points", 
                 xytext=(0,hdpi_pad), 
                 ha='center') 
ax2_ins.annotate(str(np.round(summ_stats_RATIO_slope.values_column[3], 2)), 
                 (summ_stats_RATIO_slope.values_column[3],0), 
                 textcoords="offset points", 
                 xytext=(0,hdpi_pad), 
                 ha='center') 

#insets for Bayesian rank correlations
ax3_ins = ax3.inset_axes([start_x, 1.15, len_x, 0.3], transform = ax3.transData)
ax3_ins.get_yaxis().set_visible(False)
ax3_ins.spines['top'].set_visible(False)
ax3_ins.spines['left'].set_visible(False)
ax3_ins.spines['right'].set_visible(False)
sb.kdeplot(df_MCMC_RATIO_SA.x, ax = ax3_ins, color = 'k', zorder = 0)
ax3_ins.set_xlabel('')
ax3_ins.patch.set_alpha(0.)
ax3_ins.get_xaxis().set_ticks([])
ax3_ins.scatter([summ_stats_RATIO_SA.values_column[2], summ_stats_RATIO_SA.values_column[3]], [0,0], clip_on=False, zorder = 4, edgecolor = 'k', facecolor = 'w', s = markersize)

ax3_ins.annotate(str(np.round(summ_stats_RATIO_SA.values_column[2], 2)), 
                 (summ_stats_RATIO_SA.values_column[2],0), 
                 textcoords="offset points",
                 xytext=(0,hdpi_pad), 
                 ha='center') 
ax3_ins.annotate(str(np.round(summ_stats_RATIO_SA.values_column[3], 2)), 
                 (summ_stats_RATIO_SA.values_column[3],0), 
                 textcoords="offset points", 
                 xytext=(0,hdpi_pad), 
                 ha='center') 

#insets for Bayesian rank correlations
ax4_ins = ax4.inset_axes([start_x, 2, len_x, 2.5], transform = ax4.transData)
ax4_ins.get_yaxis().set_visible(False)
ax4_ins.spines['top'].set_visible(False)
ax4_ins.spines['left'].set_visible(False)
ax4_ins.spines['right'].set_visible(False)
sb.kdeplot(df_MCMC_W2_elev.x, ax = ax4_ins, color = 'k', zorder = 0)
ax4_ins.set_xlabel('')
ax4_ins.get_xaxis().set_ticks([])
ax4_ins.scatter([summ_stats_W2_elev.values_column[2], summ_stats_W2_elev.values_column[3]], [0,0], clip_on=False, zorder = 4, edgecolor = 'k', facecolor = 'w', s = markersize)

ax4_ins.annotate(str(np.round(summ_stats_W2_elev.values_column[2], 2)), 
                 (summ_stats_W2_elev.values_column[2],0), 
                 textcoords="offset points", 
                 xytext=(0,hdpi_pad), 
                 ha='center') 
ax4_ins.annotate(str(np.round(summ_stats_W2_elev.values_column[3], 2)), 
                 (summ_stats_W2_elev.values_column[3],0), 
                 textcoords="offset points", 
                 xytext=(0,hdpi_pad), 
                 ha='center') 

#insets for Bayesian rank correlations
ax5_ins = ax5.inset_axes([start_x, 0.03, len_x, 0.05], transform = ax5.transData)
ax5_ins.patch.set_alpha(0.)
ax5_ins.get_yaxis().set_visible(False)
ax5_ins.spines['top'].set_visible(False)
ax5_ins.spines['left'].set_visible(False)
ax5_ins.spines['right'].set_visible(False)
sb.kdeplot(df_MCMC_W2_slope.x, ax = ax5_ins, color = 'k', zorder = 0)
ax5_ins.set_xlabel('')
ax5_ins.get_xaxis().set_ticks([])
ax5_ins.scatter([summ_stats_W2_slope.values_column[2], summ_stats_W2_slope.values_column[3]], [0,0], clip_on=False, zorder = 4, edgecolor = 'k', facecolor = 'w', s = markersize)

ax5_ins.annotate(str(np.round(summ_stats_W2_slope.values_column[2], 2)), 
                 (summ_stats_W2_slope.values_column[2],0), 
                 textcoords="offset points", 
                 xytext=(0,hdpi_pad), 
                 ha='center') 
ax5_ins.annotate(str(np.round(summ_stats_W2_slope.values_column[3], 2)), 
                 (summ_stats_W2_slope.values_column[3],0), 
                 textcoords="offset points", 
                 xytext=(0,hdpi_pad), 
                 ha='center') 

#insets for Bayesian rank correlations
ax6_ins = ax6.inset_axes([start_x, 16, len_x, 12], transform = ax6.transData)
ax6_ins.patch.set_alpha(0.)
ax6_ins.get_yaxis().set_visible(False)
ax6_ins.spines['top'].set_visible(False)
ax6_ins.spines['left'].set_visible(False)
ax6_ins.spines['right'].set_visible(False)
sb.kdeplot(df_MCMC_W2_SA.x, ax = ax6_ins, color = 'k', zorder = 0)
ax6_ins.set_xlabel('')
ax6_ins.get_xaxis().set_ticks([])
ax6_ins.scatter([summ_stats_W2_SA.values_column[2], summ_stats_W2_SA.values_column[3]], [0,0], clip_on=False, zorder = 4, edgecolor = 'k', facecolor = 'w', s = markersize)

ax6_ins.annotate(str(np.round(summ_stats_W2_SA.values_column[2], 2)), 
                 (summ_stats_W2_SA.values_column[2],0), 
                 textcoords="offset points", 
                 xytext=(0,hdpi_pad), 
                 ha='center') 
ax6_ins.annotate(str(np.round(summ_stats_W2_SA.values_column[3], 2)), 
                 (summ_stats_W2_SA.values_column[3],0), 
                 textcoords="offset points", 
                 xytext=(0,hdpi_pad), 
                 ha='center') 

#ABCD labels
ax1.text(0.02, 0.85, 'A', transform=ax1.transAxes, fontsize = 18)
ax2.text(0.02, 0.85, 'B', transform=ax2.transAxes, fontsize = 18)
ax3.text(0.02, 0.85, 'C', transform=ax3.transAxes, fontsize = 18)
ax4.text(0.02, 0.85, 'D', transform=ax4.transAxes, fontsize = 18)
ax5.text(0.02, 0.85, 'E', transform=ax5.transAxes, fontsize = 18)
ax6.text(0.02, 0.85, 'F', transform=ax6.transAxes, fontsize = 18)


plt.tight_layout()
fig.savefig('fig4_v3.png', dpi=1000, bbox_inches='tight')