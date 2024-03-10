import geopandas
import pandas as pd
import matplotlib.pyplot as plt
import contextily as cx


db = pd.read_csv("C:\\Users\\maddy\\OneDrive\\Documents\\Github\\python-geospatial-practice\\data\\NFDB_point_20220901.csv")
gdf = geopandas.GeoDataFrame(db, geometry=geopandas.points_from_xy(db['LATITUDE'], db['LONGITUDE']), crs='EPSG:3347') #This line creates a GeoDataFrame from the DataFrame by adding a 'geometry' column
#print(gdf.head()) 

ab_fire_selector = ['AB']
gdf_fieldname = 'SRC_AGENCY'
alberta_wildfires_gdf = gdf[gdf[gdf_fieldname].isin(ab_fire_selector)]
#print(alberta_wildfires_gdf.head())
f,ax = plt.subplots(1, figsize=(12,12))
alberta_wildfires_gdf.to_crs(epsg=3347).plot(ax=ax)
cx.add_basemap(ax, crs=alberta_wildfires_gdf.crs) #check this
ax.set_axis_off()
plt.show()