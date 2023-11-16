# THIS SCRIPT CONVERTS ENCOUNTER DATA FROM THE FIELDENCOUNT FORMAT TO THE DISTRIBUTIONTABLE FORMAT.
# USE THIS TO AUTOMATICALLY MAKE YOUR ENCOUNTER DATA VISIBLE IN THE DEX HABITAT SCREEN.

import json
import copy

enc_path = 'FieldEncountTable_d.json'
dt_path = 'DistributionTable.json'
out_path = 'DistributionTable_out.json'

gba_on = True
clear_distributions = True
clear_dun_distributions = True
dupe_to_pearl = True
dexsize = 1017
mapchunks = 891

def load_encounter_file(path):
    with open(path) as enc_file:
        f0 = json.load(enc_file)
    return f0

def load_distribution_file(path):
    with open(path) as dist_file:
        f0 = json.load(dist_file)
    return f0

def pad_or_truncate(list, target_len):
    return list[:target_len] + [empty_distribution()]*(target_len - len(list))

def convert_zone_id(zone):
    return zone + mapchunks + 1

def output_distribution(path, dist):
    with open(path, 'w') as out_file:
        json.dump(dist, out_file, indent=4)

def sort_encounters_by_poke(encs):
    new_encs = [[] for _ in range(dexsize+1)]
    for zone in encs["table"]:
        for i, ground_enc in enumerate(zone["ground_mons"]):
            if ground_enc["monsNo"] > 0:
                if i == 2 or i == 3:
                    new_encs[ground_enc["monsNo"] % 65536].append(("morning", zone["zoneID"]))
                else:
                    new_encs[ground_enc["monsNo"] % 65536].append(("ground", zone["zoneID"]))
        for swarm_enc in zone["tairyo"]:
            if swarm_enc["monsNo"] > 0:
                new_encs[swarm_enc["monsNo"] % 65536].append(("tairyo", zone["zoneID"]))
        for day_enc in zone["day"]:
            if day_enc["monsNo"] > 0:
                new_encs[day_enc["monsNo"] % 65536].append(("day", zone["zoneID"]))
        for night_enc in zone["night"]:
            if night_enc["monsNo"] > 0:
                new_encs[night_enc["monsNo"] % 65536].append(("night", zone["zoneID"]))
        for radar_enc in zone["swayGrass"]:
            if radar_enc["monsNo"] > 0:
                new_encs[radar_enc["monsNo"] % 65536].append(("swayGrass", zone["zoneID"]))
        
        for gba_ruby_enc in zone["gbaRuby"]:
            if gba_ruby_enc["monsNo"] > 0:
                new_encs[gba_ruby_enc["monsNo"] % 65536].append(("gbaRuby", zone["zoneID"]))
        for gba_sapp_enc in zone["gbaSapp"]:
            if gba_sapp_enc["monsNo"] > 0:
                new_encs[gba_sapp_enc["monsNo"] % 65536].append(("gbaSapp", zone["zoneID"]))
        for gba_eme_enc in zone["gbaEme"]:
            if gba_eme_enc["monsNo"] > 0:
                new_encs[gba_eme_enc["monsNo"] % 65536].append(("gbaEme", zone["zoneID"]))
        for gba_fire_enc in zone["gbaFire"]:
            if gba_fire_enc["monsNo"] > 0:
                new_encs[gba_fire_enc["monsNo"] % 65536].append(("gbaFire", zone["zoneID"]))
        for gba_leaf_enc in zone["gbaLeaf"]:
            if gba_leaf_enc["monsNo"] > 0:
                new_encs[gba_leaf_enc["monsNo"] % 65536].append(("gbaLeaf", zone["zoneID"]))
        
        for water_enc in zone["water_mons"]:
            if water_enc["monsNo"] > 0:
                new_encs[water_enc["monsNo"] % 65536].append(("water", zone["zoneID"]))
        for old_rod_enc in zone["boro_mons"]:
            if old_rod_enc["monsNo"] > 0:
                new_encs[old_rod_enc["monsNo"] % 65536].append(("boro", zone["zoneID"]))
        for good_rod_enc in zone["ii_mons"]:
            if good_rod_enc["monsNo"] > 0:
                new_encs[good_rod_enc["monsNo"] % 65536].append(("ii", zone["zoneID"]))
        for super_rod_enc in zone["sugoi_mons"]:
            if super_rod_enc["monsNo"] > 0:
                new_encs[super_rod_enc["monsNo"] % 65536].append(("sugoi", zone["zoneID"]))
    return new_encs

