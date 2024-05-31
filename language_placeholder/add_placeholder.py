# THIS SCRIPT ADDS PLACEHOLDER LABELS BY COMPARING A BDSP LABEL FILE TO ANOTHER.
# USE THIS TO PREPARE LANGUAGE BUNDLES FOR LATER TRANSLATING.
# IMPORTANT NOTE: THE INDICES ON x_ss_btl_attack HAVE TO BE FIXED AFTER.

import json
import copy

from os import listdir
from os.path import isfile, join

src_lang = "english"
dest_lang = "trad_chinese"

changed_list_file = "changed.json"
renamed_list_file = "renamed.json"

def load_files_json(inputs, outputs):
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

def copy_header(input, output):
    output["m_GameObject"]["m_FileID"] = input["m_GameObject"]["m_FileID"]
    output["m_GameObject"]["m_PathID"] = input["m_GameObject"]["m_PathID"]
    output["m_Enabled"] = input["m_Enabled"]
    output["m_Script"]["m_FileID"] = input["m_Script"]["m_FileID"]
    output["m_Script"]["m_PathID"] = input["m_Script"]["m_PathID"]
    output["m_Name"] = input["m_Name"]
    output["hash"] = input["hash"]
    output["langID"] = input["langID"]
    output["isResident"] = input["isResident"]
    output["isKanji"] = input["isKanji"]

def copy_label(input, output):
    output["labelIndex"] = input["labelIndex"]
    output["arrayIndex"] = input["arrayIndex"]
    output["styleInfo"] = input["styleInfo"]
    output["attributeValueArray"] = input["attributeValueArray"]
    output["tagDataArray"] = input["tagDataArray"]
    output["wordDataArray"] = input["wordDataArray"]

def loop_through_data(src_data, dest_data, renamed_list, changed_list, filename):
    output_data = copy.deepcopy(src_data)

    copy_header(dest_data, output_data)

    src_idx = 0
    dest_idx = 0
    for _ in output_data["labelDataArray"]:
        # Reached the end of either list
        if src_idx >= len(output_data["labelDataArray"]) or dest_idx >= len(dest_data["labelDataArray"]):
            break
        # Same label name
        elif output_data["labelDataArray"][src_idx]["labelName"] == dest_data["labelDataArray"][dest_idx]["labelName"]:
            # If this is not marked as changed, revert to destination language
            if output_data["labelDataArray"][src_idx]["labelName"] not in changed_list:
                copy_label(dest_data["labelDataArray"][dest_idx], output_data["labelDataArray"][src_idx])
            src_idx += 1
            dest_idx += 1
        # Different label name, but was marked as renamed
        elif output_data["labelDataArray"][src_idx]["labelName"] in renamed_list:
            # Don't copy and just skip entry, we keep this changed English label as placeholder
            src_idx += 1
            dest_idx += 1
        # Random empty entry in the middle (for ss_btl_attack)
        elif dest_data["labelDataArray"][dest_idx]["labelName"] == "" and filename == "ss_btl_attack":
            # Don't copy and just skip entry, we keep this changed English label as placeholder it's fine
            src_idx += 1
            dest_idx += 1
        else:
            # Don't copy and just increment src, we keep this new English entry as placeholder
            src_idx += 1
    
    return output_data


def add_placeholder(src_path, dest_path, output_path, renamed_path, changed_path):
    (inputs, outputs) = load_files_json([src_path, dest_path, renamed_path, changed_path], [output_path])

    src_data = json.load(inputs[0])
    dest_data = json.load(inputs[1])
    renamed_data = json.load(inputs[2])
    changed_data = json.load(inputs[3])

    filename = src_data["m_Name"].split('_', 1)[1]

    renamed_list = []
    if filename in renamed_data:
        renamed_list = renamed_data[filename]

    changed_list = []
    if filename in changed_data:
        changed_list = changed_data[filename]

    output_data = loop_through_data(src_data, dest_data, renamed_list, changed_list, filename)

    json.dump(output_data, outputs[0], ensure_ascii=False, indent=4)
    close_files([inputs[0], inputs[1], outputs[0]])

def add_placeholders_of_all_files(src_language, dest_language):
    files = [f for f in listdir("input") if isfile(join("input", f))]
    for file in files:
        if file.startswith(src_language):
            filename = file.split('_', 1)[1]
            add_placeholder(src_language + "_" + filename, dest_language + "_" + filename, dest_language + "_" + filename, renamed_list_file, changed_list_file)

add_placeholders_of_all_files(src_lang, dest_lang)