#This code follows the "Hands On" portion of Section C - Spatial Data in the Geographic Data Science Course (ENVS363/563) at the University of Liverpool by Dr. Dani Arribas-Bel

import geopandas
import osmnx
import contextily as cx
import matplotlib.pyplot as plt

#Dataset collection
#Open a polygon dataset that contains the boundaries of Spanish cities
cities = geopandas.read_file("https://ndownloader.figshare.com/files/20232174")

#Open a line dataset that contains a subset of the street network in Madrid
url = ("https://github.com/geochicasosm/lascallesdelasmujeres/raw/master/data/madrid/final_tile.geojson")
streets = geopandas.read_file(url)

#Open a point dataset that contains the location of bars in Madrid
#This will be done using the Python library osmnx, which allows us to query OpenStreetMap
#The "tags" delimits the query to only amenities of the type "bar"
pointsOfInterest = osmnx.features_from_place("Madrid, Spain", tags={"amenity": "bar"})

##############################################################################################

#Inspecting spatial data
print(cities.head())
cities.plot()
plt.show()
streets.plot()
plt.show()
pointsOfInterest.plot()
plt.show()

##############################################################################################

#Styling plots
pointsOfInterest.plot(alpha=0.1) #This changes the transparency 
plt.show()

#Remove the axes from the map
#Step 1: Setup figure and axis - create a figure named f with one axis named ax
f, ax = plt.subplots(1)
#Step 2: Plot layer of polygons on the axis - draw the polygons on the axis, ax - the method returns the axis with the geographies in them and stores it in an object with the same name
cities.plot(ax=ax)
#Step 3: Remove axis frames
ax.set_axis_off()
#Step 4: Display
plt.show()

#Adding a title
streets.plot()
plt.suptitle("Streets of Madrid")
plt.show()

#Changing map size
#Step 1: setup figure and axis with different size - in the figsize() argument, the first number represents the width and the second number represents the height
f, ax = plt.subplots(1, figsize=(12,12))
cities.plot(ax=ax)
plt.show()

#Changing the borders of polygons
#Step 1: setup figure and axis
f, ax = plt.subplots(1, figsize=(12,12))
#Step 2: Add layer of polygons on the axis, set fill color (facecolor) and border color (edgecolor)
cities.plot(
    linewidth=1,
    facecolor='red',
    edgecolor='black',
    ax=ax
)
plt.show()
#Same process for lines, except that to change line color, you simply use "color"
f, ax = plt.subplots(1)
streets.plot(
    color='red',
    linewidth=1,
    ax=ax
)
plt.show()

#Transforming CRS
print(cities.crs) #returns the current layer crs
#Reproject (to_crs) and plot (plot) polygons
cities.to_crs(epsg=4326).plot()
#Set equal axis
lims = plt.axis('equal')
plt.show()

##############################################################################################
#Composing multi-layer maps
madrid = cities.loc[[12], :].to_crs(epsg=4326) #Madrid has an id of 12 in the Spanish cities dataset; here we select it, and convert it to a CRS that is in lat/long
print(madrid)
#Below, we plot two layers: the madrid city polygon and the points of interest for the city 
f, ax = plt.subplots(1)
madrid.plot(ax=ax, color="yellow")
pointsOfInterest.plot(ax=ax, color="green")
plt.show()
plt.savefig('madrid_bars.png', dpi=300) #This line will save the map to an image in the same folder where the code is hosted; the argument dpi allows you to set the resolution; however, I'm not sure where this saved it for me

##############################################################################################
#Manipulating spatial tables (GeoDataFrames)
#Area calculation
print(cities.crs) #checking to make sure the polygons are projected in a crs that uses distance measurements
city_areas = cities.area
print(city_areas.head())
city_areas_sqkm = city_areas / 1000000
print(city_areas_sqkm.head()) 

#Length
print(streets.crs) #checking to see what crs the streets dataset is in; it's in EPSG4326 which uses lat/long, so we'll reproject the layer into the local Spanish CRS (EPSG=25830) which uses distance measurements
street_length = streets.to_crs(epsg=25830).length
print(street_length.head())

#Centroid calculation - a centroid is the spatial analog of the average of a polygon - used to summarize a polygon into a single point
cents = cities.centroid #This command returns a GeoSeries object (a single column with spatial data) with the centroids of a polygon GeoDataFrame - this can therefore be plotted directly, just like a table
print(cents.head())
cents.plot()
plt.show()

#Point in polygon (PiP) - Knowing whether a point is located inside a polygon - this can be done in GeoPandas using the contains method
polygon = cities.loc[12, 'geometry']
point1 = cents[0]
point2 = cents[112]
print(polygon.contains(point1))
print(polygon.contains(point2))
#A spatilal join is better used when there are many points and polygons to analyze