def empty_distribution():
    return copy.deepcopy({
        "BeforeMorning":[],
        "AfterMorning":[],
        "BeforeDaytime":[],
        "AfterDaytime":[],
        "BeforeNight":[],
        "AfterNight":[],
        "Fishing":[],
        "PokemonTraser":[],
        "HoneyTree":[],
    })

def insert_zone_in_distributions(d, field, zone):
    if zone not in d[field]:
        d[field].append(zone)

def fill_empty_distributions(d):
    for category in d.values():
        if len(category) == 0:
            category.append(-1)

def clear_in_distributions(d, field):
    d[field] = []

def convert_encounters(encs, dist):
    sorted_encs = sort_encounters_by_poke(encs)
    new_dist = copy.deepcopy(dist)
    
    new_dist["Diamond_FieldTable"] = pad_or_truncate(new_dist["Diamond_FieldTable"], dexsize+1)
    new_dist["Diamond_DungeonTable"] = pad_or_truncate(new_dist["Diamond_DungeonTable"], dexsize+1)
    new_dist["Pearl_FieldTable"] = pad_or_truncate(new_dist["Pearl_FieldTable"], dexsize+1)
    new_dist["Pearl_DungeonTable"] = pad_or_truncate(new_dist["Pearl_DungeonTable"], dexsize+1)

    for i in range(dexsize+1):
        if clear_distributions:
            new_dist["Diamond_FieldTable"][i] = empty_distribution()
        
        if clear_dun_distributions:
            new_dist["Diamond_DungeonTable"][i] = empty_distribution()

        if clear_distributions and dupe_to_pearl:
            new_dist["Pearl_FieldTable"][i] = empty_distribution()
        
        if clear_dun_distributions and dupe_to_pearl:
            new_dist["Pearl_DungeonTable"][i] = empty_distribution()

        poke_d = new_dist["Diamond_FieldTable"][i]
        poke_d_dun = new_dist["Diamond_DungeonTable"][i]
        poke_p = new_dist["Pearl_FieldTable"][i]
        poke_p_dun = new_dist["Pearl_DungeonTable"][i]

        new_encs = sorted_encs[i]

        for (enc_type, zone) in new_encs:
            if zone > 0:
                # Regular grass/cave and water
                if enc_type == "ground" or enc_type == "water":
                    insert_zone_in_distributions(poke_d, "BeforeMorning", convert_zone_id(zone))
                    if dupe_to_pearl: insert_zone_in_distributions(poke_p, "BeforeMorning", convert_zone_id(zone))
                    insert_zone_in_distributions(poke_d, "AfterMorning", convert_zone_id(zone))
                    if dupe_to_pearl: insert_zone_in_distributions(poke_p, "AfterMorning", convert_zone_id(zone))
                    insert_zone_in_distributions(poke_d, "BeforeDaytime", convert_zone_id(zone))
                    if dupe_to_pearl: insert_zone_in_distributions(poke_p, "BeforeDaytime", convert_zone_id(zone))
                    insert_zone_in_distributions(poke_d, "AfterDaytime", convert_zone_id(zone))
                    if dupe_to_pearl: insert_zone_in_distributions(poke_p, "AfterDaytime", convert_zone_id(zone))
                    insert_zone_in_distributions(poke_d, "BeforeNight", convert_zone_id(zone))
                    if dupe_to_pearl: insert_zone_in_distributions(poke_p, "BeforeNight", convert_zone_id(zone))
                    insert_zone_in_distributions(poke_d, "AfterNight", convert_zone_id(zone))
                    if dupe_to_pearl: insert_zone_in_distributions(poke_p, "AfterNight", convert_zone_id(zone))
                # Morning only
                elif enc_type == "morning":
                    insert_zone_in_distributions(poke_d, "BeforeMorning", convert_zone_id(zone))
                    if dupe_to_pearl: insert_zone_in_distributions(poke_p, "BeforeMorning", convert_zone_id(zone))
                    insert_zone_in_distributions(poke_d, "AfterMorning", convert_zone_id(zone))
                    if dupe_to_pearl: insert_zone_in_distributions(poke_p, "AfterMorning", convert_zone_id(zone))
                # Mid-day only
                elif enc_type == "day":
                    insert_zone_in_distributions(poke_d, "BeforeDaytime", convert_zone_id(zone))
                    if dupe_to_pearl: insert_zone_in_distributions(poke_p, "BeforeDaytime", convert_zone_id(zone))
                    insert_zone_in_distributions(poke_d, "AfterDaytime", convert_zone_id(zone))
                    if dupe_to_pearl: insert_zone_in_distributions(poke_p, "AfterDaytime", convert_zone_id(zone))
                # Night only
                elif enc_type == "night":
                    insert_zone_in_distributions(poke_d, "BeforeNight", convert_zone_id(zone))
                    if dupe_to_pearl: insert_zone_in_distributions(poke_p, "BeforeNight", convert_zone_id(zone))
                    insert_zone_in_distributions(poke_d, "AfterNight", convert_zone_id(zone))
                    if dupe_to_pearl: insert_zone_in_distributions(poke_p, "AfterNight", convert_zone_id(zone))
                # Swarm
                elif enc_type == "tairyo":
                    insert_zone_in_distributions(poke_d, "BeforeMorning", convert_zone_id(zone))
                    if dupe_to_pearl: insert_zone_in_distributions(poke_p, "BeforeMorning", convert_zone_id(zone))
                    insert_zone_in_distributions(poke_d, "AfterMorning", convert_zone_id(zone))
                    if dupe_to_pearl: insert_zone_in_distributions(poke_p, "AfterMorning", convert_zone_id(zone))
                    insert_zone_in_distributions(poke_d, "BeforeDaytime", convert_zone_id(zone))
                    if dupe_to_pearl: insert_zone_in_distributions(poke_p, "BeforeDaytime", convert_zone_id(zone))
                    insert_zone_in_distributions(poke_d, "AfterDaytime", convert_zone_id(zone))
                    if dupe_to_pearl: insert_zone_in_distributions(poke_p, "AfterDaytime", convert_zone_id(zone))
                    insert_zone_in_distributions(poke_d, "BeforeNight", convert_zone_id(zone))
                    if dupe_to_pearl: insert_zone_in_distributions(poke_p, "BeforeNight", convert_zone_id(zone))
                    insert_zone_in_distributions(poke_d, "AfterNight", convert_zone_id(zone))
                    if dupe_to_pearl: insert_zone_in_distributions(poke_p, "AfterNight", convert_zone_id(zone))
                # Poké Radar
                elif enc_type == "swayGrass":
                    insert_zone_in_distributions(poke_d, "PokemonTraser", convert_zone_id(zone))
                    if dupe_to_pearl: insert_zone_in_distributions(poke_p, "PokemonTraser", convert_zone_id(zone))
                # GBA Slots
                elif gba_on and (enc_type == "gbaRuby" or enc_type == "gbaSapp" or enc_type == "gbaEme" or enc_type == "gbaFire" or enc_type == "gbaLeaf"):
                    insert_zone_in_distributions(poke_d, "BeforeMorning", convert_zone_id(zone))
                    if dupe_to_pearl: insert_zone_in_distributions(poke_p, "BeforeMorning", convert_zone_id(zone))
                    insert_zone_in_distributions(poke_d, "AfterMorning", convert_zone_id(zone))
                    if dupe_to_pearl: insert_zone_in_distributions(poke_p, "AfterMorning", convert_zone_id(zone))
                    insert_zone_in_distributions(poke_d, "BeforeDaytime", convert_zone_id(zone))
                    if dupe_to_pearl: insert_zone_in_distributions(poke_p, "BeforeDaytime", convert_zone_id(zone))
                    insert_zone_in_distributions(poke_d, "AfterDaytime", convert_zone_id(zone))
                    if dupe_to_pearl: insert_zone_in_distributions(poke_p, "AfterDaytime", convert_zone_id(zone))
                    insert_zone_in_distributions(poke_d, "BeforeNight", convert_zone_id(zone))
                    if dupe_to_pearl: insert_zone_in_distributions(poke_p, "BeforeNight", convert_zone_id(zone))
                    insert_zone_in_distributions(poke_d, "AfterNight", convert_zone_id(zone))
                    if dupe_to_pearl: insert_zone_in_distributions(poke_p, "AfterNight", convert_zone_id(zone))
                # Fishing
                elif enc_type == "boro" or enc_type == "ii" or enc_type == "sugoi":
                    insert_zone_in_distributions(poke_d, "Fishing", convert_zone_id(zone))
                    if dupe_to_pearl: insert_zone_in_distributions(poke_p, "Fishing", convert_zone_id(zone))
        
        fill_empty_distributions(poke_d)
        fill_empty_distributions(poke_d_dun)
        fill_empty_distributions(poke_p)
        fill_empty_distributions(poke_p_dun)
    
    return new_dist

encounters = load_encounter_file(enc_path)
distribution = load_distribution_file(dt_path)
new_distribution = convert_encounters(encounters, distribution)
output_distribution(out_path, new_distribution)