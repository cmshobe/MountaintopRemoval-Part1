%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%This script generates a drainage divide network using the post-mining digital elevation
%model, plotted in Figure 5 in the following manuscript:

%Shobe, C.M., Bower, S.J., Maxwell, A.E., Glade, R.C., and Samassi, N.M. (2023) The 
%uncertain future of mountaintop-removal-mined landscapes 1: How mining changes erosion 
%processes and variables. Geomorphology.

%Please cite the paper if you use this code in any way.

%Brief description: this script uses TopoToolbox2 (Schwanghart and Scherler, 2014) to
%generate the divide network from the post-mining digital elevation model (DEMs produced
%by Ross et al. (2016) and archived at https://doi.org/10.6084/m9.figshare.12846788.v1).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%parameters
minarea = 50000; %number of pixels to use as the minimum drainage area

%meats
DEM_uncarved_new = GRIDobj('TauNew_WGS84.tif');
disp('dem imported')
FD_carved_new = FLOWobj(DEM_uncarved_new, 'preprocess', 'carve', 'verbose', true); %preprocess none means don't fill or carve sinks
disp('flowdir done')
ST_carved_new = STREAMobj(FD_carved_new, 'minarea', minarea);
disp('stream network done')
tic;
D_carved_new = DIVIDEobj(FD_carved_new, ST_carved_new, 'network', false, 'verbose', true);
toc;
disp('divides found')
D2_carved_new = cleanedges(D_carved_new, FD_carved_new);
figure
imagesc(DEM_uncarved_new)
hold on
plot(D2_carved_new)
plot(ST_carved_new, 'b')
title('NEW DEM; 5e5 minarea')
hold off

MS_new = STREAMobj2mapstruct(ST_carved_new);
shapewrite(MS_new, 'new_stream_network_5e5')
D2MS_new = DIVIDEobj2mapstruct(D2_carved_new, DEM_uncarved_new, 0);
shapewrite(D2MS_new, 'new_divide_network_5e5')