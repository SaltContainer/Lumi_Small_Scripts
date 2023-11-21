# THIS SCRIPT CONVERTS TO AND FROM BDSP'S LABEL FILE FORMAT AND CSV FOR EASIER EDITING.
# USE THIS TO REWORK LABEL FILES.

import json
import csv
import copy
import re

from utils.str_calc import calculate, loadKey

id_column = 0
name_column = 1
text_column = 2
style_style_index_column = 3
style_color_index_column = 4
style_font_size_column = 5
style_max_width_column = 6
style_control_id_column = 7

general_columns_count = 8
tag_columns_start = 8
tag_columns_count = 7

tag_tag_index_column = 0
tag_group_id_column = 1
tag_tag_id_column = 2
tag_pattern_id_column = 3
tag_force_article_column = 4
tag_tag_param_column = 5
tag_force_grammar_id_column = 6

label_file = "english_ss_btl_set.json"
csv_file = "output_set.csv"

text_regex = re.compile("([^\{\}]+|{tag:\d+}|{(?:wait|callback):\d+(?:\.\d+)?:(?:[^\{\}]+|{tag:\d+})?}|{pageend:(?:[^\{\}]+)?}\n)")

placeholder_label_file = {
    "m_GameObject": {
        "m_FileID": 0,
        "m_PathID": 0
    },
    "m_Enabled": 1,
    "m_Script": {
        "m_FileID": 0,
        "m_PathID": 3652094840918934080
    },
    "m_Name": "english_ss_btl_std",
    "hash": -1604862815,
    "langID": 2,
    "isResident": 0,
    "isKanji": 0,
    "labelDataArray": []
}

placeholder_item = {
    "labelIndex": 0,
    "arrayIndex": 0,
    "labelName": "ITEMNAME_0000",
    "styleInfo": {
        "styleIndex": 121,
        "colorIndex": -1,
        "fontSize": 42,
        "maxWidth": 420,
        "controlID": 0
    },
    "attributeValueArray": [
        -1,
        0,
        0,
        -1,
        0
    ],
    "tagDataArray": [],
    "wordDataArray": []
}

placeholder_item_tag = {
    "tagIndex": 0,
    "groupID": 0,
    "tagID": 0,
    "tagPatternID": 0,
    "forceArticle": 0,
    "tagParameter": 0,
    "tagWordArray": [],
    "forceGrmID": 0
}

placeholder_item_word = {
    "patternID": 0,
    "eventID": 0,
    "tagIndex": -1,
    "tagValue": 0.0,
    "str": "",
    "strWidth": 0.0
}

def load_files_json_to_csv(inputs, outputs):
    input_files = []
    for input in inputs:
        input_files.append(open('input/' + input, encoding='utf-8'))

    output_files = []
    for output in outputs:
        output_files.append(open('output/' + output, "w", encoding='utf-8', newline=''))
    
    return (input_files, output_files)

def load_files_csv_to_json(inputs, outputs):
    input_files = []
    for input in inputs:
        input_files.append(open('input/' + input, encoding='utf-8'))

    output_files = []
    for output in outputs:
        output_files.append(open('output/' + output, "w", encoding='utf-8'))
    
    return (input_files, output_files)

def close_files(files):
    for file in files:
        file.close()

def convert_item_to_csv(item):
    new_row = [0] * general_columns_count

    new_row[id_column] = item["labelIndex"]
    new_row[name_column] = item["labelName"]
    new_row[style_style_index_column] = item["styleInfo"]["styleIndex"]
    new_row[style_color_index_column] = item["styleInfo"]["colorIndex"]
    new_row[style_font_size_column] = item["styleInfo"]["fontSize"]
    new_row[style_max_width_column] = item["styleInfo"]["maxWidth"]
    new_row[style_control_id_column] = item["styleInfo"]["controlID"]

    words = []
    for word in item["wordDataArray"]:
        word_to_add = ""
        if word["str"] != "": # Non-empty string
            word_to_add += word["str"]
        elif word["tagIndex"] != -1:
            word_to_add += "{tag:" + str(word["tagIndex"]) + "}"

        if word["eventID"] == 2:
            word_to_add = "{wait:" + str(word["tagValue"]) + ":" + word_to_add + "}"
        
        if word["eventID"] == 5:
            word_to_add = "{callback:" + str(word["tagValue"]) + ":" + word_to_add + "}"

        if word["eventID"] == 1 or word["eventID"] == 4:
            word_to_add += "\n"
        
        if word["eventID"] == 3:
            word_to_add = "{pageend:" + word_to_add + "}\n"
        
        words.append(word_to_add)

    new_row[text_column] = "".join(words)

    for i, tag in enumerate(item["tagDataArray"]):
        new_row += [0] * tag_columns_count
        
        tag_start = tag_columns_start + tag_columns_count*i

        new_row[tag_start + tag_tag_index_column] = tag["tagIndex"]
        new_row[tag_start + tag_group_id_column] = tag["groupID"]
        new_row[tag_start + tag_tag_id_column] = tag["tagID"]
        new_row[tag_start + tag_pattern_id_column] = tag["tagPatternID"]
        new_row[tag_start + tag_force_article_column] = tag["forceArticle"]
        new_row[tag_start + tag_tag_param_column] = tag["tagParameter"]
        new_row[tag_start + tag_force_grammar_id_column] = tag["forceGrmID"]
    
    return new_row

