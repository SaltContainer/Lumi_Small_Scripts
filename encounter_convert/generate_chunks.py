# THIS SCRIPT CONVERTS REWORKS THE DISTRIBUTIONTABLE MAP ZONES TO:
# - 0 IS AN EMPTY ZONE
# - 1-892 ARE EACH INDIVIDUAL MAP CHUNKS
# - 893+ ARE EACH ZONEID
# USE THIS TO ALLOW THE encount_convert.py SCRIPT TO PROPERLY ASSIGN MAP ZONES TO ENCOUNTERS

import json
import copy

dt_path = 'DistributionTable.json'
out_path = 'DistributionTable_out_chunks.json'

max_x = 33
max_y = 27

def load_distribution_file(path):
    with open(path) as dist_file:
        f0 = json.load(dist_file)
    return f0

def pad_or_truncate(list, target_len):
    return list[:target_len] + [empty_mapchunk()]*(target_len - len(list))

def output_distribution(path, dist):
    with open(path, 'w') as out_file:
        json.dump(dist, out_file, indent=4)

def empty_mapchunk():
    return copy.deepcopy({
        "MapID": 0,
        "LightUpGridXZ": [
            {
                "x": -1,
                "y": -1
            },
            {
                "x": -1,
                "y": -1
            },
            {
                "x": -1,
                "y": -1
            },
            {
                "x": -1,
                "y": -1
            },
            {
                "x": -1,
                "y": -1
            },
            {
                "x": -1,
                "y": -1
            },
            {
                "x": -1,
                "y": -1
            },
            {
                "x": -1,
                "y": -1
            },
            {
                "x": -1,
                "y": -1
            },
            {
                "x": -1,
                "y": -1
            },
            {
                "x": -1,
                "y": -1
            },
            {
                "x": -1,
                "y": -1
            },
            {
                "x": -1,
                "y": -1
            },
            {
                "x": -1,
                "y": -1
            },
            {
                "x": -1,
                "y": -1
            },
            {
                "x": -1,
                "y": -1
            },
            {
                "x": -1,
                "y": -1
            },
            {
                "x": -1,
                "y": -1
            },
            {
                "x": -1,
                "y": -1
            },
            {
                "x": -1,
                "y": -1
            },
            {
                "x": -1,
                "y": -1
            }
      ],
      "DistributionHideFlag": 0
    })

def generate_data(dist):
    new_dist = copy.deepcopy(dist)
    new_dist["MapDistribution"] = [empty_mapchunk()] * (max_x*max_y + 1)

    new_dist["MapDistribution"][0] = empty_mapchunk()

    for y in range(max_y):
        for x in range(max_x):
            id = y*max_x + x + 1
            new_dist["MapDistribution"][id] = empty_mapchunk()
            new_dist["MapDistribution"][id]["MapID"] = id
            new_dist["MapDistribution"][id]["LightUpGridXZ"][0]["x"] = x
            new_dist["MapDistribution"][id]["LightUpGridXZ"][0]["y"] = y
    return new_dist

def fix_x(dist):
    for map in range(1550):
        for xz in dist["MapDistribution"][map]["LightUpGridXZ"]:
            if xz["x"] != -1 or xz["y"] != -1:
                xz["x"] = xz["x"] + 1
    return dist

distribution = load_distribution_file(dt_path)
new_distribution = fix_x(distribution)
output_distribution(out_path, new_distribution)