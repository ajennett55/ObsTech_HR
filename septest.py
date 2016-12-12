import numpy
import matplotlib.pyplot as plt
import astropy.io.fits as fits
import numpy as np
import sep
from matplotlib import rcParams
from matplotlib.patches import Ellipse

loga, logl, logte = numpy.loadtxt('isocz0.dat', usecols=(0, 3, 4), unpack=True)
w7 = numpy.where(loga == 10.10)
w8 = numpy.where(loga == 10.25)
#w8 = numpy.where(loga == 8.0)
plt.plot(logte[w7], logl[w7],label='12.6 Gyr')
plt.plot(logte[w8], logl[w8],label='17.8 Gyr')
plt.xlabel('Log(Teff)')
plt.ylabel('Log L')
plt.axis([5.0, 3.5, 0, 6])
plt.legend(loc='lower left')
plt.show()

izero = 23.849944552087
vzero = 24.166323443905
vo = fits.open('M2V.fit')
io = fits.open('M2Is.fit')

datav = vo[0].data
datav = datav.byteswap().newbyteorder()
bkgv = sep.Background(datav)
data_subv = datav - bkgv
VImag = []
Vmag = []
wVImag = []
wVmag = []


datai = io[0].data
datai = datai.byteswap().newbyteorder()
bkgi = sep.Background(datai)
data_subi = datai - bkgi

#Vobjects = sep.extract(data_subv, 1.5,deblend_cont=1, err=bkgv.globalrms)
Vobjects = sep.extract(data_subv, 1.5, err=bkgv.globalrms)
Iobjects = sep.extract(data_subi, 1.5, err=bkgi.globalrms)
#Iobjects = sep.extract(data_subi, 1.5, deblend_cont=1, err=bkgi.globalrms)
#objects = sep.extr
print len(Vobjects)
print len(Iobjects)
"""
# plot background-subtracted image
fig, ax = plt.subplots()
m, s = np.mean(data_subv), np.std(data_subv)
im = ax.imshow(data_subv, interpolation='nearest', cmap='gray', vmin=m-s, vmax=m+s, origin='lower')

# plot an ellipse for each object
for i in range(len(Vobjects)):
    e = Ellipse(xy=(Vobjects['x'][i], Vobjects['y'][i]), width=6*Vobjects['a'][i], height=6*Vobjects['b'][i], angle=Vobjects['theta'][i] * 180. / np.pi)
    e.set_facecolor('none')
    e.set_edgecolor('red')
    ax.add_artist(e)

plt.show()
"""
fluxv, fluxerrv, flag = sep.sum_circle(data_subv, Vobjects['x'], Vobjects['y'], 3.0, err=bkgv.globalrms, gain=1.0)
fluxi, fluxerri, flag = sep.sum_circle(data_subi, Iobjects['x'], Iobjects['y'], 3.0, err=bkgi.globalrms, gain=1.0)
"""
for i in range(len(Vobjects)):
    print("object {:d}: flux = {:f} +/- {:f}".format(i, fluxv[i], fluxerrv[i]))

for i in range(len(Iobjects)):
    print("object {:d}: flux = {:f} +/- {:f}".format(i, fluxi[i], fluxerri[i]))
"""
"""
fig, ax = plt.subplots()
m, s = np.mean(data_subv), np.std(data_subv)
im = ax.imshow(data_subv, interpolation='nearest', cmap='gray', vmin=m-s, vmax=m+s, origin='lower')
k=0
"""
for i in range (len(Vobjects)):
    for j in range(len(Iobjects)):
        if int(Vobjects[i]['x']) == int(Iobjects[j]['x']):
            if int(Vobjects[i]['y']) == int(Iobjects[j]['y']):
                #print(fluxv[i])
                magvi = (-2.5 * np.log10(fluxv[i]) + vzero) - (-2.5 * np.log10(fluxi[j]) + izero)
                magv = -2.5 * np.log10(fluxv[i]) + vzero
                VImag.append(magvi)
                Vmag.append(magv)
"""                if magvi < 0.8:
                    k+=1
                    e = Ellipse(xy=(Vobjects['x'][i], Vobjects['y'][i]), width=6*Vobjects['a'][i], height=6*Vobjects['b'][i], angle=Vobjects['theta'][i] * 180. / np.pi)
                    e.set_facecolor('none')
                    e.set_edgecolor('red')
                    ax.add_artist(e)

plt.show()
"""

distance = 10
distance_modulus = 5*np.log10(distance/10)

#print k
plt.scatter(VImag, Vmag)
plt.plot((-logte[w7]+5.05), -logl[w7]+16,label='10 Myr')
plt.plot(-logte[w8]+5.05, (-logl[w8]+16),label='100 Myr')
#plt.scatter(wVImag, wVmag)
plt.gca().invert_yaxis()
plt.xlabel("V-I")
plt.ylabel("V")
plt.show()
