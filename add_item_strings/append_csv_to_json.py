# THIS SCRIPT APPENDS DATA TO THE GIVEN LANGUAGE LABEL FILES BASED ON A CSV FILE.
# USE THIS TO AUTOMATICALLY ADD NEW LABELS TO LABEL FILES.

import json
import csv
import copy

from utils.str_calc import calculate, loadKey

id_column = 0
name_column = 1
name_classified_column = 2
name_acc_column = 3
name_acc_classified_column = 4
name_plural_column = 5
name_plural_classified_column = 6
description_column = 8

placeholder_name = {
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

placeholder_name_text = {
    "patternID": 0,
    "eventID": 7,
    "tagIndex": -1,
    "tagValue": 0.0,
    "str": "Placeholder Item",
    "strWidth": 0.0
}

placeholder_description = {
    "labelIndex": 0,
    "arrayIndex": 0,
    "labelName": "ITEMINFO_0000",
    "styleInfo": {
        "styleIndex": 109,
        "colorIndex": -1,
        "fontSize": 32,
        "maxWidth": 736,
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

placeholder_description_text = {
    "patternID": 7,
    "eventID": 1,
    "tagIndex": -1,
    "tagValue": 0.0,
    "str": "A placeholder item.",
    "strWidth": 0.0
}

def load_files(json_input_path, csv_input_path, json_output_path):
    json_input_file = open('input/' + json_input_path, encoding='utf-8')
    csv_input_file = open('input/' + csv_input_path, encoding='utf-8')
    json_output_file = open('output/' + json_output_path, "w", encoding='utf-8')
    return (json_input_file, csv_input_file, json_output_file)


def close_files(json_input_file, csv_input_file, json_output_file):
    json_input_file.close()
    csv_input_file.close()
    json_output_file.close()


def set_base_name_data(csv_row, csv_column):
    new_item = copy.deepcopy(placeholder_name)
    new_item["labelIndex"] = int(csv_row[id_column])
    new_item["arrayIndex"] = int(csv_row[id_column])
    new_item["labelName"] = "ITEMNAME_" + csv_row[id_column]

    new_text = copy.deepcopy(placeholder_name_text)
    new_text["str"] = csv_row[csv_column]
    new_text["strWidth"] = calculate(csv_row[csv_column])
    new_item["wordDataArray"].append(new_text)

    return new_item


def write_names(json_input_path, csv_input_path, json_output_path):
    (json_input_file, csv_input_file, json_output_file) = load_files(json_input_path, csv_input_path, json_output_path)
    
    json_data = json.load(json_input_file)
    csv_reader = csv.reader(csv_input_file, delimiter=',')

    for row in csv_reader:
        new_item = set_base_name_data(row, name_column)
        new_item["styleInfo"]["styleIndex"] = 121
        json_data['labelDataArray'].append(new_item)
                
    json.dump(json_data, json_output_file, ensure_ascii=False, indent=4)
    close_files(json_input_file, csv_input_file, json_output_file)


def write_names_classified(json_input_path, csv_input_path, json_output_path):
    (json_input_file, csv_input_file, json_output_file) = load_files(json_input_path, csv_input_path, json_output_path)
    
    json_data = json.load(json_input_file)
    csv_reader = csv.reader(csv_input_file, delimiter=',')

    for row in csv_reader:
        new_item = set_base_name_data(row, name_classified_column)
        new_item["styleInfo"]["styleIndex"] = 123
        json_data['labelDataArray'].append(new_item)
                
    json.dump(json_data, json_output_file, ensure_ascii=False, indent=4)
    close_files(json_input_file, csv_input_file, json_output_file)


def write_names_acc(json_input_path, csv_input_path, json_output_path):
    (json_input_file, csv_input_file, json_output_file) = load_files(json_input_path, csv_input_path, json_output_path)
    
    json_data = json.load(json_input_file)
    csv_reader = csv.reader(csv_input_file, delimiter=',')

    for row in csv_reader:
        new_item = set_base_name_data(row, name_acc_column)
        new_item["styleInfo"]["styleIndex"] = 121
        json_data['labelDataArray'].append(new_item)
                
    json.dump(json_data, json_output_file, ensure_ascii=False, indent=4)
    close_files(json_input_file, csv_input_file, json_output_file)


def write_names_acc_classified(json_input_path, csv_input_path, json_output_path):
    (json_input_file, csv_input_file, json_output_file) = load_files(json_input_path, csv_input_path, json_output_path)
    
    json_data = json.load(json_input_file)
    csv_reader = csv.reader(csv_input_file, delimiter=',')

    for row in csv_reader:
        new_item = set_base_name_data(row, name_acc_classified_column)
        new_item["styleInfo"]["styleIndex"] = 123
        json_data['labelDataArray'].append(new_item)
                
    json.dump(json_data, json_output_file, ensure_ascii=False, indent=4)
    close_files(json_input_file, csv_input_file, json_output_file)


def write_names_plural(json_input_path, csv_input_path, json_output_path):
    (json_input_file, csv_input_file, json_output_file) = load_files(json_input_path, csv_input_path, json_output_path)
    
    json_data = json.load(json_input_file)
    csv_reader = csv.reader(csv_input_file, delimiter=',')

    for row in csv_reader:
        new_item = set_base_name_data(row, name_plural_column)
        new_item["styleInfo"]["styleIndex"] = 122
        json_data['labelDataArray'].append(new_item)
                
    json.dump(json_data, json_output_file, ensure_ascii=False, indent=4)
    close_files(json_input_file, csv_input_file, json_output_file)


def write_names_plural_classified(json_input_path, csv_input_path, json_output_path):
    (json_input_file, csv_input_file, json_output_file) = load_files(json_input_path, csv_input_path, json_output_path)
    
    json_data = json.load(json_input_file)
    csv_reader = csv.reader(csv_input_file, delimiter=',')

    for row in csv_reader:
        new_item = set_base_name_data(row, name_plural_classified_column)
        new_item["styleInfo"]["styleIndex"] = 123
        json_data['labelDataArray'].append(new_item)
                
    json.dump(json_data, json_output_file, ensure_ascii=False, indent=4)
    close_files(json_input_file, csv_input_file, json_output_file)


def write_descriptions(json_input_path, csv_input_path, json_output_path):
    (json_input_file, csv_input_file, json_output_file) = load_files(json_input_path, csv_input_path, json_output_path)
    
    json_data = json.load(json_input_file)
    csv_reader = csv.reader(csv_input_file, delimiter=',')

    for row in csv_reader:
        new_item = copy.deepcopy(placeholder_description)
        new_item["labelIndex"] = int(row[id_column])
        new_item["arrayIndex"] = int(row[id_column])
        new_item["labelName"] = "ITEMINFO_" + row[id_column]
        lines = row[description_column].split("\n")
        for line in lines:
            new_line = copy.deepcopy(placeholder_description_text)
            new_line["str"] = line
            new_line["strWidth"] = calculate(line)
            new_item["wordDataArray"].append(new_line)
        new_item["wordDataArray"][-1]["patternID"] = 0
        new_item["wordDataArray"][-1]["eventID"] = 7
        json_data['labelDataArray'].append(new_item)
                
    json.dump(json_data, json_output_file, ensure_ascii=False, indent=4)
    close_files(json_input_file, csv_input_file, json_output_file)


loadKey()
write_names('english_ss_itemname.json', 'new_data.csv', 'english_ss_itemname.json')
write_names_classified('english_ss_itemname_classified.json', 'new_data.csv', 'english_ss_itemname_classified.json')
write_names_acc('english_ss_itemname_acc.json', 'new_data.csv', 'english_ss_itemname_acc.json')
write_names_acc_classified('english_ss_itemname_acc_classified.json', 'new_data.csv', 'english_ss_itemname_acc_classified.json')
write_names_plural('english_ss_itemname_plural.json', 'new_data.csv', 'english_ss_itemname_plural.json')
write_names_plural_classified('english_ss_itemname_plural_classified.json', 'new_data.csv', 'english_ss_itemname_plural_classified.json')
write_descriptions('english_ss_iteminfo.json', 'new_data.csv', 'english_ss_iteminfo.json')