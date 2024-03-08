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
#print(cities.head())
#cities.plot()
#plt.show()
#streets.plot()
#plt.show()
#pointsOfInterest.plot()
#plt.show()

##############################################################################################

#Styling plots
#pointsOfInterest.plot(alpha=0.1) #This changes the transparency 
#plt.show()

#Remove the axes from the map
#Step 1: Setup figure and axis - create a figure named f with one axis named ax
#f, ax = plt.subplots(1)
#Step 2: Plot layer of polygons on the axis - draw the polygons on the axis, ax - the method returns the axis with the geographies in them and stores it in an object with the same name
#cities.plot(ax=ax)
#Step 3: Remove axis frames
#ax.set_axis_off()
#Step 4: Display
#plt.show()

#Adding a title
#streets.plot()
#plt.suptitle("Streets of Madrid")
#plt.show()

#Changing map size
#Step 1: setup figure and axis with different size - in the figsize() argument, the first number represents the width and the second number represents the height
#f, ax = plt.subplots(1, figsize=(12,12))
#cities.plot(ax=ax)
#plt.show()

#Changing the borders of polygons
#Step 1: setup figure and axis
#f, ax = plt.subplots(1, figsize=(12,12))
#Step 2: Add layer of polygons on the axis, set fill color (facecolor) and border color (edgecolor)
#cities.plot(
#    linewidth=1,
#    facecolor='red',
#    edgecolor='black',
#    ax=ax
#)
#plt.show()
#Same process for lines, except that to change line color, you simply use "color"
#f, ax = plt.subplots(1)
#streets.plot(
#    color='red',
#    linewidth=1,
#    ax=ax
#)
#plt.show()

#Transforming CRS
#print(cities.crs) #returns the current layer crs
#Reproject (to_crs) and plot (plot) polygons
#cities.to_crs(epsg=4326).plot()
#Set equal axis
#lims = plt.axis('equal')
#plt.show()

##############################################################################################
#Composing multi-layer maps
#madrid = cities.loc[[12], :].to_crs(epsg=4326) #Madrid has an id of 12 in the Spanish cities dataset; here we select it, and convert it to a CRS that is in lat/long
#print(madrid)
#Below, we plot two layers: the madrid city polygon and the points of interest for the city 
#f, ax = plt.subplots(1)
#madrid.plot(ax=ax, color="yellow")
#pointsOfInterest.plot(ax=ax, color="green")
#plt.show()
#plt.savefig('madrid_bars.png', dpi=300) #This line will save the map to an image in the same folder where the code is hosted; the argument dpi allows you to set the resolution; however, I'm not sure where this saved it for me

##############################################################################################
#Manipulating spatial tables (GeoDataFrames)
#Area calculation
#print(cities.crs) #checking to make sure the polygons are projected in a crs that uses distance measurements
city_areas = cities.area
#print(city_areas.head())
city_areas_sqkm = city_areas / 1000000
#print(city_areas_sqkm.head()) 

#Length
#print(streets.crs) #checking to see what crs the streets dataset is in; it's in EPSG4326 which uses lat/long, so we'll reproject the layer into the local Spanish CRS (EPSG=25830) which uses distance measurements
street_length = streets.to_crs(epsg=25830).length
#print(street_length.head())

#Centroid calculation - a centroid is the spatial analog of the average of a polygon - used to summarize a polygon into a single point
cents = cities.centroid #This command returns a GeoSeries object (a single column with spatial data) with the centroids of a polygon GeoDataFrame - this can therefore be plotted directly, just like a table
#print(cents.head())
cents.plot()
#plt.show()

#Point in polygon (PiP) - Knowing whether a point is located inside a polygon - this can be done in GeoPandas using the contains method
polygon = cities.loc[12, 'geometry']
point1 = cents[0]
point2 = cents[112]
#print(polygon.contains(point1))
#print(polygon.contains(point2))
#A spatilal join is better used when there are many points and polygons to analyze

#Buffers
pointsOfInterest_reprojected = pointsOfInterest.to_crs(cities.crs)
#print(pointsOfInterest_reprojected.crs)
buffer = pointsOfInterest_reprojected.buffer(500) #creates a 500 meter buffer around every bar in Madrid
print(buffer.head())
f, ax = plt.subplots(1)
buffer.plot(ax=ax, linewidth=0)
pointsOfInterest_reprojected.plot(ax=ax, markersize=1, color='yellow') #plot bars on top of buffers
plt.show()

##############################################################################################
#Adding base layers from web sources