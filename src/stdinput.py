# =============================== User Inputs =========================================
box_deg_pres = 3.

dir = "2008-Ike"
backgdir = "/mnt/gpfs/nobackup/surge/chenchen/"+dir+"/"+dir+"-gfs/"
#backgdir = "/Users/cchen/PycharmProjects/3-Blend_winds/" + dir + "-gfs/"

backgstr = "*.grb*"

hwinddir = "/mnt/gpfs/nobackup/surge/chenchen/"+dir+"/"+dir+"-hwind-addpressure/"
#hwinddir = "/Users/cchen/PycharmProjects/3-Blend_winds/" + dir + "-hwind-addpressure/"

hwindstr = "*.nc"

time_spacing = 3.
start_date = "2008090500"
end_date = "2008091500"

lonE = 324.  # for CFSR format output, lon range is in 0~360
lonW = 258.
latN = 50.  # for CFSR format output, lat grid should descending
latS = 5.
latlen = 801
lonlen = 1321

outfilename = "/mnt/gpfs/nobackup/surge/chenchen/" + dir + "_hwind_gfs_forMike_" + start_date + "to" + end_date + "_nc3_without_factor.nc"
# =============================== User Inputs =========================================

