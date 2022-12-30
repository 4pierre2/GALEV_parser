#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 14:36:08 2022

@author: pierre
"""

import numpy as np
import glob


# Loading data

galevs = []
filenames = glob.glob('./MODEL/*spec.dat')
for filename in filenames:
    specs = np.loadtxt(filename)
    lam_galev = specs[:, 1]/1e4
    specs_galev = specs[:,2:]
    for spec in specs_galev.T:
        spec_t = spec*1e-7*1e4*4*3.1415*(10*3.0856e18)**2 # from erg s−1 cm−2 Å−1 at 10 pc to W.micron-1
        galevs.append(spec_t)
    ages_galev = np.arange(4e6, 1.6000000001e10, 4e6)
    
# Defining functions for parsing
    
def get_spec(age):
    x_age = np.argmin(abs(age-ages_galev))
    age_true = ages_galev[x_age]
    # print("Actual age: "+str(age_true))
    spec_age = galevs[x_age]
    return lam_galev, spec_age

def save_spec(age, filename='./spec_galev.dat'):
    lam, spec = get_spec(age)
    np.savetxt(filename, np.array([lam, spec]).T, delimiter=',')
    
# Examples
    
# save_spec(1.2e7, './12myr.dat')
# save_spec(4e7, './40myr.dat')
# save_spec(1e8, './100myr.dat')
# save_spec(1e10, './10gyr.dat')

l50, s50 = get_spec(5e7)
l5000, s5000 = get_spec(5e9)


    
import matplotlib.pyplot as plt
    
maxi = 0
for age in np.arange(20, 500, 4):
    lam, spec = get_spec(age*1e6)
    lam = lam[100:-10]
    spec = lam*spec[100:-10]
    if np.max(spec)>maxi:
        maxi = np.max(spec)
    
plt.ioff()
for age in np.arange(4, 500, 4):
    lam, spec = get_spec(age*1e6)
    lam = lam[100:-10]
    spec = lam*spec[100:-10]
    plt.plot(lam, spec)
    plt.loglog()
    plt.xlabel('Wavelength ($\mu m$)')
    plt.ylabel('$\lambda F_{\lambda}$ (W)')
    plt.ylim(maxi/300, maxi)
    plt.title('Age (Myr) : '+str(int(age)))
    plt.savefig('./forgif/'+'{:0>6}'.format(age)+'.png')
    plt.close()
import imageio
images = []
filenames = sorted(glob.glob('./forgif/*.png'))
for filename in filenames:
    images.append(imageio.imread(filename))
imageio.mimsave('./gif.gif', images)

