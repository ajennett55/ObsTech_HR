import glob
import astropy.io.fits as fits
import numpy as np
import time
import scipy.ndimage as ndimage
import skimage
from skimage.feature.register_translation import _upsampled_dft

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

for i in range(len(new)):
#    mf[i] = np.median(f[i][0].data)
#    f[i][0].data = f[i][0].data/mf[i]
#    print(np.median(f[i][0].data))
    g[i] = f[i][0].data
#    print g[i]

# Put the align stuff from class here and then do the mean combine. 
shift,error,diffphase=skimate.feature.reigster_translation(f[1][0].data,f[2][0].data,upsample_factor=100)
print shift,error

h = np.dstack((g))
mh = np.mean(h, axis =2)
f[0].data = mh

fname = raw_input("Enter a name for the new image: ")
f[0].writeto(fname)
