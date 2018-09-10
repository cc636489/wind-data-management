# A functional programming solution to manage time-space wind data.

This is a functional programming solution to joint two wind datasets, which come from 2 different resources. 

Achieved features: 
* Auto-data-cleaning: Imputed on missing values in both 2D space and time. 
* Auto-data-joint: Jointed two wind data sets from two different resources with three implemented methodologies.
* Scientific-data-I/O: output jointed wind data in standard scientific format, Netcdf4. 

## Dependencies:

This program requires Python2.7 and several packages installed: 

- Nio
- xarray
- re
- datatime
- scipy
- NetCDF4
- geopy

## Running recipes:

Modify `stdinput.py` to your needs, and simply run by:

        python main.py


## Test results:

Retrieved two different wind data sets from [GFS](https://www.ncdc.noaa.gov/data-access/model-data/model-datasets/global-forcast-system-gfs) database and [Hwind](http://www.rms.com/models/hwind) filesystem, respectively. See `Grab.f90`.

### Methodology 1: replace GFS with Hwind data set.
Here are how Hwind data and GFS data looks like:
<p align="center">
<img src="/doc/use_direct.png">
</p>


### Methodology 2: add Gaussian Filtering at interface of two data sets during replacing.
Here are how Hwind data and GFS data looks like:
<p align="center">
<img src="/doc/use_gaussian.png">
</p>


### Methodology 3: use weight function at interface of two data sets during replacing.
Here are how Hwind data and GFS data looks like:
<p align="center">
<img src="/doc/use_weight.png">
</p>


### Results: sequence wind data visualization.
Here is the sequence wind velocity profile during hurricane `Hermine` in 2016.
![Alt Text](https://github.com/cc636489/wind-data-management/raw/master/doc/wind_velocity_sequance_data.gif)