#Buffers
pointsOfInterest_reprojected = pointsOfInterest.to_crs(cities.crs)
print(pointsOfInterest_reprojected.crs)
buffer = pointsOfInterest_reprojected.buffer(500) #creates a 500 meter buffer around every bar in Madrid
print(buffer.head())
f, ax = plt.subplots(1)
buffer.plot(ax=ax, linewidth=0)
pointsOfInterest_reprojected.plot(ax=ax, markersize=1, color='yellow') #plot bars on top of buffers
plt.show()

##############################################################################################
#Adding base layers from web sources
#contextily is the library we use to add web basemaps
ax = cities.plot(color="black")
cx.add_basemap(ax, crs=cities.crs) #contextily.add_basemap requires an explicit description of what crs to use
plt.show()

f, ax = plt.subplots(1, figsize=(9,9))
madrid.plot(alpha=0.25, ax=ax)
cx.add_basemap(ax, crs=madrid.crs) #this opens the general OpenStreetMap
cx.add_basemap(ax, crs=madrid.crs, source=cx.providers.Esri.WorldImagery) #This opens satellite imagery
cx.add_basemap(ax, crs=madrid.crs, source=cx.providers.Esri.WorldTerrain) #This opens a terrain map
ax.set_axis_off()
plt.show()

##############################################################################################
#Attribute joins and spatial joins - following the Merging data documentation from GeoPandas: https://geopandas.org/en/stable/docs/user_guide/mergingdata.html
import geodatasets
import pandas as pd
chicago = geopandas.read_file(geodatasets.get_path("geoda.chicago.commpop"))
groceries = geopandas.read_file(geodatasets.get_path("geoda.groceries"))
#For attribute join
chicago_shapes = chicago[['geometry', 'NID']]
chicago_names = chicago[['community', 'NID']]
#For spatial joins
chicago = chicago[['geometry', 'community']].to_crs(groceries.crs)
#Appending GeoDataFrame and GeoSeries using the pandas append() methods
#Remember: GeoSeries = a Series object designed to store shapely geometry objects
#Remember: GeoDataFrame = a pandas.DataFrame that has a column with geometry
#Appending GeoSeries
joined = pd.concat([chicago.geometry, groceries.geometry])
#Appending GeoDataFrames
douglas = chicago[chicago.community == 'DOUGLAS']
oakland = chicago[chicago.community == 'OAKLAND']
douglas_oakland = pd.concat([douglas, oakland])
#Attribute joins
#Attribute joins are done using the `merge` method which will merge the two different types of information based on a shared variable, i.e., ID
#It's recommended to use the `merge()` method called from the spatial dataset, though the pandas.merge() method will work if the GeoDataFrame is in the left argument
#If the DataFrame is in the left argument and the GeoDataFrame is in the right argument, the result will no longer be a GeoDataFrame
#The following merge adds the chicago_names DataFrame to the chicago_shapes GeoDataFrame on the shared variable NID
print(chicago_shapes.head()) #By printing this out, we see that chicago_shapes is the GeoDataFrame (because there is a column for geometry information)...
print(chicago_names.head()) #... and the chicago_names is the DataFrame
chicago_shapes = chicago_shapes.merge(chicago_names, on='NID') #We merge the GeoDataFrame and the DataFrame using the merge method on the shared variable (NID)
print(chicago_shapes.head())
#Spatial joins
#In a spatial join, two geometry objects are merged based on their spatial relationship to one another
#In the following example, one GeoDataFrame is of communities, and the other GeoDataFrame is of grocery stores
print(chicago.head())
print(groceries.head())
#There are two spatial-join methods in GeoPandas: GeoDataFrame.sjoin() and GeoDataFrame.sjoin_nearest()
#GeodataFrame.sjoin() joins based on binary predicates, i.e., intersects, contains, etc.
# - The sjoin() method has two arguments: `how` and `predicate`
# - The `predicate` argument specifies how GeoPandas decides whether or not to join the attributes of one object to another.
# - `predicate` values include: intersects, contains, within, touches, crosses, and overlaps
# - The `how` argument specifies the type of join that will occur and which geometry is retained in the resultant GeoDataFrame
# = The `how` argument takes the following values: left (uses the index from the left (or left_df); retains only the left_df geometry column), right (uses the index from the second (or right_df); retains only the right_df geometry column), and inner (uses the intersection of the index values from both GeoDataFrame; retains only the left_df geometry column)
#GeoDataFrame.sjoin_nearest() joins based on proximity with the ability to set a maximum search radius
# GeoDataFrame.sjoin_nearest() conducts proximity-based joins
# - Takes three arguments: `how` (same as in s.join()), `max_distance`, and `distance_col`
# - max_distance argument specifies a maximum search radius for matching geometries - it's highly recommended to use this parameter
# - distance_col, if set, causes the resultant GeoDataFrame to include a column with this name containing the computed distances between an input geometry and the nearest geomery
groceries_with_community = groceries.sjoin(chicago, how='inner', predicate='intersects')
print(groceries_with_community.head())

