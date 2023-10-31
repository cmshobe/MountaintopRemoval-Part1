########################################################################
#This script runs statistical tests for Figure 4 in the following manuscript:

#Shobe, C.M., Bower, S.J., Maxwell, A.E., Glade, R.C., and Samassi, N.M. (2023) The 
#uncertain future of mountaintop-removal-mined landscapes 1: How mining changes erosion 
#processes and variables. Geomorphology.

#Please cite the paper if you use this code in any way.

#Brief description: this script uses the software and methodology of 
#
#       van Doorn, J.B., Ly, A., Marsman, M., & Wagenmakers, E.-J.  (2020). 
#           Bayesian Rank-Based Hypothesis Testing for the Rank Sum Test, the Signed Rank Test, 
#           and Spearman's rho. Journal of Applied Statistics, 47, 2984-3006.
#
#as downloaded from the article's online supplement: https://osf.io/gny35/
#
#to conduct Bayesian rank correlation analyses on the relationships 
#between the proportion of a watershed that experienced mountaintop removal
#mining and the changes in topography between the pre- and post-mined 
#watersheds.

########################################################################

# First source the files with the relevant functions
source('rankBasedCommonFunctions.R')
source('rankSumSampler.R') # Wilcoxon rank sum function
source('signRankSampler.R') # Wilcoxon signed-rank function
source('spearmanSampler.R')# Spearman's rho function
library(logspline)
library(HDInterval)

mining_data <- read.csv("../full_mining_stats.csv") 

x <- mining_data$per_mined[mining_data$per_Ross>0.9] # percent mined
y <- mining_data$W2_SA[mining_data$per_Ross>0.9] # elev wasserstein dist

rhoSamples_W2_SA <- spearmanGibbsSampler(xVals = x,
                                         yVals = y, 
                                         nSamples = 1e5,
                                         progBar = TRUE,
                                         kappaPriorParameter = 1,
                                         nBurnin = 1,
                                         nChains = 5)

# Posterior distribution
hist(rhoSamples_W2_SA$rhoSamples, freq = FALSE)

# Give the posterior samples for rho to the function below to compute BF01
spearman_bayes_factor_W2_SA <- computeBayesFactorOneZero(rhoSamples_W2_SA$rhoSamples, 
                          whichTest = "Spearman",
                          priorParameter = 1)
# Bayes' factor is the ratio of the likelihood of our alternative model 
# (presumably, the existence of a correlation) to the null model (none)

#calculate 95% and 99% HPDI (highest posterior density interval) 

cred_interval_99_W2_SA <- hdi(rhoSamples_W2_SA$rhoSamples, 0.99)
cred_interval_95_W2_SA <- hdi(rhoSamples_W2_SA$rhoSamples, 0.95)


d_W2_SA = density(rhoSamples_W2_SA$rhoSamples)
plot(d_W2_SA)

posterior_median <- median(rhoSamples_W2_SA$rhoSamples)

#stuff to save!
labels_column <- c("posterior_median", 
                   "bayes_factor",
                   "cred_interval_99_min",
                   "cred_interval_99_max",
                   "cred_interval_95_min",
                   "cred_interval_95_max")
values_column <- c(posterior_median,
                   spearman_bayes_factor_W2_SA,
                   cred_interval_99_W2_SA[1],
                   cred_interval_99_W2_SA[2],
                   cred_interval_95_W2_SA[1],
                   cred_interval_95_W2_SA[2])

#build dataframe
export_df <- data.frame(labels_column, values_column)
write.csv(export_df, 'outputs/spearman_bayes_W2_SA.csv', row.names = FALSE)
write.csv(rhoSamples_W2_SA$rhoSamples, 'outputs/spearman_bayes_W2_SA_samples.csv', row.names = FALSE)