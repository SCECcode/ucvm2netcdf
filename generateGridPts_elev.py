"""
This script discritizes the CVM-H Low res region an counts the number of points
in the volume based on the discretizion size.
This will help determine the size of the netcdf files that we propose to generate
for the C

Proposed region is CVM-H LR region:

<coordinates>
          -120.862028,30.95649600000001,0 -120.862028,36.612951,0 -113.33294,36.612951,0 -113.33294,30.95649600000001,0 -120.862028,30.95649600000001,0
</coordinates>

"""
import numpy as np

import numpy as np
import sys

max_lon= -113.333
min_lon= -120.862
max_lat= 36.613
min_lat= 30.956
max_elev= 4000.0
min_elev= -15000.0

fout_name = "cvmh_elev_file.txt"

# Low Res Basins
n_lon_steps = int(377)
n_lat_steps = int(283)
n_elev_steps = int(191)

# Full Resolution
#n_lon_steps = int(754)
#n_lat_steps = int(566)
#n_elev_steps = 109

#lat_size: 0.010012389380531062
#lon_size: 0.009998671978749485
#z_steps: 495.0495049504951
#lon_size (km): 1.1098525896411928
#z_size (m): 495.0495049504951
#Number of pts: 43529928

lat_steps = np.linspace(min_lat,max_lat,n_lat_steps)
lon_steps = np.linspace(min_lon,max_lon,n_lon_steps)
z_steps = np.linspace(max_elev,min_elev,n_elev_steps)
print((z_steps))
print((n_lon_steps * n_lat_steps * n_elev_steps))
#sys.exit(0)

n_pts = 0
out_file = open(fout_name,"w")

#
# some of the model (cvms in particular) are much faster if you
# query the same point lat/lon for different depths, then
# move to new points. In this output file, the depth
# changes fastest so each point is queried 0-50000m
# before moving to next point
#
for x in lon_steps:
    for y in lat_steps:
        for z in z_steps:
            #print(x,y,z)
            out_file.write("{0:.3f} {1:0.3f} {2:d}\n".format(x,y,int(z)))
            n_pts += 1

out_file.close()
#
# approximate conversion from dd to km
#
#1° = 111 km  (or 60 nautical miles)
#0.1° = 11.1 km
#0.01° = 1.11 km (2 decimals, km accuracy)
#0.001° =111 m
#0.0001° = 11.1 m
#0.00001° = 1.11 m
#0.000001° = 0.11 m (7 decimals, cm accuracy)




lat_size = lat_steps[1] - lat_steps[0]
lon_size = lon_steps[1] - lon_steps[0]
z_size = z_steps[1] - z_steps[0]

print("lat_size:", lat_size)
print("lon_size:",lon_size)
print("z_steps:",z_size)

print("lon_size (km):",(lon_size/0.01) * 1.11)
print("z_size (m):",z_size)
print("Number of pts:",n_pts)
