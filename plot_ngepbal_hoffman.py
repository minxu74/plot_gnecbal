#!/usr/bin/env python


import netCDF4 as nc4

import matplotlib as mpl
import matplotlib.pyplot as plt

import datetime
import numpy as np

import glob
import sys, cftime



#ilamb_root="/qfs/people/xumi699/scratch/proc_ilamb4xj/ilamb_wks/_build/EcosystemandCarbonCycle/GlobalNetEcosystemCarbonBalance"
ilamb_root="/qfs/people/xumi699/scratch/proc_ilamb4xj/ilamb_wks/_build/"


ncfiles = glob.glob(ilamb_root + "/EcosystemandCarbonCycle/GlobalNetEcosystemCarbonBalance/Hoffman/*.nc")

print (ncfiles)


fig, ax = plt.subplots()

for ncfile in ncfiles:
    print (ncfile)
    with nc4.Dataset(ncfile, 'r') as ncf:


         xx = ncf.groups['MeanState'].variables['time_'][:] / 365. + 1851
         yy = ncf.groups['MeanState'].variables['accumulate_of_nbp_over_global'][:] * (-1.)


         if 'Benchmark' in ncfile:
             yb = ncf.groups['MeanState'].variables['accumulate_of_nbp_over_global_bnds'][:,0] * (-1.)
             yt = ncf.groups['MeanState'].variables['accumulate_of_nbp_over_global_bnds'][:,1] * (-1.)
             ax.fill_between(xx, yb, yt, lw=0, color = 'k', alpha = 0.25)
             ax.plot(xx, yy, '-', color='black', label='Benchmark')

             
         elif 'CNP' in ncfile:
             ax.plot(xx, yy, '-', color='blue', label='CNP')
         else:
             ax.plot(xx, yy, '-', color='red', label='CNonly')


         ax.set_xlabel("Year", fontsize="large", fontweight="bold")
         ax.set_xlim(1850, 2005)
         ax.set_ylabel("Accumulative land carbon sink (PgC)", fontsize="large", fontweight="bold")
         ax.set_ylim(-55, 25)

         ax.tick_params(labelsize='large', width=1)
         ax.legend(bbox_to_anchor=(0.05, 1), loc='upper left', borderaxespad=0.)

ax.hlines(0, 1850, 2005, colors='grey', linestyles='--')

plt.savefig("ngepbal_hoffman.png", dpi=300)
