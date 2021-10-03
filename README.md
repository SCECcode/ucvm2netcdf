# ucvm2netcdf
Scripts for creating netcdf format version of UCVM velocity model.

These files create netCDF versions of SCEC CVMs. These resulting netCDF files have been contributed to IRIS EMC
and to wave propagation modelers.

## Configuration
These scripts are used to output netcdf format velocity model files. These scripts use a netcdf python library.
IRIS provides an alternative netCDF generator that inputs CSV files, with metadata and outputs netCDF.

## Processing Summary
These scripts assume that the user has access to a working version of UCVM. The processing stages are:
(1) User rung "generateGridPts_depth.py" to generate a list of lat,lon, depths that will be used an inputs to UCVM.
This script discretizes a volume in southern California that matches the geographical coverage region of the CVM-H
low-resolution model, and a depth up to 54km. The horizontal spacking is 500m.

  - generateGridPts_depth.py
  - generateGridPts_elev.py

A second version of this script will discretize the same region, but will express the Z component at elevation.
This model defines pts from 4km above sea level, to 50km below sea level. Velocity models defined this way, will
define properties above sea level only for elevated regions. 

Both versions of these scripts outputs the mesh points that will be queried by the CVM.

(2) User runs UCVM, inputs the grid file created above, defines which CVM they want to query, and 
outputs a ucvm output file with  material properties, something like this. For recent models, we
have used the ucvm_docker images on ourlaptops to perfom this query. The current discrized models are about
4 million points, and the ucvm model query can take 30minutes.

$ ucvm_query -f ucvm.conf -m cvmh < socal_grid_pts_depth.txt > cvmh_depth_socal.txt

(3) User edits one of the make_xxx_nc.py scripts and specifies the input file name generated in the step above, 
that defines the material properties they want in the netCDF file. The make_xxx_nc.py scripts contains specific
metadata defining the models that area being created. The current version are throught be have correct metadata
but any updated input material properties files, may require the user to update the metadata.

  - make_cvmh_depth_nc.py
  - make_cvmh_elev_nc.py
  - make_cvms5_depth_nc.py
  - make_cvms4_depth_nc.py

## make_netcdf_test_script.py
A preliminary netcdf script that that worked at one point without full metadata

## Example Processing stages Using Docker
- Edit generateGridPts_depth.py to set n pts in each dimenion define the output file (e.g. cvm4_depth_file.txt)
- run generateGridPts_depth.py
- Used ucvm in docker to extract vp,vs, rho
- Start UCVM in Docker:
- Make sure Docker daemon is running
- docker run --rm -it --mount type=bind,source="$(pwd)"/target,destination=/app/target  sceccode/miniucvm:1.1
