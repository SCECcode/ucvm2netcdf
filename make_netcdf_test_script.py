#!/bin/env python
#
#
# Purpose: Program showing how to write a NETCDF4 file for use by IRIS Paraview
# This inputs a list of UCVM ASCII files and outputs netcdf files that represent the model.
#
# Author: Philip Maechling
# Modification Date: 24 October 2018
#
#
import os
import sys
import time

import numpy as np
from netCDF4 import Dataset


def read_grid(grd_name,lat_steps,lon_steps,z_steps,lat_size,lon_size,z_size):
    #
    # This reads an ASCII grid file with material properties
    #

    #
    # This is returning a 1d array. Explanation is it thinks I'm specifying a structured array.
    # Until I get it to return a 2d array, I call split to find the columns
    queries = np.genfromtxt(grd_name, skip_header=0,usecols=(0, 1, 2, 14, 15, 16),dtype=float,autostrip=True)

    #
    # Now determine the depth increments using total lines divied by dlon * dlat
    #

    print("Total lon values:", lon_steps)
    print("Total lat values:", lat_steps)
    print("Total Depth Values:", z_steps)
    total_lines = len(queries)
    print("Total Lines from mesh file:", total_lines)
    calculated_lines = (lon_steps * lat_steps * z_steps)
    print("Calculated lines:", calculated_lines)
    if (total_lines != calculated_lines):
        print("Error matching number of lines in file (from params), (from file):",calculated_lines,total_lines)
        sys.exit(-1)
    #
    # Create a NetCDF3 file with this data
    #
    sname = os.path.splitext(grd_name)[0]
    fname = sname + ".nc"
    dataset = Dataset(fname, "w", format='NETCDF3_CLASSIC')

    #
    # Define Dataset fill on
    # Unclear the impact these have on results, so leave off
    #
    # dataset.set_auto_scale(True)
    # dataset.set_fill_on()

    #
    # Define 3D for volume mesh
    latitude = dataset.createDimension("latitude", lat_steps)
    longitude = dataset.createDimension("longitude", lon_steps)
    depth = dataset.createDimension("depth", z_steps)

    # print "Dimensions:", dataset.dimensions
    lats = dataset.createVariable("latitude", "f4", ("latitude",))
    lons = dataset.createVariable("longitude", "f4", ("longitude",))
    deps = dataset.createVariable("depth", "f4", ("depth",))

    vp = dataset.createVariable("vp", "f4", ("latitude", "longitude", "depth"))
    vs = dataset.createVariable("vs", "f4", ("latitude", "longitude", "depth"))
    rho = dataset.createVariable("rho", "f4", ("latitude", "longitude", "depth"))

    #
    # Define the Dataset global attributes
    #

    dataset.title = "Community Velocity Model - Harvard (CVM-H) v15.1"
    dataset.id = "SCEC_CVM_H_v15_1"
    dataset.summary = "CVM-H v15.1 is a 3D structural velocity model for the southern California crust and upper mantle. CVM-H v15.1 is comprised of detailed basin velocity descriptions based on tens of thousands of direct velocity (Vp, Vs) measurements and incorporates the locations and displacement of major fault zones that influence basin structure. These basin descriptions were used to developed tomographic models of crust and upper mantle velocity and density structure, which were subsequently iterated and improved using 3D waveform adjoint tomography."
    dataset.reference = "Shaw et al. (2015)"
    dataset.references = "https://doi.org/10.1016/j.epsl.2015.01.016"
    dataset.keywords = "seismic, shear wave, s wave, p wave, density, elastic waveform, tomography"
    dataset.Conventions = "CF-1.6"
    dataset.Metadata_Conventions = "Unidata Dataset Discovery v1.0"
    dataset.creator_name = "SCEC"
    dataset.creator_url = "https://www.scec.org/research/ucvm"
    dataset.creator_email = "maechlin@usc.edu"
    dataset.institution = "Southern California Earthquake Center (SCEC)"
    dataset.acknowledgment = "CVM-H v15.1 model development was lead by Department of Earth and Planetary Sciences, Harvard University"
    dataset.license = "These data may be redistributed and used without restriction."
    dataset.history = "CVM-H v15.1 model released 2015-01-15. NetCDF version created " + time.ctime(time.time())
    dataset.comment = "netCDF model extracted from CVM-H using UCVM and converted to netCDF by SCEC. CVM-H flags setting used are: cvmh_param=USE_1D_BKG,True and cvmh_param=USE_GTL,False"
    dataset.source = 'SCEC CVM-H v15.1 NetCDF file'

    dataset.geospatial_lat_min = 30.95
    dataset.geospatial_lat_max = 36.613
    dataset.geospatial_lat_units = "degrees_north"
    dataset.geospatial_lat_resolution = lat_size
    dataset.geospatial_lon_min = -120.862
    dataset.geospatial_lon_max = -113.333
    dataset.geospatial_lon_units = "degrees_east"
    dataset.geospatial_lon_resolution = lon_size
    dataset.geospatial_vertical_min = -50.0
    dataset.geospatial_vertical_max = 4.0
    dataset.geospatial_vertical_units = "km"
    dataset.geospatial_vertical_resolution = z_size
    dataset.geospatial_vertical_positive = "up"

    # Variabgle Attributes
    lats.units = 'degrees_north'
    lats.standard_name = 'latitude'
    lats.long_name = 'Latitude; positive north'

    lons.units = 'degrees_east'
    lons.standard_name = 'longitude'
    lons.long_name = 'Longitude; positive east'

    deps.units = 'km'
    deps.positive = 'up'
    deps.long_name = 'depth below sea level (bsl)'

    #
    #
    vp.long_name = "P Velocity"
    vp.display_name = "P Velocity (km/s)"
    vp.units = 'km.s-1'
    vp.valid_range = 0.0,10.0
    vp.missing_value = -99999.00


    vs.long_name = "S Velocity"
    vs.display_name = "S Velocity (km/s)"
    vs.units = 'km.s-1'
    vs.valid_range = 0.0,10.0
    vs.missing_value = -99999.00


    rho.long_name = "Density"
    rho.display_name = "Density (kg/m^3)"
    rho.units = 'kg.m-3'
    rho.valid_range = 0.000,10000.0
    rho.missing_value = -99999.00


    # Start with python array array creation formula
    x_lons = []
    y_lats = []
    z_depths = []

    #
    # Populate 3 lists of mesh points depth,lat,lo
    # Convert depth from m to km.
    #
    line_count = 0
    for sl in queries:
        if line_count < z_steps:
            elem = np.split(sl,6)
            z_depths.append((float(elem[2]) / 1000.0))
        line_count += 1

    line_count = 0
    for sl in queries:
        if ((line_count % z_steps) == 0) and (line_count < (z_steps * lat_steps)):
            elem = np.split(sl, 6)
            y_lats.append(float(elem[1]))
        line_count += 1

    line_count = 0
    for sl in queries:
        if line_count % (z_steps * lat_steps) == 0:
            elem = np.split(sl, 6)
            x_lons.append(float(elem[0]))
        line_count += 1

    #
    # Convert the single dim array into np array, and then into coordinate variables
    #
    lons[:] = np.array(x_lons)
    lats[:] = np.array(y_lats)
    deps[:] = np.array(z_depths)

    cur_line = 0
    for idlons in range(int(lon_steps)):
        for idlats in range(int(lat_steps)):
            for iddp in range(int(z_steps)):
                myline = queries[cur_line]
                cur_line += 1
                myelems = np.split(myline,6)
                #
                # Both vp and vs is a signal that the data is not defined for that point
                #
                if myelems[3] == 0 and myelems[4] == 0:
                    vp_value = -99999.0
                    vp[idlats, idlons, iddp] = vp_value
                    vs_value = -99999.0
                    vs[idlats, idlons, iddp] = vs_value
                    rho_value = -99999.0
                    rho[idlats, idlons, iddp] = rho_value
                else:
                    vp_value = (float(myelems[3]))
                    vp[idlats, idlons, iddp] = (vp_value/1000.0)
                    vs_value = (float(myelems[4]))
                    vs[idlats, idlons, iddp] = (vs_value/1000.0)
                    rho_value = (float(myelems[5]))
                    rho[idlats, idlons, iddp] = rho_value

    print("writing new netcdffile")
    dataset.close()

    # Notes on the formation of netcdf file format indicating the order of the variables.
    #
    # i.e. time varies most quickly? That is,
    # would I write a reading program specifying
    # u(time,depth,lat,lon)?
    # No.  The specifiers of the netCDF API were/are C programmers;
    # consequently, the leftmost dimension of a variable in the CDL file is the
    # grossest dimension and the rightmost dimension in the CDL file is the
    # finest.


