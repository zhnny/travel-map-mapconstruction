from pyproj import Proj

changshaProj = Proj("epsg:4526")

import os
file = os.listdir('./jumpfilter')
trip_files = []
for trip_file in file:
    if trip_file.startswith('trip_'):
        trip_files.append(trip_file)
trip_files.__len__()

dir = './jumpfilter/'
for trip_file in trip_files:
    with open(dir+trip_file) as tf:
        # print(trip_file)
        tmp = []
        for trip_line in tf:
            point = trip_line.split(' ')
            lon,lat = changshaProj(float(point[1]),float(point[0]))
            tmp.append(str(lon)+' '+str(lat)+' '+str(point[2])+' '+str(point[3]))
        # print(tmp)
        if(len(tmp) > 1):
            with open('projection/'+trip_file,'w') as cf:
                cf.writelines(tmp)
            with open('projection/all.csv','a') as af:
                af.writelines(tmp)
        # print(trip_file)