%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%This script generates a drainage divide network using the pre-mining digital elevation
%model, plotted in Figure 5 in the following manuscript:

%Shobe, C.M., Bower, S.J., Maxwell, A.E., Glade, R.C., and Samassi, N.M. (2023) The 
%uncertain future of mountaintop-removal-mined landscapes 1: How mining changes erosion 
%processes and variables. Geomorphology.

%Please cite the paper if you use this code in any way.

%Brief description: this script uses TopoToolbox2 (Schwanghart and Scherler, 2014) to
%generate the divide network from the pre-mining digital elevation model (DEMs produced
%by Ross et al. (2016) and archived at https://doi.org/10.6084/m9.figshare.12846764.v1).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%parameters
minarea = 50000; %number of pixels to use as the minimum drainage area

%meats
DEM_uncarved = GRIDobj('TauOldElev_WGS84.tif');
disp('dem imported')
FD_carved = FLOWobj(DEM_uncarved, 'preprocess', 'carve', 'verbose', true); %preprocess none means don't fill or carve sinks
disp('flowdir done')
ST_carved = STREAMobj(FD_carved, 'minarea', minarea);
disp('stream network done')
tic;
D_carved = DIVIDEobj(FD_carved, ST_carved, 'network', false, 'verbose', true);
toc;
disp('divides found')
D2_carved = cleanedges(D_carved, FD_carved);
figure
imagesc(DEM_uncarved)
hold on
plot(D2_carved)
plot(ST_carved, 'b')
title('OLD DEM; 5e5 minarea')
hold off

MS = STREAMobj2mapstruct(ST_carved);
shapewrite(MS, 'old_stream_network_5e5')
D2MS = DIVIDEobj2mapstruct(D2_carved, DEM_uncarved, 0);
shapewrite(D2MS, 'old_divide_network_5e5')
