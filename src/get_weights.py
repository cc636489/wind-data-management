def r_base(lon_center,lat_center,lon1,lat1,lon2,lat2):
    point_center = (lat_center,lon_center)
    point1 = (lat_center,lon1)
    point2 = (lat_center,lon2)
    point3 = (lat1,lon_center)
    point4 = (lat2,lon_center)
    a = great_circle(point1, point_center).kilometers
    b = great_circle(point2, point_center).kilometers
    c = great_circle(point3, point_center).kilometers
    d = great_circle(point4, point_center).kilometers
    rbase = min(a,b,c,d)
    rmin = rbase*0.8 # decide the region of blend
    rmax = rbase # decide the region of blend
    return rmin,rmax

def r_map(latarr, lonarr, centerlat, centerlon):  # Simple lon/lat -> Distance function
    # Create 2D lon and lat arrays with meshgrid unless lonarr or latarr are 1D
    if len(lonarr) + len(latarr) > 2:
        longrid, latgrid = np.meshgrid(lonarr, latarr)
    else:
        # Both arrays are 1D, no need for meshgrid
        longrid = lonarr
        latgrid = latarr
    # Radius of Earth in meters
    RE = 6371000
    # Convert Degrees to Radians
    longrid = np.deg2rad(longrid)
    latgrid = np.deg2rad(latgrid)
    centerlon = np.deg2rad(centerlon)
    centerlat = np.deg2rad(centerlat)
    # Calculate differences
    dLon = longrid - centerlon
    dLat = latgrid - centerlat
    #xdistance = dLon * np.cos(centerlat) * RE
    #ydistance = dLat * RE
    # Calculate distance in kilometers
    distance = np.sqrt((dLon * np.cos(centerlat)) ** 2 + dLat ** 2) * RE
    distance = distance / 1000.
    return distance

def weight_map(rmin, rmax, rmap):
    w = np.zeros(rmap.shape)
    # Option1: exponential funtion
    # w[:] = np.exp(-10.*(r[:]-rmin)/(rmax-rmin))
    # Option2: Polynomial function, smooth at endpoint
    w[:] = 2* ((rmap[:] - rmin) / (rmax - rmin)) ** 3 - 3 * ((rmap[:] - rmin) / (rmax - rmin)) ** 2 + 1
    w[rmap <= rmin] = 1
    w[rmap >= rmax] = 0
    return w
