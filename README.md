## ucvm2netcdf
These scripts are used to create netcdf format version of UCVM velocity model. 
These scripts use a netcdf python library to define format and metadata.
IRIS provides an alternative netCDF generator that inputs CSV files, with metadata and outputs netCDF.

## Processing Summary
These scripts assume that the user has access to a working version of UCVM. The processing stages are:

(1) The user runs one of the following "generateGridPts_depth.py" to generate a list of lat,lon, depths that 
will be used an inputs to UCVM. This script discretizes a volume in southern California that matches the geographical coverage region of the CVM-H
low-resolution model, and a depth up to 54km. The horizontal spacking is 500m. The output format is 
a three column, white space delimited, ASCII format with lat,lon, depth in decimal degrees, and 
depth in meters with one line per mesh point. A 4 million point query requires a 4M line input file:

-120.862 30.956 500

A second version of this script will discretize the same region, but will express the Z component at elevation.
This model defines pts from 4km above sea level, to 50km below sea level. Velocity models defined this way, will
define properties above sea level only for elevated regions. Both versions of these scripts outputs the mesh points that will be queried by the CVM.

  - generateGridPts_depth.py
  - generateGridPts_elev.py

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

## Prototype development
This contains a preliminary netcdf script that that worked at one point without full metadata. While developing the netCDF file
for IRIS, we used netCDF format checking programs to ensure we were creating valid netCDF format and metadata. Our scripts use a 
netCDF python interface. We also tested a netCDF creation program from IRIS that converts a CSV format volume and
a text metadata format to create a netCDF format.
- make_netcdf_test_script.py

## Example Processing stages Using Docker
- Configure to run UCVM on local computer using Dockerhub image:[SCEC UCVM Dockerimages](https://github.com/sceccode/ucvm_docker.git)
- Edit generateGridPts_depth.py to set n pts in each dimenion define the output file (e.g. cvm4_depth_file.txt)
- run generateGridPts_depth.py
- Used Docker version of ucvm extract vp,vs, rho and write ucvm output file
- run make_xxx_xxx_nc.py script to create output netCDF file. The output file name is the input file name, with a modified extension changed to .nc
- Use IDV viz tool to read in netCDF file and visualize the model coverage region, volume, and material properties
