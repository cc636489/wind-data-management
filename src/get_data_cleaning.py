def ProjectField2TargetMap(orglat,orglon,newlat,newlon,orgp,orgu,orgv):
    """

    Project field to the target geophysical map.

    Args:
        orglat (1darray): -90 ~ 90  ascending order.
        orglon (1darray): 0 ~ 360  ascending order.
        newlat (1darray): -90 ~ 90  ascending order.
        newlon (1darray): 0 ~ 360  ascending order.
        orgp (ndarray): orginal pressure field before projecting to new map.
        orgu (ndarray): orginal uwind field before projecting to new map.
        orgv (ndarray): orginal vwind field before projecting to new map.


    return:
        newp (ndarray): new pressure field after projecting to new map.
        newu (ndarray): new uwind field atfer projecting to new map.
        newv (ndarray): new vwind field atfer projecting to new map.

    """

    # Check whether orglat, orglon, newlat, newlon is inascending order.
    if all(np.sort(orglon) == orglon) and all(np.sort(orglat) == orglat) \
            and all(np.sort(newlon) == newlon) and all(np.sort(newlat) == newlat):
        pass
    else:
        print "ERROR: input orginal latlon or new latlon is not in ascending order!"
        sys.exit()

    f_p = interpolate.RectBivariateSpline(orglat,orglon,orgp)
    f_u = interpolate.RectBivariateSpline(orglat,orglon,orgu)
    f_v = interpolate.RectBivariateSpline(orglat,orglon,orgv)

    newp = f_p(newlat,newlon)
    newu = f_u(newlat,newlon)
    newv = f_v(newlat,newlon)

    return newp,newu,newv
