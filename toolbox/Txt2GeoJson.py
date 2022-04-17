vertices_dict = {}
with open('./data/resultvertices.txt','r') as vertices:
    for line in vertices:
        tmp = line.split(',')
        vertices_dict[int(tmp[0])] = [float(tmp[1]),float(tmp[2][:-1])]

edge_arr = []
with open('./data/resultedges.txt','r') as edges:
    for line in edges:
        tmp = line.split(',')
        edge_arr.append([vertices_dict[int(tmp[1])],vertices_dict[int(tmp[2])]])

import os
import json

def save_trajs(data, path, type_style):
    res = {
        "type": "FeatureCollection",
        "features": []
    }
    for i, traj in enumerate(data):
        t = {
            "type": "Feature",
            "geometry": {
                "type": "LineString", "coordinates": traj
            },
            "properties": {
                "id": i
            }
        }

        res["features"].append(t)

    if os.path.exists(path):
        os.remove(path)
    with open(path, "w") as f:
        if type_style == "LineString":
            json.dump(res, f)
            
save_trajs(edge_arr, "./final_map.json", "LineString")