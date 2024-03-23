#Code from: https://kpegion.github.io/Pangeo-at-AOES/examples/read-fortran-binary.html

import numpy as np
from array import array
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt

path = 'C:\\cygwin64\\snowmodel\\snowmodel-fraserexperimental-test1\\outputs\\wo_assim\\'
fname = 'swed.gdat'

nlons = 60 #from the swed.ctl file, xdef
nlats = 41 #from the swed.ctl file, ydef
neofs = 365 #from the swed.ctl file, tdef
nvars = 1 #from the swed.ctl file, vars
missing_value = -9999.0 #from the swed.ctl file, undef

lat = 41
lon = 60

#Define times as a pandas date range
eofs = np.arange(neofs)

#Define the length of each record
recl = (nlons*nlats*nvars*4)

#Create empty array to store the data
data = np.zeros((neofs,nlats,nlons,nvars))

#Read the data

luin = open(path+fname, 'rb')

#Loop over all times
for e in range(neofs):
    #Loop over all variables
    for v in range(nvars):
        #Read in fortran record in bytes
        tmp = luin.read(recl)
        #Convert to single precision (real 32bit)
        tmp1 = array('b', tmp)
        #Pull out data array
        tmp2 = tmp1[1:-1]
        #Create a 2d array (lat x lon) and store it in the data array
        data[e,:,:,v] = np.reshape(tmp2,(nlats,nlons))

#Extract variable
swed = data[:,:,:,0]

#Take care of missing data by setting it to NAN
swed[swed<=missing_value] = np.nan

#Put data into xarray.Dataset
swed_ds = xr.DataArray(swed,
                       coords={
                           'eofnum':eofs,
                           'lat':lat,
                           'lon':lon
                       },
                       dims=['eofnum','lat','lon'])
swed_ds = swed_ds.to_dataset(name='swed')

swed_ds = swed_ds.dropna(dim='lon', how='all')

print(swed_ds)


