import glob
import astropy.io.fits as fits
import numpy as np
import time
"""
>>> f=fits.open("M2_I2_45s_ds_0.fit")
>>> f.header["BZERO"]

>>> f[0].header["BZERO"]

>>> print f[0].data

>>> f[0].data.dtype.name

>>> g=f[0].data+f[0].header['bzero]*1.

>>> g=f[0].data+f[0].header['bzero']*1.
>>> g

>>> f[0].data=g
>>> f[0].data

>>> f[0].header['bzero']

>>> f[0].header['bzero']=0
>>> f[0].header['bzero']=0
>>> f[0].header['bzero']

>>> f.write("test.fit")

>>> f.writeto("test.fit")
"""

fir = raw_input("Give a wildcard: ")
#sec = raw_input("Give another wildcard: ")
types = [fir, '*fit']
files_grabbed = []
t1=time.time()
for files in types:
    files_grabbed.extend(glob.glob(files))
new=[]
for i in range(len(files_grabbed)):
    for j in range(i+1, len(files_grabbed)):
        if files_grabbed[i] == files_grabbed[j]:
            new.append(files_grabbed[i])
f = [[] for j in range(len(new))]
g = [[] for j in range(len(new))]
#print len(new)
for i in range(len(new)):
    f[i] = fits.open(new[i])
    g[i] = f[i][0].data+f[i][0].header['bzero']*1.
    print f[i][0].header['bzero']
    print g[i]

h = np.dstack((g))
mh = np.median(h, axis =2)
f[0][0].data = mh
f[0][0].header['bzero'] = 0
fname = raw_input("Enter a name for the new image: ")
f[0].writeto(fname)
