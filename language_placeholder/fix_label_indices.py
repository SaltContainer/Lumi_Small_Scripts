# THIS SCRIPT CHANGES BOTH LABELINDEX AND ARRAYINDEX TO MATCH THE PROPER INDEX IN THE ARRAY OF THE LABEL.
# USE THIS TO HAVE A NICE ORDERED BDSP LABEL FILE
# IMPORTANT NOTE: x_ss_btl_attack HAS TO BE RAN THROUGH THIS SCRIPT IF YOU GENERATED PLACEHOLDERS FOR IT.

import json

input_file = "spanish_ss_btl_attack.json"
output_file = "spanish_ss_btl_attack.json"

fix_label_index = True
fix_array_index = True

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

def fix_label_indices(input_path, output_path):
    (inputs, outputs) = load_files_json([input_path], [output_path])

    label_data = json.load(inputs[0])

    for (i, label) in enumerate(label_data["labelDataArray"]):
        if fix_label_index: label["labelIndex"] = i
        if fix_array_index: label["arrayIndex"] = i

    json.dump(label_data, outputs[0], ensure_ascii=False, indent=4)
    close_files([inputs[0], outputs[0]])


fix_label_indices(input_file, output_file)