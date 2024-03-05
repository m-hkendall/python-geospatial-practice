#This code follows the "Hands-On" tutorial of Section B - Open Science in the Geographic Data Science Course (ENVS363/563) at the University of Liverpool by Dr. Dani Arribas-Bel

import os
import pandas as pd
import seaborn as sea
import matplotlib.pyplot as plt

db = pd.read_csv("https://darribas.org/gds_course/content/data/liv_pop.csv",index_col='GeographyCode')
# read_csv is a pandas libary method that allows for reading csv files
# index_col is an argument that allows us to make the GeographyCode column the index of the table
# db is the object we store the data in; it allows us to save the result of read_csv; it is a data frame object that has two dimensions: rows and columns

#print(db) - This allows us to print the dataframe

#Inspecting what the dataset looks like
#print(db.head()) #this shows us the top five lines of the table
#print(db.tail()) #this shows the bottom five lines of the table
#print(db.info()) #this gives an overview of the table

#Describing the values and characteristics of the dataset
#print(db.describe()) #this gives some of the statistical (i.e., count, mean, standard deviation, min, max, etc.) values of the table
#print(db.describe().T) #this transposes the table
#print(db.min()) #this obtains minimum values for the table
#print(db['Europe'].min()) #this gives us the minimum values for the Europe column of the dataset
#pandas.DataFrame.loc: access a group of rows and columns by label(s) or a boolean array
#print(db.loc['E01006512', :].std()) #this gives the standard deviation for the E01006512 row of the dataset

#Creating new columns - generate new columns by applying operations to existing columns
#Ex. calculate total population by area
total = db['Europe'] + db['Africa'] + db['Middle East and Asia'] + db['The Americas and the Caribbean'] + db['Antarctica and Oceania'] #this is the longcoded version
#print(total.head())
total = db.sum(axis=1) #this is the short version - the sum function in this context gives us the total sum of population by areas
#print(total.head()) 
db['Total'] = total #this adds our total sum of population by areas calculations as a new column in the table
db.head()
#print(db.head())
#Ex. Generating new table values for a new column using scalars that can be modifed
#db['ones'] = 1
#db.head()
#print(db.head())
#db.loc['E01006512', 'ones'] = 3 #this changes the 1 value to a 3 in the row E01006512 and column 'ones'
#db.head()
#print(db.head())

#Delete columns
#del db['ones'] #This command deleted our 'ones' column
#print(db.head())

#Index-based queries
#Ex. List-based queries
#list_qry = db.loc[['E01006512', 'E01006513', 'E01006514', 'E01006515'], ['Total', 'Europe']] #this extracts the total and European population of the first four areas in the table; the square brackets delineate the index of the items we want in this subset - this is called a list-based query
#print(list_qry)
#Ex. Range-based queries - we give two indices and those, as well as any indices found within the range will also be returned
#range_qry = db.loc["E01006514":"E01006518","Europe":"Antarctica and Oceania"]
#print(range_qry)
#Ex. Combined list and range queries
#range_list_qry = db.loc["E01006514":"E01006518",["Europe","Total"]]
#print(range_list_qry)

#Condition-based queries
#Dataframes support data selection based on conditions, i.e., we don't know exactly what observations we want, but we do know what conditions they need to satisfy, e.g., areas with more than 2000 inhabitants
#Selecting areas with more than 2,500 people in Total:
#moreThan5000Total = db.loc[db['Total'] > 2500, :]
#print(moreThan5000Total)
#Selecting areas with no more than 750 Europeans:
#noMoreThan750Europeans = db.loc[db['Europe'] < 750, :]
#print(noMoreThan750Europeans)
#Selecting areas with exactly 10 persons from Antarctica and Oceania:
#exactly10AntarcticaAndOceania = db.loc[db['Antarctica and Oceania'] == 10, :]
#print(exactly10AntarcticaAndOceania)
#Selecting areas where European population is less than half the population:
#euLessThanHalfPopulation = db.loc[(db['Europe'] * 100. /db['Total']) < 50, :]
#print(euLessThanHalfPopulation)
# Querying the dataframe using the pandas.DataFrame.query operator
#moreThan2500Total_query = db.query("Total > 2500")
#print(moreThan2500Total_query)
#moreThan2500LessThan10000_query = db.query("(Total > 2500) & (Total < 10000)")
#print(moreThan2500LessThan10000_query)
#Combining queries
#Selecting areas with more than 25 people from the Americas and Carribean, but less than 1,500 in total:
#moreThan25AmericasCarribeanLessThan1500Total = db.loc[(db['The Americas and the Caribbean'] > 25) & (db['Total'] < 1500), :]
#print(moreThan25AmericasCarribeanLessThan1500Total)

#Sorting
#Sort the table by total population:
#db_population_sorted = db.sort_values('Total', ascending=True) #ascending=True == print smallest to largest; ascending=False == print largest to smallest
#db_population_sorted.head()
#print(db_population_sorted)

#Visualization
#histogram = sea.histplot(db['Total'], kde=False) #kde argument, a boolean, if True, will compute a kernel density estimate to smooth the distribution and show these lines on the plot
#plt.show() #this is the command to show the chart in a new window
#kernelDensityPlot = sea.kdeplot(db['Total'], shade=True) #a kernel desntiy estimator (KDE) plot is a method for visualizing the distribution of observations in a dataset, analogous to a histogram, though the KDE represents data using a continuous probability density curve; the shade parameter adds a shade under the curve
#plt.show()
#lineChart = db['Total'].sort_values(ascending=False).plot() #this produces a line plot
#plt.show()
#barChart = db['Total'].sort_values(ascending=False).head(10).plot.bar() #the head argument returns the first 10 rows of the dataset
#plt.show()
#barChartHorizontal = db['Total'].sort_values(ascending=False).head(10).plot.barh()
#plt.show()

#Un/tidy data
#What constitutes tidy data according to Hadley Wickham:
# 1. Each variable forms a column
# 2. Each observation forms a row
# 3. Each type of observational unit forms a table
print(db.head()) #this dataset has two observational units: GeographyCode, which gives the different areas of Liverpool, and the birth origin (subgroups) of an area
#Create two different tables, one containing the Total data and one containing the subgroup data
#Create a table "db_totals" that contains only the Total count of people for each geography code
db_totals = db[['Total']]
print(db_totals.head()) #db_totals is now a tidy table where each row is an observation, every variable forms a column, and there is only one observational unit in the table
#Create a table "db_subgroups" that contains the birth origin (subgroups) columns without "Totals"
db_subgroups = db.drop('Total', axis=1) #The drop function leaves db untouched, whereas if we had used the del function, the Totals column would have been permanently removed from db
print(db_subgroups.head()) #db_subgroups needs further cleaning because every row is not an observation, and because every column is not a variable
#Rearrange db_subgroups so that every row is a population subgroup in an area - we will do this by creating a pandas Series and then re-creating a data frame using the Series
tidy_subgroups = db_subgroups.stack() #the stack method stacks the different columns into rows
print(tidy_subgroups.head())
tidy_subgroupsDF = tidy_subgroups.reset_index() #this creates a DataFrame from a Series
print(tidy_subgroupsDF.head())
tidy_subgroupsDF = tidy_subgroupsDF.rename(columns={'level_1': 'Subgroup', 0: 'Freq'}) #This renames the columns 
print(tidy_subgroupsDF.head()) #This subgroups table is officially clean
#Grouping, transforming, aggregating


