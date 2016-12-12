import glob
import astropy.io.fits as fits
import numpy as np

# The dark subtraction for flats is included in this script

fir = raw_input("Give a wildcard: ")
#sec = raw_input("Give another wildcard: ")
types = [fir, '*fit']
files_grabbed = []
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

master = raw_input("What is the name of the master dark?")
dark = fits.open(master)
for i in range(len(f)):
    f[i][0].data = f[i][0].data - dark[0].data

for i in range(len(new)):
    mf[i] = np.median(f[i][0].data)
    f[i][0].data = f[i][0].data/mf[i]
#    print(np.median(f[i][0].data))
    g[i] = f[i][0].data+f[i][0].header['bzero']*1.
#    print g[i]

h = np.dstack((g))
mh = np.median(h, axis =2)
m = np.median(mh)
final = mh/m
f[0][0].data = final
f[0][0].header['bzero'] = 0
fname = raw_input("Enter a name for the new image: ")
f[0][0].writeto(fname)
