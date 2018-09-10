import sys
import numpy as np
import glob
import Nio
import xarray as xr
import re
from datetime import datetime,timedelta
from scipy import interpolate
from netCDF4 import Dataset
from geopy.distance import great_circle
import matplotlib.pyplot as plt
from stdinput import *
from get_data_cleaning import *
from get_data_joint import *
from get_data_sets import *
from get_initial import *
from get_results import *
from get_weights import *


def main():

    # Create target time step.
    [time_grid, nbtimestep] = CreateTargetTimeStep(start_date,end_date,time_spacing)

    # Create target geophysical map.
    [lat_grid,lon_grid] = CreateTargetGeoMap(latS,latN,lonW,lonE,latlen,lonlen)

    # Create target geophysical field.
    [pres_grid,u_grid,v_grid] = CreateTargetGeoField(nbtimestep,latlen,lonlen)

    # Get background and hwind file list.
    [backgformat,backgfulllist,backgtimelist_obj] = GetFileList(backgdir,backgstr)
    [hwindformat,hwindfulllist,hwindtimelist_obj] = GetFileList(hwinddir,hwindstr)

    for i in range(nbtimestep):

        targetimestep_obj = datetime.strptime(time_grid[i], '%Y%m%d%H')
        print "----start time step " + str(i) + ": " + str(targetimestep_obj) + "----"

        [backgstat,backguseonlybg,backgindex] = FindPlaceInSortedList(backgformat,targetimestep_obj,backgtimelist_obj)
        [hwindstat,hwinduseonlgbg,hwindindex] = FindPlaceInSortedList(hwindformat,targetimestep_obj,hwindtimelist_obj)

        if hwinduseonlgbg:
            print "target time step is outside hwind analysis time range, use only background file without blending!"
            [orgblat, orgblon, orgbp, orgbu, orgbv] = GetOrgFieldOnTargetTime(backgformat, backgstat, backgindex, backgfulllist,targetimestep_obj, backgtimelist_obj)
            [newbp, newbu, newbv] = ProjectField2TargetMap(orgblat, orgblon, lat_grid, lon_grid, orgbp, orgbu, orgbv)
            pres_grid[i, ...] = newbp
            u_grid[i, ...] = newbu
            v_grid[i, ...] = newbv
        else:
            print "target time step is inside hwind analysis time range, use both hwind and background field by blending!"
            [orgblat,orgblon,orgbp,orgbu,orgbv] = GetOrgFieldOnTargetTime(backgformat,backgstat,backgindex,backgfulllist,targetimestep_obj,backgtimelist_obj)
            [orghlat,orghlon,orghp,orghu,orghv] = GetOrgFieldOnTargetTime(hwindformat,hwindstat,hwindindex,hwindfulllist,targetimestep_obj,hwindtimelist_obj)

            [newbp,newbu,newbv] = ProjectField2TargetMap(orgblat,orgblon,lat_grid,lon_grid,orgbp,orgbu,orgbv)
            [newhp,newhu,newhv] = ProjectField2TargetMap(orghlat,orghlon,lat_grid,lon_grid,orghp,orghu,orghv)

            centerhwindindex = np.unravel_index(np.nanargmin(orghp), orghp.shape)
            centerlat = orghlat[centerhwindindex[0]]
            centerlon = orghlon[centerhwindindex[1]]
            wholemap = r_map(lat_grid,lon_grid,centerlat,centerlon)
            [rpresmin,rpresmax] = r_base(centerlon,centerlat,centerlon-box_deg_pres/2.,centerlat-box_deg_pres/2.,centerlon+box_deg_pres/2.,centerlat+box_deg_pres/2.)
            [ruvmin,ruvmax] = r_base(centerlon,centerlat,orghlon[0],orghlat[0],orghlon[-1],orghlat[-1])
            weightpres = weight_map(rpresmin,rpresmax,wholemap)
            weightuv = weight_map(ruvmin,ruvmax,wholemap)

            pres_grid[i, ...] = weightpres * newhp + (1 - weightpres) * newbp
            u_grid[i, ...] = weightuv * newhu + (1 - weightuv) * newbu
            v_grid[i, ...] = weightuv * newhv + (1 - weightuv) * newbv

        print "\n"

        pres_grid[i, ...] = np.flipud(pres_grid[i, ...])
#        u_grid[i, ...] = np.flipud(u_grid[i, ...] / 1.1)
#        v_grid[i, ...] = np.flipud(v_grid[i, ...] / 1.1)
        u_grid[i, ...] = np.flipud(u_grid[i, ...])
        v_grid[i, ...] = np.flipud(v_grid[i, ...])

    lat_grid = np.flipud(lat_grid)

    GetOutputNetcdf(outfilename,hwindfulllist[0],lat_grid,lon_grid,time_grid,pres_grid,u_grid,v_grid)

    return True

if __name__ == "__main__":
    print "Program Starts ..."
    main()
else:
    print "The script being imported as module. Some global variables is also imported in namespace!"
    sys.exit()