def convert_item_to_json(row):
    new_item = copy.deepcopy(placeholder_item)

    new_item["labelIndex"] = int(row[id_column])
    new_item["arrayIndex"] = int(row[id_column])
    new_item["labelName"] = row[name_column]
    
    i = 0
    while i*tag_columns_count + tag_columns_start < len(row) and row[i*tag_columns_count + tag_columns_start] != "":
        index = i*tag_columns_count + tag_columns_start
        new_tag = copy.deepcopy(placeholder_item_tag)

        new_tag["tagIndex"] = int(row[index + tag_tag_index_column])
        new_tag["groupID"] = int(row[index + tag_group_id_column])
        new_tag["tagID"] = int(row[index + tag_tag_id_column])
        new_tag["tagPatternID"] = int(row[index + tag_pattern_id_column])
        new_tag["forceArticle"] = int(row[index + tag_force_article_column])
        new_tag["tagParameter"] = int(row[index + tag_tag_param_column])
        new_tag["forceGrmID"] = int(row[index + tag_force_grammar_id_column])

        new_item["tagDataArray"].append(new_tag)
        i += 1

    matches = text_regex.findall(row[text_column])
    adjusted_matches = []

    if matches == []:
        adjusted_matches = [""]
    for match in matches:
        if not (match.startswith("{")):
            if match.count("\n") > 0:
                submatches = match.split("\n")
                for j, submatch in enumerate(submatches):
                    if j < len(submatches) - 1:
                        adjusted_matches.append(submatch + "\n")
                    elif submatch != "":
                        adjusted_matches.append(submatch)
            else:
                adjusted_matches.append(match)
        else:
            adjusted_matches.append(match)

    first_line = True
    for match in adjusted_matches:
        new_line = copy.deepcopy(placeholder_item_word)

        if match.startswith("{") and match.endswith("}"):
            trimmed = match[1:-1]
            args = trimmed.split(":")
            if args[0] == "tag":
                new_line["patternID"] = 5
                new_line["tagIndex"] = int(args[1])
                new_line["strWidth"] = -1.0
            elif args[0] == "wait":
                new_line["patternID"] = 7
                new_line["eventID"] = 2
                new_line["tagValue"] = float(args[1])
                new_line["str"] = args[2]
                new_line["strWidth"] = calculate(args[2])
            elif args[0] == "callback":
                new_line["patternID"] = 7
                new_line["eventID"] = 5
                new_line["tagValue"] = float(args[1])
                new_line["str"] = args[2]
                new_line["strWidth"] = calculate(args[2])
        elif match.startswith("{") and match.endswith("}\n"):
            trimmed = match[1:-2]
            args = trimmed.split(":")
            if args[0] == "pageend":
                new_line["patternID"] = 7
                new_line["eventID"] = 3
                new_line["str"] = args[1]
                new_line["strWidth"] = calculate(args[1])
        else:
            if match.endswith("\n"):
                new_line["patternID"] = 7
                new_line["eventID"] = 1
                new_line["str"] = match[:-1]
                new_line["strWidth"] = calculate(match[:-1])
                if not first_line:
                    new_line["eventID"] = 4
                first_line = False
            else:
                new_line["patternID"] = 0
                new_line["eventID"] = 0
                new_line["str"] = match
                new_line["strWidth"] = calculate(match)

        new_item["wordDataArray"].append(new_line)
    
    new_item["wordDataArray"][-1]["eventID"] = 7

    new_item["styleInfo"]["styleIndex"] = int(row[style_style_index_column])
    new_item["styleInfo"]["colorIndex"] = int(row[style_color_index_column])
    new_item["styleInfo"]["fontSize"] = int(row[style_font_size_column])
    new_item["styleInfo"]["maxWidth"] = int(row[style_max_width_column])
    new_item["styleInfo"]["controlID"] = int(row[style_control_id_column])

    return new_item

def convert_to_csv(json_input_path, csv_output_path):
    (inputs, outputs) = load_files_json_to_csv([json_input_path], [csv_output_path])

    json_data = json.load(inputs[0])
    csv_writer = csv.writer(outputs[0], delimiter=',')

    for item in json_data['labelDataArray']:
        new_row = convert_item_to_csv(item)
        csv_writer.writerow(new_row)
    
    close_files([inputs[0], outputs[0]])

def convert_to_json(csv_input_path, json_output_path):
    (inputs, outputs) = load_files_csv_to_json([csv_input_path], [json_output_path])

    csv_reader = csv.reader(inputs[0], delimiter=',')
    json_data = copy.deepcopy(placeholder_label_file)
    
    for row in csv_reader:
        new_item = convert_item_to_json(row)
        json_data['labelDataArray'].append(new_item)
                
    json.dump(json_data, outputs[0], ensure_ascii=False, indent=4)
    close_files([inputs[0], outputs[0]])


loadKey()
convert_to_csv(label_file, csv_file)
#convert_to_json(csv_file, label_file)