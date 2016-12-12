import glob
import astropy.io.fits as fits
import numpy as np
import time

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
mf = ["" for j in range(len(new))]
g = [[] for j in range(len(new))]
#print len(new)
for i in range(len(new)):
    f[i] = fits.open(new[i])
    print f[i][0].header['bzero']
    g[i] = f[i][0].data+f[i][0].header['bzero']*1.
    f[i][0].header['bzero'] = 0
    print g[i]

master = raw_input("What is the name of the master dark?")
dark = fits.open(master)
for i in range(len(f)):
    print dark[0].data
    f[i][0].data = g[i] - dark[0].data
    j = str(i)
    fname = fir + "_ds_" + j + ".fit"
    f[i].writeto(fname)
