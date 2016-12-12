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

master = raw_input("What is the name of the master flat?")
dark = fits.open(master)
print dark[0].data
for i in range(len(f)):
    f[i][0].data = f[i][0].data / dark[0].data
    j = str(i)
    fir2 = fir.replace("*", "")
    fname = fir2 + "_fd_" + j + ".fit"
    f[i].writeto(fname)
