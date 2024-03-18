import geopandas
import pandas as pd
import matplotlib.pyplot as plt
import contextily as cx


db = pd.read_csv("C:\\Users\\maddy\\OneDrive\\Documents\\Github\\python-geospatial-practice\\data\\NFDB_point_20220901.csv")
gdf = geopandas.GeoDataFrame(db, geometry=geopandas.points_from_xy(db['LONGITUDE'], db['LATITUDE']), crs='EPSG:3347') #This line creates a GeoDataFrame from the DataFrame by adding a 'geometry' column
ecoregions = geopandas.read_file("C:\\Users\\maddy\\OneDrive\\Documents\\Github\\python-geospatial-practice\\data\\Ecoregions\\ecoregions.shp")
provinces = geopandas.read_file("C:\\Users\\maddy\\OneDrive\\Documents\\Github\\python-geospatial-practice\\data\\lpr_000b16a_e\\lpr_000b16a_e.shp")

ab_fire_selector = ['AB']
gdf_fieldname = 'SRC_AGENCY'
alberta_wildfires_gdf = gdf[gdf[gdf_fieldname].isin(ab_fire_selector)]
#print(alberta_wildfires_gdf.head())
#f,ax = plt.subplots(1, figsize=(12,12))
#alberta_wildfires_gdf.to_crs(epsg=3347).plot(ax=ax)
#alberta_wildfires_gdf = alberta_wildfires_gdf.to_crs(epsg=3347)
#print(alberta_wildfires_gdf.crs)
#alberta_wildfires_gdf.plot(ax=ax)
#cx.add_basemap(ax, crs=alberta_wildfires_gdf.crs) #check this
#ax.set_axis_off()
#plt.show()

alberta_wildfires_2018 = alberta_wildfires_gdf.query("YEAR==2018")
#print(alberta_wildfires_2018)
#alberta_wildfires_2018.plot(ax=ax)
#ax.set_axis_off()
#cx.add_basemap(ax, crs=alberta_wildfires_2018.crs, source=cx.providers.Esri.WorldTerrain)
#lt.show()

alberta_wildfires_ge_200_ha = alberta_wildfires_gdf.query("SIZE_HA>=200")
alberta_wildfires_ge_200_ha = alberta_wildfires_gdf.loc[alberta_wildfires_gdf['SIZE_HA'] >= 200, :] #different way of tackling the above query
#print(alberta_wildfires_ge_200_ha)
#alberta_wildfires_ge_200_ha.plot(ax=ax)
#ax.set_axis_off()
#plt.show()

#print(provinces.head())
alberta = provinces.loc[provinces["PRENAME"] == 'Alberta']
alberta_reprojected = alberta.to_crs(epsg=3347)
#print("Alberta CRS: ", alberta_reprojected.crs)
ecoregions_reprojected = ecoregions.to_crs(epsg=3347)
#print("Ecoregions CRS: ", ecoregions_reprojected.crs)\
alberta_ecoregions = geopandas.clip(ecoregions_reprojected, alberta_reprojected)
alberta_ecoregions.plot()
plt.show()
