import json

indexdata_json = "./input/SearchIndexData_TR.json"
initial_json = "./input/trad_chinese_ss_initial.json"
monsname_json = "./input/trad_chinese_ss_monsname.json"
itemname_json = "./input/trad_chinese_ss_itemname.json"
movename_json = "./input/trad_chinese_ss_wazaname.json"
abilityname_json = "./input/trad_chinese_ss_tokusei.json"
trad_chinese_ordering = "./input/trad_chinese_ordering.json"
output = "./output/SearchIndexData_TR.json"

def find_trad_chinese_grouping(array, char):
    for (i, grouping) in enumerate(array):
        for j, grouping_char in enumerate(grouping):
            if grouping_char == char:
                return (i, j)
    
    print("Missing character in ordering: " + char)
    return (-1, -1)

def find_trad_chinese_grouping_of_word(array, word):
    groupings = []
    for char in word:
        groupings.append(find_trad_chinese_grouping(array, char))
    
    return groupings

def find_label_in_label_array(array, label_name):
    for label in array:
        if label["labelName"] == label_name:
            return label["wordDataArray"][0]["str"]
    
    return ""

indexdata_json_file = open(indexdata_json, 'r', encoding='utf-8')
indexdata_json_data = json.load(indexdata_json_file)
indexdata_json_file.close()

initial_json_file = open(initial_json, 'r', encoding='utf-8')
initial_json_data = json.load(initial_json_file)
initial_json_file.close()

monsname_json_file = open(monsname_json, 'r', encoding='utf-8')
monsname_json_data = json.load(monsname_json_file)
monsname_json_file.close()

itemname_json_file = open(itemname_json, 'r', encoding='utf-8')
itemname_json_data = json.load(itemname_json_file)
itemname_json_file.close()

movename_json_file = open(movename_json, 'r', encoding='utf-8')
movename_json_data = json.load(movename_json_file)
movename_json_file.close()

abilityname_json_file = open(abilityname_json, 'r', encoding='utf-8')
abilityname_json_data = json.load(abilityname_json_file)
abilityname_json_file.close()

trad_chinese_ordering_file = open(trad_chinese_ordering, 'r', encoding='utf-8')
trad_chinese_ordering_data = json.load(trad_chinese_ordering_file)
trad_chinese_ordering_file.close()

indexdata_json_data["MonsterName"] = []
monsname_groupings = []
indexdata_json_data["WazaName"] = []
movename_groupings = []
indexdata_json_data["Tokusei"] = []
abilityname_groupings = []
indexdata_json_data["ItemName"] = []
itemname_groupings = []

# Mons
for mon in monsname_json_data["labelDataArray"][1:]:
    name = mon["wordDataArray"][0]["str"]
    monsname_groupings.append((mon["labelName"], find_trad_chinese_grouping_of_word(trad_chinese_ordering_data["stroke_strings"], name)))

monsname_groupings.sort(key=lambda mg: [(g[0], g[1]) for g in mg[1]])
for (monlabel, groupings) in monsname_groupings:
    #print("[" + monlabel + "] " + find_label_in_label_array(monsname_json_data["labelDataArray"], monlabel) + ": " + str(groupings))
    indexdata_json_data["MonsterName"].append({ "MessageID": monlabel, "IndexGroup": groupings[0][0] })

# Moves
for move in movename_json_data["labelDataArray"][1:]:
    name = move["wordDataArray"][0]["str"]
    movename_groupings.append((move["labelName"], find_trad_chinese_grouping_of_word(trad_chinese_ordering_data["stroke_strings"], name)))

movename_groupings.sort(key=lambda mg: [(g[0], g[1]) for g in mg[1]])
for (movelabel, groupings) in movename_groupings:
    indexdata_json_data["WazaName"].append({ "MessageID": movelabel, "IndexGroup": groupings[0][0] })

# Abilities
for ability in abilityname_json_data["labelDataArray"][1:]:
    name = ability["wordDataArray"][0]["str"]
    abilityname_groupings.append((ability["labelName"], find_trad_chinese_grouping_of_word(trad_chinese_ordering_data["stroke_strings"], name)))

abilityname_groupings.sort(key=lambda mg: [(g[0], g[1]) for g in mg[1]])
for (abilitylabel, groupings) in abilityname_groupings:
    indexdata_json_data["Tokusei"].append({ "MessageID": abilitylabel, "IndexGroup": groupings[0][0] })

# Items
for item in itemname_json_data["labelDataArray"][1:]:
    name = item["wordDataArray"][0]["str"]
    itemname_groupings.append((item["labelName"], find_trad_chinese_grouping_of_word(trad_chinese_ordering_data["stroke_strings"], name)))

itemname_groupings.sort(key=lambda mg: [(g[0], g[1]) for g in mg[1]])
for (itemlabel, groupings) in itemname_groupings:
    indexdata_json_data["ItemName"].append({ "MessageID": itemlabel, "IndexGroup": groupings[0][0] })

output_json_file = open(output, 'w', encoding='utf-8')
json.dump(indexdata_json_data, output_json_file, ensure_ascii=False, indent=4)
output_json_file.close()
