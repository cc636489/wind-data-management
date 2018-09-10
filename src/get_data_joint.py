def ReadInOrgField(fileformat,filefullname):

    # lat = ["lat_0","lat_3"]
    # lon = ["lon_0","lon_3"]
    # pressure = ["PRMSL_P0_L101_GLL0","MSLET_P0_L101_GLL0","PRMSL_3_MSL"]
    # uwind = ["UGRD_P0_L103_GLL0","U_GRD_3_HTGL"]
    # vwind = ["VGRD_P0_L103_GLL0","V_GRD_3_HTGL"]

    if fileformat == "GRIB":
        orgdata = xr.open_dataset(filefullname, engine="pynio")
        if "gfsanl_4" in filefullname:
            orglat = orgdata.lat_0.values
            orglon = orgdata.lon_0.values
            try:
                orgp = orgdata.PRMSL_P0_L101_GLL0[:,:].values
            except AttributeError:
                print fileformat + ": AttributeError, try MSLET_P0_L101_GLL0, no PRMSL_P0_L101_GLL0 attributes in background file!"
                orgp = orgdata.MSLET_P0_L101_GLL0[:].values
            orgu = orgdata.UGRD_P0_L103_GLL0[:].values
            orgv = orgdata.VGRD_P0_L103_GLL0[:].values
        elif "gfsanl_3" in filefullname:
            orglat = orgdata.lat_3.values
            orglon = orgdata.lon_3.values
            orgp = orgdata.PRMSL_3_MSL[:].values
            orgu = orgdata.U_GRD_3_HTGL[:].values
            orgv = orgdata.V_GRD_3_HTGL[:].values
        else:
            print fileformat + ": ERROR: grib file get a new type of name. gfsanl_4 or gfsanl_3 is not in the file name any more!"
            sys.exit()
        orgdata.close()

    elif fileformat == "NETCDF":
        orgdata = Dataset(filefullname,"r")
        orglon = orgdata.variables['longitude'][:] + 360.  # boolean array set to nan
        orglat = orgdata.variables['latitude'][:]
        orgp = orgdata.variables['presmsl'][:]
        orgu = orgdata.variables['u1min'][:]
        orgv = orgdata.variables['v1min'][:]
        orgdata.close()

    else:
        print fileformat + ": ERROR: This isn't an GRIB file or NETCDF file . NOT considered yet."
        sys.exit()

    # Check if domain has abnormally filled with many zeros

    # Check org size, if matrix is in 3d, just keep the last 2d.
    if len(orgp.shape) == 3:
        orgp2d = orgp[0,:,:]
    elif len(orgp.shape) == 2:
        orgp2d = orgp[:,:]
    else:
        print fileformat + ": ERROR: pressure field is neither 2d nor 3d field! Check the original file!"

    if len(orgu.shape) == 3:
        orgu2d = orgu[0,:,:]
    elif len(orgu.shape) == 2:
        orgu2d = orgu[:, :]
    else:
        print fileformat + ": ERROR: uwind field is neither 2d nor 3d field! Check the original file!"

    if len(orgv.shape) == 3:
        orgv2d = orgv[0,:,:]
    elif len(orgv.shape) == 2:
        orgv2d = orgv[:, :]
    else:
        print fileformat + ": ERROR: vwind field is neither 2d nor 3d field! Check the original file!"

    # Check if orglat is in ascending order. Check this because of Projection requirement.
    if all(np.sort(orglat) == orglat):
        pass
    else:
        orglat = np.flipud(orglat)
        orgp2d = np.flipud(orgp2d)
        orgu2d = np.flipud(orgu2d)
        orgv2d = np.flipud(orgv2d)

    # Check if orglon is in ascending order.
    if all(np.sort(orglon) == orglon):
        pass
    else:
        orglon = np.fliplr(orglon)
        orgp2d = np.fliplr(orgp2d)
        orgu2d = np.fliplr(orgu2d)
        orgv2d = np.fliplr(orgv2d)


    return orglat,orglon,orgp2d,orgu2d,orgv2d

