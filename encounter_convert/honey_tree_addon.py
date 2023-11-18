# THIS SCRIPT ADDS HONEY TREE ENCOUNTER DATA INTO DISTRIBUTIONTABLE.
# THIS EXPECTS THE JSON FORMAT USED BY THE LUMINESCENT EXLAUNCH EXEFS.
# USE THIS TO AUTOMATICALLY ADD HONEY TREE DATA TO THE DEX HABITAT SCREEN.

import json

honey_tree_path = 'HoneyTrees/zone_'
dt_path = 'DistributionTable.json'
out_path = 'DistributionTable_out.json'

dupe_to_pearl = True
dexsize = 1017

hardcoded_chunks = [
    [ 197, 571 ],
    [ 199, 471 ],
    [ 201, 502 ],
    [ 253, 535 ],
    [ 359, 569 ],
    [ 361, 440 ],
    [ 362, 573 ],
    [ 364, 639 ],
    [ 365, 643 ],
    [ 367, 647 ],
    [ 373, 549 ],
    [ 375, 449 ],
    [ 378, 445 ],
    [ 379, 677 ],
    [ 383, 812 ],
    [ 385, 784 ],
    [ 392, 654 ],
    [ 394, 521 ],
    [ 400, 663 ],
    [ 404, 868 ],
    [ 407, 723 ]
]

def load_honey_tree_file(zone):
    with open(honey_tree_path + str(zone) + '.json') as ht_file:
        f0 = json.load(ht_file)
    return f0

def load_distribution_file(path):
    with open(path) as dist_file:
        f0 = json.load(dist_file)
    return f0

def output_distribution(path, dist):
    with open(path, 'w') as out_file:
        json.dump(dist, out_file, indent=4)

def insert_zone_in_distributions(d, field, zone):
    if zone not in d[field]:
        d[field].append(zone)

def fill_empty_distributions(d):
    for category in d.values():
        if len(category) == 0:
            category.append(-1)

def clear_in_distributions(d, field):
    d[field] = []

def load_honey_tree_encounter():
    encs = []
    for (zone, chunk) in hardcoded_chunks:
        encs.append([chunk, load_honey_tree_file(zone)])
    return encs

def sort_encounters_by_poke(encs):
    new_encs = [[] for _ in range(dexsize+1)]
    for chunk, data in encs:
        for slot in data["slots"]:
            if slot["monsNo"] > 0:
                new_encs[slot["monsNo"]].append(("honey", chunk))
    return new_encs

def add_honey_tree_encounters(encs, dist):
    sorted_encs = sort_encounters_by_poke(encs)

    for i in range(dexsize+1):
        poke_d = dist["Diamond_FieldTable"][i]
        poke_d_dun = dist["Diamond_DungeonTable"][i]
        poke_p = dist["Pearl_FieldTable"][i]
        poke_p_dun = dist["Pearl_DungeonTable"][i]

        new_encs = sorted_encs[i]

        clear_in_distributions(poke_d, "HoneyTree")
        if dupe_to_pearl: clear_in_distributions(poke_p, "HoneyTree")

        for (enc_type, chunk) in new_encs:
            # Honey Tree encounters
            if enc_type == "honey":
                insert_zone_in_distributions(poke_d, "HoneyTree", chunk)
                if dupe_to_pearl: insert_zone_in_distributions(poke_p, "HoneyTree", chunk)
        
        fill_empty_distributions(poke_d)
        fill_empty_distributions(poke_d_dun)
        fill_empty_distributions(poke_p)
        fill_empty_distributions(poke_p_dun)
    
    return dist

encounters = load_honey_tree_encounter()
distribution = load_distribution_file(dt_path)
new_distribution = add_honey_tree_encounters(encounters, distribution)
output_distribution(out_path, new_distribution)