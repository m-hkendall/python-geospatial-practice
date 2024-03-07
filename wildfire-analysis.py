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
import numpy as np

db = pd.read_csv("C:\\Users\\maddy\\OneDrive\\Documents\\Github\\python-geospatial-practice\\data\\NFDB_point_20220901.csv") #need the double back-slashes to deal with unicode error;
#print(db.head())

#1. How many wildfires in Canada have occurred per decade?
wildfireTotalCountPerDecade = db.value_counts(subset='DECADE', sort=False)
#print(wildfireTotalCountPerDecade)
#wildfireTotalCountPerDecade_barChart = wildfireTotalCountPerDecade.plot.bar()
#plt.title("Number of Canadian Wildfires Per Decade")
#plt.xlabel("Decade")
#plt.ylabel("Number of Wildfires")
#plt.show()

#2. How many wildfires in Canada have occurred per decade and per size?
#wildfireTotalCountPerSize = db.value_counts(subset="SIZE_HA")
#print(wildfireTotalCountPerSize)
#The following code creates the Fire_Size_Brackets using the numpy.select method 
#wildfire_conditions = [
#    (db['SIZE_HA'] > 0) & (db['SIZE_HA'] <= 199),
#    (db['SIZE_HA'] > 200) & (db['SIZE_HA'] <= 999),
#    (db['SIZE_HA'] > 1000) & (db['SIZE_HA'] <= 9999),
#    (db['SIZE_HA'] > 10000) & (db['SIZE_HA'] <= 99999),
#    (db['SIZE_HA'] > 100000) & (db['SIZE_HA'] <= 499999),
#    (db['SIZE_HA'] > 500000) & (db['SIZE_HA'] <= 999999),
#    (db['SIZE_HA'] > 1000000)
#]
#wildfire_size_categories = [
#    '0-199 HA',
#    '200-999 HA',
#    '1,000-9,999 HA',
#    '10,000-99,999 HA',
#    '100,000-499,999 HA',
#    '500,000-999,999 HA',
#    '1,000,000+ HA'
#]
#db['Fire_Size_Bracket'] = np.select(wildfire_conditions, wildfire_size_categories)
#print(db)
#wildfireBySizeCategoryCount = db.value_counts(subset="Fire_Size_Bracket", sort=False)
#print(wildfireBySizeCategoryCount)

#pivot_table = pd.pivot_table(db[['DECADE', 'Fire_Size_Bracket']], index='DECADE', columns='Fire_Size_Bracket', aggfunc='size', fill_value=0, sort=False) #aggfunc 'size' gives the count of the incidences of fire_size_bracket per fire size bracket, thus giving the count of fire size with rows of decade and columns of fire size brackets
#pivot_table_sorted = pivot_table.sort_values(by="DECADE", ascending=True) #This sorts the index (rows) of the pivot table from earliest to most recent dates
#pivot_table_sorted = pivot_table.sort_index(axis=0).sort_index(axis=1)
#pivot_table_sorted = pivot_table_sorted.reindex(columns=pivot_table_sorted.columns.sort_values(ascending=False, key=lambda x: x != '1,000,000+ HA')) #This custom sorting function puts the troublesom "1,000,000+ HA" column at the end of the pivot table
#print(pivot_table_sorted)
#pivot_table_barChart = pivot_table_sorted.plot.bar()
#plt.title("Number of Wildfires in Canada by SIze and Decade")
#plt.xlabel("Decade")
#plt.ylabel("Number of fires")
#plt.legend(title="Wildfire Size in Hectares")
#plt.show()

# 3. How many wildfires occur in each month in Canada?
wildfireTotalCountPerMonth = db.value_counts(subset="MONTH", sort=False) #This code gives us the full count of wildfires per month, including those in the db where the month = 0

#We want to only look at the wildfires where the months are in the range of 1-12, or, January-December. 
monthMask = db['MONTH'] == 0 #Step 1: create a boolean mask for the rows to remove, i.e., the wildfires where the MONTH = 0
wildfireMonth_db = db[~monthMask] #Step 2: select all wildfires except the ones where the month = 0
wildfireMonth_db_TotalCountPerMonth = wildfireMonth_db.value_counts(subset="MONTH", sort=False) #Step 3: determine the new count of wildfires per month, where the months are 1-12
print(wildfireMonth_db_TotalCountPerMonth)
wildfireMonth_db_TotalCountPerMonth.plot.bar()
plt.title("Number of Wildfires in Canada by Month")
plt.xlabel("Month")
plt.ylabel("Number of fires")
plt.show()
