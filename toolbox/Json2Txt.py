import os
file = os.listdir('./trackdata/origin/')
trip_files = []
for trip_file in file:
    if trip_file.startswith('trackjson'):
        trip_files.append(trip_file)
# print(trip_files)
trip_files.__len__()

import json
dir = './trackdata/origin/'
for file in trip_files:
    trackjson = json.loads(open(dir+file, 'r').read())
    tmp = []
    for track in trackjson:
        tmp.append(str(track[1]) + " " + str(track[2]) + " " + str(track[3]) + " " + str(int(track[0])) + "\n")
    with open("./trackdata/trip_" +  str(file[9:][:-5]) + ".txt","w") as tf:
        tf.writelines(tmp)