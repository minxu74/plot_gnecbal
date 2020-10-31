#!/usr/bin/env python


import netCDF4 as nc4

import matplotlib as mpl
import matplotlib.pyplot as plt

import datetime
import numpy as np

import glob
import sys, cftime



#ilamb_root="/qfs/people/xumi699/scratch/proc_ilamb4xj/ilamb_wks/_build/EcosystemandCarbonCycle/GlobalNetEcosystemCarbonBalance"
ilamb_root="/qfs/people/xumi699/scratch/proc_ilamb4xj/ilamb_wks/_build_useneedirectly/"


ncfiles = glob.glob(ilamb_root + "/EcosystemandCarbonCycle/GlobalNetEcosystemCarbonBalance/GCP/*.nc")

print (ncfiles)



with nc4.Dataset("GCP_Benchmark.nc", "r") as newncf:

    xxnew = newncf.groups['MeanState'].variables['time_'][:] / 365. + 1851
    yynew = newncf.groups['MeanState'].variables['accumulate_of_nbp_over_global'][:] * (-1.)
    ybnew = newncf.groups['MeanState'].variables['accumulate_of_nbp_over_global_bnds'][:,0] * (-1.)
    ytnew = newncf.groups['MeanState'].variables['accumulate_of_nbp_over_global_bnds'][:,1] * (-1.)


fig, ax = plt.subplots()

for ncfile in ncfiles:
    print (ncfile)
    with nc4.Dataset(ncfile, 'r') as ncf:


         xx = ncf.groups['MeanState'].variables['time_'][:] / 365. + 1851
         yy = ncf.groups['MeanState'].variables['accumulate_of_nbp_over_global'][:] * (-1.)


         if 'Benchmark' in ncfile:
             ax.fill_between(xxnew, ybnew, ytnew, lw=0, color = 'k', alpha = 0.25)
             #ax.plot(xxnew, yynew, '--', color='black', label='Benchmark New')
             ax.plot(xx, yy, '-', color='black', label='Benchmark')

             
         elif 'CNP' in ncfile:
             ax.plot(xx, yy, '-', color='blue', label='ELMv1-CNP')
         elif 'CNonly' in ncfile:
             ax.plot(xx, yy, '-', color='red', label='ELMv1-CN')


         ax.set_xlabel("Year", fontsize="large", fontweight="bold")
         ax.set_xlim(1960, 2010)
         ax.set_ylabel("Accumulative land carbon sink (PgC)", fontsize="large", fontweight="bold")
         ax.set_ylim(-30, 80)

         ax.tick_params(labelsize='large', width=1)
         ax.legend(bbox_to_anchor=(0.05, 1), loc='upper left', borderaxespad=0.)

ax.hlines(0, 1850, 2010, colors='grey', linestyles='--')

plt.savefig("ngepbal_gcp_withuncertainty.png", dpi=300)
