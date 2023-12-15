#############################################
## To show the Spatial rainfall percentiles
## Computing the percentile value
## Assume the 1-D array data
## Nearest-rank method
### n = [(p/100)*N]
## list - no of samples
## n index value
## P - req pecentile value
#############################################
import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
##################################
def percentile(list,P):
    list.sort()
    length = len(list)
    rank =(length-1)*(P/100)
    d = rank - int(rank)
    result = float(list[int(rank)]) + (float(list[int(rank + 1)]) - float(list[int(rank)])) * d
    return result
##################################
diri_obs='/scratch/sahiduli/SSK/SAI/INPUTDATA/OBS/RAINFALL/'
#ds = xr.open_dataset(diri_obs+'IMD_DD_CLIM.nc',decode_times=False)
ds = xr.open_dataset(diri_obs+'GPM_IMD_MERGED_MNS2023.nc',decode_times=False)
rfn = ds["rain"]
#print(rfn)
lat = ds["lat"]
lon = ds["lon"]
time = ds["time"]
crd = rfn.shape
#print(dims[0])
##pd.to_datetime(time.values).map(lambda x: x.strftime('%d-%m-%Y_%H')))
#####################
new_rf = np.zeros(shape=(crd[1],crd[2]),dtype=float)
new_rf = rfn[0,:,:]
#####################

for i in range (len(lat)):
    for j in range (len(lon)):
        t1=percentile(rfn[:,i,j].values,95)
        new_rf[i,j]=t1

########################
## plot section
########################

#-- create figure and axes object
fig = plt.figure(figsize=(12,12))

#-- choose map projection
ax = plt.axes(projection=ccrs.PlateCarree())

#-- add coastlines, country border lines, and grid lines
ax.coastlines(zorder=1)

#-- create states outlines
states_provinces = cfeature.NaturalEarthFeature(category='cultural',
                                                name='admin_1_states_provinces_lines',
                                                scale='50m',
                                                facecolor='none')

ax.add_feature(cfeature.BORDERS, linewidth=0.6, edgecolor='gray', zorder=2)
ax.add_feature(states_provinces, edgecolor='gray', zorder=3)

ax.gridlines(draw_labels=True,
             linewidth=0.5,
             color='gray',
             xlocs=range(60,120,20),
             ylocs=range(0,50,10),
             zorder=4)

#-- add title
ax.set_title('Temperature', fontsize=12, fontweight='bold')

#-- create contour line plot
cnplot = ax.contourf(new_rf.lon, new_rf.lat, new_rf[:,:],
                     cmap='jet',
                     levels=15,
                     zorder=0,
                     transform=ccrs.PlateCarree())

#-- add colorbar
cbar = plt.colorbar(cnplot, orientation='horizontal',
                    pad=0.05, shrink=0.7)
cbar.set_label('K')

#-- save graphic output to PNG file
plt.savefig('plot_matplotlib_contour_filled_rect12.png',
            bbox_inches='tight',
            dpi=100)