if __name__ == "__main__":
    #
    #
    #
    # This script assumes the users has output a grid file,
    # which defines lat/lon/depth on a regular grid
    # and has called ucvm, using the grid file as input, and created a mesh file
    # A netcdf file inputs the mesh file, and converts it to a netcdf file,
    # and changes the name of the mesh file by adding a .nc extension
    # Use a full pathnames to simplify things
    # This current script assumes the hardcoded lat/lon/depth
    # This could be passed in, but is simplified here for testing.
    #
    # Define the mesh file to create a netcdf file
    # the output netcdf file will have the name of the mesh file, but with a .nc extension
    mesh_file_name = "/Users/maechlin/emc_files/cvms_output_mesh.txt"
    #
    # Define the dimensions of the region. These are from the CVM-H LR Model
    #
    #< coordinates >
    #-120.862028, 30.95649600000001, 0 - 120.862028, 36.612951, 0 - 113.33294, 36.612951,
    # 0 - 113.33294, 30.95649600000001, 0 - 120.862028, 30.95649600000001, 0
    #< / coordinates >
    #
    max_lon = -113.333
    min_lon = -120.862
    max_lat = 36.613
    min_lat = 30.956
    min_z = -50.0
    max_z = 4.0
    #
    # Select a number of points in the mesh in x, y, and z dimensions
    # These numbers were from estimates of the CVM-H LR in km (x,y) and 0.5km in z
    n_lon_steps = int(754)
    n_lat_steps = int(566)
    n_z_steps = int(109)

    #
    # This divides the dimension into even spaces, based on the n-steps
    # and the lat/lon/depths given above
    #
    lat_steps = np.linspace(min_lat, max_lat, n_lat_steps)
    lon_steps = np.linspace(min_lon, max_lon, n_lon_steps)
    z_steps = np.linspace(min_z, max_z, n_z_steps)

    n_pts = 0

    lat_size = lat_steps[1] - lat_steps[0]
    lon_size = lon_steps[1] - lon_steps[0]
    z_size = z_steps[1] - z_steps[0]

    print("lat_steps:", n_lat_steps)
    print("lat_size:", lat_size)
    print("lon_steps:",n_lon_steps)
    print("lon_size:", lon_size)
    print("z_steps:", n_z_steps)
    print("z_size (km):", z_size)
    n_pts = n_lat_steps * n_lon_steps * n_z_steps
    print("Number of pts:", n_pts)
    #sys.exit(0)
    #w
    # Create netCDF Files for SCEC CVM files
    #

    fin = mesh_file_name
    print("Reading cvm mesh file: ", fin)
    read_grid(fin,n_lat_steps,n_lon_steps,n_z_steps,lat_size,lon_size,z_size)
    print("Completed netCDF3 file creation file:", fin)

    print("Exiting Success")
    sys.exit(True)
