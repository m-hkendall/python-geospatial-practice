# Questions to be answered from NFDB:
# 1. How many wildfires in Canada have occurred per decade
# 2. How many wildfires in Canada have occurred per decade and per size
# 3. How many wildfires occur in each month in Canada?
# 4. How many wildfires have occurred per decade and cause?
# 5. What is the number of wildfires that occurred per agency?

import os
import pandas as pd
import seaborn as sea
import matplotlib.pyplot as plt

db = pd.read_csv("C:\\Users\\maddy\\OneDrive\\Documents\\Github\\python-geospatial-practice\\data\\NFDB_point_20220901.csv") #need the double back-slashes to deal with unicode error;
#print(db.head())

wildfireTotalCountPerDecade = db.value_counts(subset='DECADE', sort=False)
print(wildfireTotalCountPerDecade)
wildfireTotalCountPerDecade_barChart = wildfireTotalCountPerDecade.plot.bar()
plt.title("Number of Canadian Wildfires Per Decade")
plt.xlabel("Decade")
plt.ylabel("Number of Wildfires")
plt.show()

