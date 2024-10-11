import json

path = "FieldEncountTable_d.json"

def check_slots(slots, name):
    for (i, e) in enumerate(slots):
            if e["maxlv"] != e["minlv"]:
                print("Level mismatch in zone {zone}, {type} slot {slot}... Minimum is {min} and maximum is {max}!".format(zone = j["zoneID"], type = name, slot = i, min = e["minlv"], max = e["maxlv"]))


json_file = open(path, 'r', encoding='utf-8')
json_data = json.load(json_file)
json_file.close()

for j in json_data["table"]:
    check_slots(j["ground_mons"], "Ground")
    check_slots(j["tairyo"], "Swarm")
    check_slots(j["day"], "Day")
    check_slots(j["night"], "Night")
    check_slots(j["swayGrass"], "Radar")
    check_slots(j["gbaRuby"], "Ruby")
    check_slots(j["gbaSapp"], "Sapphire")
    check_slots(j["gbaEme"], "Emerald")
    check_slots(j["gbaFire"], "FireRed")
    check_slots(j["gbaLeaf"], "LeafGreen")
    check_slots(j["water_mons"], "Surf")
    check_slots(j["boro_mons"], "Old Rod")
    check_slots(j["ii_mons"], "Good Rod")
    check_slots(j["sugoi_mons"], "Super Rod")
