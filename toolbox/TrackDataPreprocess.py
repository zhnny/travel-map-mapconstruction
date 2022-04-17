class MBR:
    def __init__(self, min_lat, min_lng, max_lat, max_lng):
        self.min_lat = min_lat
        self.min_lng = min_lng
        self.max_lat = max_lat
        self.max_lng = max_lng

    def contains(self, lat, lng):
        return self.min_lat <= lat < self.max_lat and self.min_lng <= lng < self.max_lng

big_MBR = MBR(28.14384, 112.85616, 28.21707, 112.96715)
small_MBR = MBR(28.170235, 112.917099, 28.203567, 112.943637)

import os
file = os.listdir('./trackdata')
trip_files = []
for trip_file in file:
    if trip_file.startswith('trip_'):
        trip_files.append(trip_file)
trip_files.__len__()

dir = './trackdata/'
for trip_file in trip_files:
    with open(dir+trip_file) as tf:
        # print(trip_file)
        tmp = []
        for trip_line in tf:
            point = trip_line.split(' ')
            if big_MBR.contains(float(point[0]),float(point[1])):
                tmp.append(trip_line)
        # print(len(tmp))
        if(len(tmp) > 1):
            with open(dir+'clip/'+trip_file,'w') as cf:
                cf.writelines(tmp)
            with open(dir+'clip/all.csv','a') as af:
                af.writelines(tmp)
        # print(trip_file)
        
import math
EARTH_MEAN_RADIUS_METER = 6371008.7714

class SPoint:
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng
    def __str__(self):
        return '({},{})'.format(self.lat, self.lng)
    def __eq__(self, other):
        return self.lat == other.lat and self.lng == other.lng
    
# returns the distance in meters between two points specified in degrees (Haversine formula).
def distance(a, b):
    return haversine_distance(a, b)

def haversine_distance(a, b):
    if a.__eq__(b):
        return 0.0
    delta_lat = math.radians(b.lat - a.lat)
    delta_lng = math.radians(b.lng - a.lng)
    h = math.sin(delta_lat / 2.0) * math.sin(delta_lat / 2.0) + math.cos(math.radians(a.lat)) * math.cos(
        math.radians(b.lat)) * math.sin(delta_lng / 2.0) * math.sin(delta_lng / 2.0)
    c = 2.0 * math.atan2(math.sqrt(h), math.sqrt(1 - h))
    d = EARTH_MEAN_RADIUS_METER * c
    return d

import os
file = os.listdir('./trackdata/clip/')
trip_files = []
for trip_file in file:
    if trip_file.startswith('trip_'):
        trip_files.append(trip_file)
trip_files.__len__()

dir = './trackdata/clip/'
MAX_SAPN = 20
for trip_file in trip_files:
    with open(dir+trip_file) as tf:
        # print(trip_file)
        tmp = []
        num = 0
        tag = ''
        lines = tf.readlines()
        for i in range(len(lines)-1):
            point1 = lines[i].split(' ')
            point2 = lines[i+1].split(' ')
            if distance(SPoint(float(point1[0]),float(point1[1])),SPoint(float(point2[0]),float(point2[1]))) < MAX_SAPN:
                tmp.append(lines[i])
            else:
                if(len(tmp) > 1):
                    if num > 0:
                        tag = '_' + str(num)
                    with open('./trackdata/'+'jumpfilter/'+trip_file[:-4]+tag+'.txt','w') as cf:
                        cf.writelines(tmp)
                    with open('./trackdata/'+'jumpfilter/all.csv','a') as af:
                        af.writelines(tmp)
                    num = num + 1
                tmp.clear()
        if(len(tmp) > 1):
            tmp.append(lines[len(lines)-1])
            if num > 0:
                tag = '_' + str(num)
            with open('./trackdata/'+'jumpfilter/'+trip_file[:-4]+tag+'.txt','w') as cf:
                cf.writelines(tmp)
            with open('./trackdata/'+'jumpfilter/all.csv','a') as af:
                af.writelines(tmp)