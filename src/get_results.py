def GetOutputNetcdf(outfilename,samplefilename,lat_grid,lon_grid,time_grid,pres_grid,u_grid,v_grid):

    # Next step: Write to new netcdf file
    outgrp = Dataset(outfilename, 'w', format='NETCDF3_CLASSIC')
    outgrp.createDimension('lon', len(lon_grid))
    outgrp.createDimension('lat', len(lat_grid))
    outgrp.createDimension('time', None)  # None: unlimited dimension

    # Create coordinate variables (w/ same names as dimensions)
    lonVar = outgrp.createVariable('lon', 'f4', ('lon',))  # f4: 32bit float
    latVar = outgrp.createVariable('lat', 'f4', ('lat',))  # f4: 32bit float
    timeVar = outgrp.createVariable('time', 'f8', ('time',))  # f8: 64bit float

    # Create variables w/ wind & pressure data
    presVar = outgrp.createVariable('PRES_L1', 'f4', ('time', 'lat', 'lon',))
    uVar = outgrp.createVariable('U_GRD_L103', 'f4', ('time', 'lat', 'lon',))
    vVar = outgrp.createVariable('V_GRD_L103', 'f4', ('time', 'lat', 'lon',))

    # Load first file to get variable attributes
    rootgrp = Dataset(samplefilename, "r")
    print(rootgrp.variables.keys())
    timeFirst = rootgrp.variables['time']
    lonFirst = rootgrp.variables['longitude']
    latFirst = rootgrp.variables['latitude']
    presFirst = rootgrp.variables['presmsl']
    uFirst = rootgrp.variables['u1min']
    vFirst = rootgrp.variables['v1min']

    lonVar.units = lonFirst.units
    latVar.units = latFirst.units
    timeVar.units = timeFirst.units
    presVar.units = presFirst.units
    uVar.units = uFirst.units
    vVar.units = vFirst.units

    lonVar.long_name = lonFirst.long_name
    latVar.long_name = latFirst.long_name
    timeVar.long_name = timeFirst.long_name
    presVar.long_name = presFirst.long_name
    uVar.long_name = uFirst.long_name
    vVar.long_name = vFirst.long_name

    timeVar.calendar = timeFirst.calendar
    timeVar.coordinate_defines = timeFirst.coordinate_defines

    rootgrp.close()

    # Write data to the new netcdf variables
    ref_time = "1900010100"
    ref_obj = datetime.strptime(ref_time, "%Y%m%d%H")
    time_final = []
    for t in time_grid:
        t_obj = datetime.strptime(t, "%Y%m%d%H")
        a = (t_obj - ref_obj).total_seconds() / 60.
        time_final.append(str(a))
    lonVar[:] = lon_grid
    latVar[:] = lat_grid
    timeVar[:] = time_final
    presVar[:, :, :] = pres_grid
    uVar[:, :, :] = u_grid
    vVar[:, :, :] = v_grid

    outgrp.close()

    return True

