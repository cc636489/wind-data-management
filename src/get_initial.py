def CreateTargetTimeStep(startdate, enddate, timespacing):
    """

    Creating Target output time steps.

    Args:
        startdate (str): output file start date.
        enddate (str): output file end date.
        timespacing (float): time period between each record, in hours.

    return:
        time_grid (list): target time step in format yyyymmddhh.
        nbtimestep(int): number of target time steps.

    """

    time_grid = []

    startdate_obj = datetime.strptime(startdate, '%Y%m%d%H')
    enddate_obj = datetime.strptime(enddate, '%Y%m%d%H')

    curdate_obj = startdate_obj

    while curdate_obj <= enddate_obj:
        curdate = datetime.strftime(curdate_obj, '%Y%m%d%H')
        time_grid.append(curdate)
        curdate_obj = curdate_obj + timedelta(hours=timespacing)

    nbtimestep = len(time_grid)

    return time_grid, nbtimestep

def CreateTargetGeoMap(latS, latN, lonW, lonE, latlen, lonlen):
    """

    Create target geophysical map with lat lon box in degree.

    Args:
        latS (float):south degree.
        latN (float):north degree.
        lonW (float):east degree.
        lonE (float):west degree.
        latlen (int):length of latitude.
        lonlen (int):length of longitude.

    return:
        lat_grid (1darray):latitudes in a row.
        lon_grid (1darray):longitudes in a row.

    """

    lat_grid = np.linspace(latS, latN, latlen)
    lon_grid = np.linspace(lonW, lonE, lonlen)

    return lat_grid,lon_grid

def CreateTargetGeoField(nbtimestep,latlen,lonlen):
    """

    Create target geophysical field, like mean sea level pressure, 10 meters wind speed.

    Args:
        nbtimestep (int):number of target time step.
        latlen (int):latitudes.
        lonlen (int):longitudes.

    return:
        pres_grid (ndarray):mean sea level pressure.
        u_grid (ndarray):10 meters uwind.
        v_grid (ndarray):10 meters vwind.

    """

    pres_grid = np.zeros((nbtimestep, latlen, lonlen))
    u_grid = np.zeros((nbtimestep, latlen, lonlen))
    v_grid = np.zeros((nbtimestep, latlen, lonlen))

    return pres_grid,u_grid,v_grid