def GetOrgFieldOnTargetTime(fileformat,matchstat,fileindex,fullfilelist,targetimestep_obj,timefilelist_obj):

    if matchstat:
        print fileformat + ": target time step match!"
        # Read in orglat, orglon, orgu, orgv, orgp.
        [orglat,orglon,orgp,orgu,orgv] = ReadInOrgField(fileformat,fullfilelist[fileindex])

    else:
        print fileformat + ": target time step not match, do time interpolation!"

        # Read in closely two files, do time interpolation.
        [org1lat,org1lon,org1p,org1u,org1v] = ReadInOrgField(fileformat,fullfilelist[fileindex])
        [org2lat,org2lon,org2p,org2u,org2v] = ReadInOrgField(fileformat,fullfilelist[fileindex+1])

        # Calculate time weights.
        diff1 = abs(timedelta.total_seconds(targetimestep_obj - timefilelist_obj[fileindex]))
        diff2 = abs(timedelta.total_seconds(targetimestep_obj - timefilelist_obj[fileindex + 1]))
        timeweight = diff1 / (diff1 + diff2)

        # Check matrix size of those two bunch of files, if not the same, do space interpolation.
        if fileformat == "GRIB":
            if len(org1lat) == len(org2lat) and len(org1lon) == len(org2lon):

                # Make time averaging to lat lon field. Should remain the same.
                orglat = (1 - timeweight) * org1lat + timeweight * org2lat
                orglon = (1 - timeweight) * org1lon + timeweight * org2lon

                # Make time averaging to each field.
                orgp = (1 - timeweight) * org1p + timeweight * org2p
                orgu = (1 - timeweight) * org1u + timeweight * org2u
                orgv = (1 - timeweight) * org1v + timeweight * org2v

            else:
                print fileformat + ": ERROR: Detect domain matrix shape is changing! Abnormal cases! Check the original file!"
                sys.exit()

        elif fileformat == "NETCDF":
            print fileformat + ": Can't do time interpolation directly, size of Hwind field might change! Hwind field use moving mesh! Do space interpolation first!"
            print fileformat + ": WARNING: Don't take into account of curved storm track yet, right now track is set to be straight line!"

            # Make up the same matrix size and the same lat lon range of geo map for each time step.
            templatrange = min(max(org1lat)-min(org1lat),max(org2lat)-min(org2lat))
            templonrange = min(max(org1lon)-min(org1lon),max(org2lon)-min(org2lon))

            templatlen = max(len(org1lat),len(org2lat))
            templonlen = max(len(org1lon),len(org2lon))

            org1latcenter = np.mean(org1lat)
            org1loncenter = np.mean(org1lon)

            org1latmin = org1latcenter - templatrange / 2.
            org1latmax = org1latcenter + templatrange / 2.
            org1lonmin = org1loncenter - templonrange / 2.
            org1lonmax = org1loncenter + templonrange / 2.

            org2latcenter = np.mean(org2lat)
            org2loncenter = np.mean(org2lon)

            org2latmin = org2latcenter - templatrange / 2.
            org2latmax = org2latcenter + templatrange / 2.
            org2lonmin = org2loncenter - templonrange / 2.
            org2lonmax = org2loncenter + templonrange / 2.

            temp1latmap = np.linspace(org1latmin,org1latmax,templatlen)
            temp1lonmap = np.linspace(org1lonmin,org1lonmax,templonlen)

            temp2latmap = np.linspace(org2latmin,org2latmax,templatlen)
            temp2lonmap = np.linspace(org2lonmin,org2lonmax,templonlen)

            [temp1p,temp1u,temp1v] = ProjectField2TargetMap(org1lat,org1lon,temp1latmap,temp1lonmap,org1p,org1u,org1v)
            [temp2p,temp2u,temp2v] = ProjectField2TargetMap(org2lat,org2lon,temp2latmap,temp2lonmap,org2p,org2u,org2v)

            # Make time averaging to lat lon.
            orglat = (1 - timeweight) * temp1latmap + timeweight * temp2latmap
            orglon = (1 - timeweight) * temp1lonmap + timeweight * temp2lonmap

            # Make time averaging to each field.
            orgp = (1 - timeweight) * temp1p + timeweight * temp2p
            orgu = (1 - timeweight) * temp1u + timeweight * temp2u
            orgv = (1 - timeweight) * temp1v + timeweight * temp2v

        else:
            print "ERROR: This isn't an GRIB file or NETCDF file . NOT considered yet."
            sys.exit()

    return orglat,orglon,orgp,orgu,orgv
