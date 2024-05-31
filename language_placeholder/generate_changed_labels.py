# THIS SCRIPT GENERATES A FILE THAT DESCRIBES ALL THE CHANGED LABELS IN A BDSP LABEL FILE.
# USE THIS TO PREPARE FOR ADDING PLACEHOLDER LABELS.

import json
import copy

from os import listdir
from os.path import isfile, join
from utils.str_calc import calculate, loadKey

vanilla_folder = "vanilla"
edited_folder = "lumi"

output_file = "changed.json"

output_data = {}

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

def find_label_with_label_name(labels, label_name):
    for label in labels:
        if label["labelName"] == label_name:
            return label
    
    return None

def is_label_changed(vanilla_label, edited_label):
    if vanilla_label["styleInfo"]["styleIndex"] != edited_label["styleInfo"]["styleIndex"]: return True
    if vanilla_label["styleInfo"]["colorIndex"] != edited_label["styleInfo"]["colorIndex"]: return True
    if vanilla_label["styleInfo"]["fontSize"] != edited_label["styleInfo"]["fontSize"]: return True
    if vanilla_label["styleInfo"]["maxWidth"] != edited_label["styleInfo"]["maxWidth"]: return True
    if vanilla_label["styleInfo"]["controlID"] != edited_label["styleInfo"]["controlID"]: return True

    if vanilla_label["attributeValueArray"] != edited_label["attributeValueArray"]: return True

    if len(vanilla_label["tagDataArray"]) != len(edited_label["tagDataArray"]): return True
    for (i, vanilla_tag) in enumerate(vanilla_label["tagDataArray"]):
        if vanilla_tag["tagIndex"] != edited_label["tagDataArray"][i]["tagIndex"]: return True
        if vanilla_tag["groupID"] != edited_label["tagDataArray"][i]["groupID"]: return True
        if vanilla_tag["tagID"] != edited_label["tagDataArray"][i]["tagID"]: return True
        if vanilla_tag["tagPatternID"] != edited_label["tagDataArray"][i]["tagPatternID"]: return True
        if vanilla_tag["forceArticle"] != edited_label["tagDataArray"][i]["forceArticle"]: return True
        if vanilla_tag["tagParameter"] != edited_label["tagDataArray"][i]["tagParameter"]: return True
        if vanilla_tag["tagWordArray"] != edited_label["tagDataArray"][i]["tagWordArray"]: return True
        if vanilla_tag["forceGrmID"] != edited_label["tagDataArray"][i]["forceGrmID"]: return True

    if len(vanilla_label["wordDataArray"]) != len(edited_label["wordDataArray"]): return True
    for (i, vanilla_word) in enumerate(vanilla_label["wordDataArray"]):
        if vanilla_word["patternID"] != edited_label["wordDataArray"][i]["patternID"]: return True
        if vanilla_word["eventID"] != edited_label["wordDataArray"][i]["eventID"]: return True
        if vanilla_word["tagIndex"] != edited_label["wordDataArray"][i]["tagIndex"]: return True
        if vanilla_word["tagValue"] != edited_label["wordDataArray"][i]["tagValue"]: return True
        if vanilla_word["str"] != edited_label["wordDataArray"][i]["str"]: return True
        if vanilla_word["strWidth"] != edited_label["wordDataArray"][i]["strWidth"]: return True
    
    return False

def get_root_label_file_name(full_filename):
    return full_filename.split('_', 1)[1].split('.')[0]

def generate_changed_labels_of_file(vanilla_dir, edited_dir, filename):
    (inputs, outputs) = load_files_json([vanilla_dir + "/" + filename, edited_dir + "/" + filename], [])

    vanilla_data = json.load(inputs[0])
    edited_data = json.load(inputs[1])

    output_data[get_root_label_file_name(filename)] = []
    for label in vanilla_data["labelDataArray"]:
        edited_label = find_label_with_label_name(edited_data["labelDataArray"], label["labelName"])
        if edited_label != None and is_label_changed(label, edited_label):
            output_data[get_root_label_file_name(filename)].append(label["labelName"])

    close_files(inputs)

def generate_changed_labels(vanilla_dir, edited_dir, output_path):
    files = [f for f in listdir("input/" + vanilla_dir) if isfile(join("input/" + edited_dir, f))]
    for file in files:
        generate_changed_labels_of_file(vanilla_dir, edited_dir, file)
    
    (inputs, outputs) = load_files_json([], [output_path])
    json.dump(output_data, outputs[0], ensure_ascii=False, indent=4)
    close_files(outputs)

loadKey()
generate_changed_labels(vanilla_folder, edited_folder, output_file)