##############################################################################################
#Spatial overlays - following the 'Set operations with overlay' documentation from GeoPandas: https://geopandas.org/en/stable/docs/user_guide/set_operations.html
from shapely.geometry import Polygon
#create example data
polys1 = geopandas.GeoSeries([Polygon([(0,0), (2,0), (2,2), (0,2)]),
                              Polygon([(2,2), (4,2), (4,4), (2,4)])])

polys2 = geopandas.GeoSeries([Polygon([(1,1), (3,1), (3,3), (1,3)]),
                              Polygon([(3,3), (5,3), (5,5), (3,5)])])

df1 = geopandas.GeoDataFrame({'geometry': polys1, 'df1':[1,2]})

df2 = geopandas.GeoDataFrame({'geometry': polys2, 'df2':[1,2]})

ax = df1.plot(color='red')
df2.plot(ax=ax, color='green', alpha=0.5)
plt.show()

#Using how='union' returns all the possible geometries
#The overlay() method will determine the set of all individual geometries from overlapping the two input GeoDataFrames - this result covers the area covered by the two input GeoDataFrames and also preserves all unique regions defined by the combined boundaries of the two GeoDataFrames
res_union = df1.overlay(df2, how='union')
ax = res_union.plot(alpha=0.5, cmap='tab10')
df1.plot(ax=ax, facecolor='none', edgecolor='k')
df2.plot(ax=ax, facecolor='none', edgecolor='k')
plt.show()

#Using how='intersection' returns only those geometries that are contained by both GeoDataFrames
res_intersection = df1.overlay(df2, how='intersection')
ax = res_intersection.plot(cmap='tab10')
df1.plot(ax=ax, facecolor='none', edgecolor='k')
df2.plot(ax=ax, facecolor='none', edgecolor='k')
plt.show()

#Using how='symmetric_difference' returns the geometries that are only part of one of the GeoDataFrames but not both
res_symdiff = df1.overlay(df2, how='symmetric_difference')
ax = res_symdiff.plot(cmap='tab10')
df1.plot(ax=ax, facecolor='none', edgecolor='k')
df2.plot(ax=ax, facecolor='none', edgecolor='k')
plt.show()

#Using how='difference' returns the geometries that are part of df1 but are not contained in df2
res_difference = df1.overlay(df2, how='difference')
ax = res_difference.plot(cmap='tab10')
df1.plot(ax=ax, facecolor='none', edgecolor='k')
df2.plot(ax=ax, facecolor='none', edgecolor='k')
plt.show()

#Using how='identity' returns the surface of d1 but with the geometries obtained from overlaying df1 with df2
res_identity = df1.overlay(df2, how='identity')
ax = res_identity.plot(cmap='tab10')
df1.plot(ax=ax, facecolor='none', edgecolor='k')
df2.plot(ax=ax, facecolor='none', edgecolor='k')
plt.show()

#Overlay example using chicago and grocery datasets
chicago = chicago.to_crs("ESRI:102003")
groceries = groceries.to_crs("ESRI:102003")
#We wish to identify the "served" portion of each area - defined as areas within 1 km of a grocery store using a GeoDataFrame of community areas and a GeoDataFrame of groceries
chicago.plot()
plt.show()
print(chicago.crs) #Checking CRS
print(groceries.crs) #Checking CRS
#Creating a 1 km buffer around grocery stores
groceries['geometry'] = groceries.buffer(1000) #CRS is in meters, so 1000 m = 1 km
groceries.plot()
plt.show()
#Now select only the portion of community areas within 1km of a grocery using how='intersection', which creates a new set of polygons where these two layers overlap
chicago_cores = chicago.overlay(groceries, how='intersection') #This gives the portions of Chicago close to grocery stores
chicago_cores.plot(alpha=0.5, edgecolor='k', cmap='tab10')
plt.show()
chicago_periferies = chicago.overlay(groceries, how='difference') #This gives the portions of Chicago far from grocery stores
chicago_periferies.plot(alpha=0.5, edgecolor='k', cmap='tab10')
plt.show()
#Note: in default settings, overlay() returns only geometries of the SAME GEOMETRY TYPE as GeoDataFrame (left one) has, where Polygon and MultiPolygon is considered as a same type.
#      This is controlled using keep_geom_type argument, which is set to True by default.
#      If you set keep_geom_type=False, overlay() will return all geometry types resulting from selected set-operations, where, for example, you could get an intersection of touching geometries where two polygons intersect in a line or a point