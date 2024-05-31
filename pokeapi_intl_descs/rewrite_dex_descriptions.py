# THIS SCRIPT OBTAINS INTERNATIONAL POKÉDEX ENTRIES FOR EACH POKÉMON AND FILLS OUT COMMON_MSBT WITH THEM
# USE THIS TO FILL OUT DEX ENTRIES FOR EACH LANGUAGE IN THE POKÉDEX

import json
import copy
import pokebase as pb

from utils.str_calc import calculate, loadKey

lang_index = 8

from_file = True

dia_file = "dp_pokedex_diamond.json"
prl_file = "dp_pokedex_pearl.json"

pokeapi_file = "pokapi_entries.json"


languages = [
    ("french", "fr"),
    ("german", "de"),
    ("italian", "it"),
    ("jpn", "ja-Hrkt"),
    ("jpn_kanji", "ja"),
    ("korean", "ko"),
    ("simp_chinese", "zh-Hans"),
    ("trad_chinese", "zh-Hant"),
    ("spanish", "es"),
]

game_priority = [
    "sword", "shield",
    "ultra-sun", "ultra-moon",
    "sun", "moon",
    "omega-ruby", "alpha-sapphire",
    "x", "y",
    "black-2", "white-2",
    "black", "white"
]

placeholder_word = {
    "patternID": 0,
    "eventID": 0,
    "tagIndex": -1,
    "tagValue": 0.0,
    "str": "",
    "strWidth": 0.0
}


def load_files(inputs, outputs):
    input_files = []
    for input in inputs:
        input_files.append(open('input/' + input, encoding='utf-8'))

    output_files = []
    for output in outputs:
        output_files.append(open('output/' + output, "w", encoding='utf-8', newline=''))
    
    return (input_files, output_files)

def close_files(files):
    for file in files:
        file.close()

def get_pokeapi_description(monsno, language_idx):
    try:
        poke = pb.APIResource('pokemon-species', monsno)

        for game in game_priority:
            found_entry = next((x for x in poke.flavor_text_entries if x.language.name == languages[language_idx][1] and x.version.name == game), None)
            if found_entry != None:
                return found_entry.flavor_text
            
        return None
    except:
        print("Could not find entry on pokeapi for Pokémon ID {0}".format(str(monsno)))

def get_pokeapi_description_from_file(monsno, language_idx, pokeapi_data):
    # Limited to Gen 8 before PLA
    if monsno > 0 and monsno < 899:
        for game in game_priority:
            found_entry = next((x for x in pokeapi_data["descriptions"][monsno]["list"] if x["lang"] == languages[language_idx][1] and x["game"] == game), None)
            if found_entry != None:
                return found_entry["lines"]
        
    return None

def replace_description(label, new_description, language_idx, monsno):
    label["wordDataArray"] = []

    for line in new_description.split("\n"):
        word = copy.deepcopy(placeholder_word)
        word["patternID"] = 7
        word["eventID"] = 1
        word["tagIndex"] = -1
        word["tagValue"] = 0.0
        word["str"] = line

        if languages[language_idx][0] in ["jpn", "jpn_kanji", "korean", "simp_chinese", "trad_chinese"]:
            word["strWidth"] = 32.0 * len(line)
        else:
            word["strWidth"] = calculate(line)
        label["wordDataArray"].append(word)
    
    label["wordDataArray"][-1]["patternID"] = 0
    label["wordDataArray"][-1]["eventID"] = 7

    #print("Description in language {0} for Pokémon ID {1} replaced!".format(languages[language_idx][0], monsno))

def rewrite_descriptions(language_idx, dia_base_path, prl_base_path):
    dia_path = languages[language_idx][0] + "_" + dia_base_path
    prl_path = languages[language_idx][0] + "_" + prl_base_path
    (inputs, outputs) = load_files([dia_path, prl_path, pokeapi_file], [dia_path, prl_path])

    dia_data = json.load(inputs[0])
    prl_data = json.load(inputs[1])
    pokeapi_data = json.load(inputs[2])

    for (i, dia) in enumerate(dia_data["labelDataArray"]):
        # Ignore vanilla mons
        if i < 494:
            continue
        monsno = int(dia["labelName"].split("_", 4)[3])
        new_description = None
        if from_file:
            new_description = get_pokeapi_description_from_file(monsno, language_idx, pokeapi_data)
        else:
            new_description = get_pokeapi_description(monsno, language_idx)
        if new_description != None: replace_description(dia, new_description, language_idx, monsno)

    for (i, prl) in enumerate(prl_data["labelDataArray"]):
        # Ignore vanilla mons
        if i < 494:
            continue
        monsno = int(prl["labelName"].split("_", 4)[3])
        new_description = None
        if from_file:
            new_description = get_pokeapi_description_from_file(monsno, language_idx, pokeapi_data)
        else:
            new_description = get_pokeapi_description(monsno, language_idx)
        if new_description != None: replace_description(prl, new_description, language_idx, monsno)
                
    json.dump(dia_data, outputs[0], ensure_ascii=False, indent=4)
    json.dump(prl_data, outputs[1], ensure_ascii=False, indent=4)
    close_files(inputs + outputs)

def get_all_pokeapi_descriptions(monsno):
    obj = {"list": []}

    try:
        poke = pb.APIResource('pokemon-species', monsno)
        obj["list"] = [{"lines": x.flavor_text, "lang": x.language.name, "game": x.version.name} for x in poke.flavor_text_entries]
    except:
        print("Could not find entry on pokeapi for Pokémon ID {0}".format(str(monsno)))

    return obj

def steal_from_pokeapi(pokeapi_output_path):
    (inputs, outputs) = load_files([], [pokeapi_output_path])

    descriptions = []

    for i in range(899):
        descriptions.append(get_all_pokeapi_descriptions(i))
    
    json.dump({"descriptions": descriptions}, outputs[0], ensure_ascii=False, indent=4)
    close_files(inputs + outputs)

loadKey()
#steal_from_pokeapi(pokeapi_output_file)
rewrite_descriptions(lang_index, dia_file, prl_file)