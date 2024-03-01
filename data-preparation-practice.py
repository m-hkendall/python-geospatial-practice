#This code follows the "Hands-On" tutorial of Section B - Open Science in the Geographic Data Science Course (ENVS363/563) at the University of Liverpool by Dr. Dani Arribas-Bel

import os
import pandas as pd
import seaborn as sea

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
#print(db.loc['E01006512', :].std()) #this gives the standard deviation for the E01006512 row of the dataset

#Creating new columns - generate new columns by applying operations to existing columns
#Ex. calculate total population by area
#total = db['Europe'] + db['Africa'] + db['Middle East and Asia'] + db['The Americas and the Caribbean'] + db['Antarctica and Oceania'] #this is the longcoded version
#print(total.head())
#total = db.sum(axis=1) #this is the short version - the sum function in this context gives us the total sum of population by areas
#print(total.head()) 
#db['Total'] = total #this adds our total sum of population by areas calculations as a new column in the table
#db.head()
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

