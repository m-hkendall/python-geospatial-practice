import geopandas
import pandas as pd
import matplotlib.pyplot as plt
import contextily as cx

ecoregions = geopandas.read_file("C:\\Users\\maddy\\OneDrive\\Documents\\Github\\python-geospatial-practice\\data\\Ecoregions\\ecoregions.shp")
provinces = geopandas.read_file("C:\\Users\\maddy\\OneDrive\\Documents\\Github\\python-geospatial-practice\\data\\lpr_000b16a_e\\lpr_000b16a_e.shp")

#Spatially studying Alberta Ecoregions
#print(provinces.head())
alberta = provinces.loc[provinces["PRENAME"] == 'Alberta']
alberta_reprojected = alberta.to_crs(epsg=3347)
#print("Alberta CRS: ", alberta_reprojected.crs)
ecoregions_reprojected = ecoregions.to_crs(epsg=3347)
#print("Ecoregions CRS: ", ecoregions_reprojected.crs)\
alberta_ecoregions = geopandas.clip(ecoregions_reprojected, alberta_reprojected)
f,ax = plt.subplots(1, figsize=(10,11))
alberta_ecoregions.plot(ax=ax, color='#525252', alpha=0.5, edgecolor='#B9EBE3', linewidth=0.3)
ax.set_axis_off()
cx.add_basemap(ax, crs=alberta_ecoregions.crs)
plt.title("Alberta Ecoregions")
plt.show()

print(alberta_ecoregions.head())
#Calculating area (sqkm) of ecoregion polygons
alberta_ecoregions["area"] = alberta_ecoregions['geometry'].area / 10**6
print(alberta_ecoregions.head())

#Finding the five smallest ecoregion polygons
alberta_ecoregions_sorted = alberta_ecoregions.sort_values(by='area')
print(alberta_ecoregions_sorted)
five_smallest_alberta_ecoregions = alberta_ecoregions_sorted.head(5)
print(five_smallest_alberta_ecoregions)
#Mapping alberta ecoregions, where the smallest ecoregions are colored red and the rest are colored black
f,ax = plt.subplots(1, figsize=(12,12))
alberta_ecoregions.plot(ax=ax, color='#525252', alpha=0.5, edgecolor='#B9EBE3', linewidth=0.3)
five_smallest_alberta_ecoregions.plot(ax=ax, color='red', alpha=0.8)
ax.set_axis_off()
cx.add_basemap(ax, crs=alberta_ecoregions.crs)
plt.title("5 Smallest Alberta Ecoregions")
plt.show()