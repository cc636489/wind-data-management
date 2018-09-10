def GetFileList(filedir,filestr):

    # Get full input file list.
    fullfilelist = sorted( glob.glob(filedir + filestr) )
    nbfile = len(fullfilelist)

    # Check if we have the right path to the full file.
    if nbfile == 0 :
        print "ERROR: DON'T get the right path to glob files! EMPTY in the file list!"
        sys.exit()

    # Get the time of input file list.
    if ".grb" in filestr:
        fileformat = "GRIB"
        grblist = [re.search("\d\d\d\d\d\d\d\d_\d\d", fullfilelist[i]).group() for i in range(nbfile)]
        timefilelist = [''.join(grblist[i].split("_")) for i in range(nbfile)]
        timefilelist_obj = [datetime.strptime(timefilelist[i], '%Y%m%d%H') for i in range(nbfile)]

    elif ".nc" in filestr:
        fileformat = "NETCDF"
        timefilelist = [re.search("\d\d\d\d\d\d\d\d\d\d", fullfilelist[i]).group() for i in range(nbfile)]
        timefilelist_obj = [datetime.strptime(timefilelist[i], '%Y%m%d%H') for i in range(nbfile)]

    else:
        print "ERROR: This isn't an GRIB file or NETCDF file . NOT considered yet."
        sys.exit()

    return fileformat,fullfilelist,timefilelist_obj

def FindPlaceInSortedList(fileformat,target,list):
    """

    Find the right place to put target in an sorted list assumed in ascending order.

    Args:
        target (): One element of the same type in the list.
        list (sorted list): A list in ascending order.

    return:
        i:
        matchstat:
    """

    # Check the list to make sure it's in ascending order.
    if all(np.sort(list) == list):
        pass
    else:
        print "ERROR: timefilelist is not in ascending order!"
        sys.exit()

    # Find target in the list.
    for i in range(len(list)):

        if i == len(list)-1:
            if target == list[i]:
                matchstat = True
                useonlybackgstat = False
                return matchstat,useonlybackgstat,i
            else:
                if fileformat == "GRIB":
                    print "ERROR: target time step isn't within the filelist! Check startdate and endate! " \
                          "These dates should within the range of background field!"
                    sys.exit()
                elif fileformat == "NETCDF":
                    matchstat = False
                    useonlybackgstat = True
                    return matchstat,useonlybackgstat,i
                else:
                    pass

        else:
            if target == list[i]:
                matchstat = True
                useonlybackgstat = False
                return matchstat,useonlybackgstat,i
            elif target > list[i] and target < list[i+1]:
                matchstat = False
                useonlybackgstat = False
                return matchstat,useonlybackgstat,i
            else:
                pass
