# THIS SCRIPT PREPARES THE ASSETRIPPER RIPPED RESOURCES FOLDER FOR USE IN THE BDSP DECOMP
# USE THIS TO BE ABLE TO RUN THE DECOMP

import os
import shutil

replace_table = [
    ('fileID: 1453722849, guid: 67dfb1fdfb2b407222eda8e23ac8b724',  'fileID: 11500000, guid: f4688fdb7df04437aeb418b961361dc5'),
    ('fileID: -667331979, guid: 67dfb1fdfb2b407222eda8e23ac8b724',  'fileID: 11500000, guid: 71c1514a6bd24e1e882cebbe1904ce04'),
    ('fileID: 2019389346, guid: 67dfb1fdfb2b407222eda8e23ac8b724',  'fileID: 11500000, guid: 84a92b25f83d49b9bc132d206b370281'),
    ('fileID: -1936749209, guid: 67dfb1fdfb2b407222eda8e23ac8b724', 'fileID: 11500000, guid: ab2114bdc8544297b417dfefe9f1e410'),
    ('fileID: -395462249, guid: 67dfb1fdfb2b407222eda8e23ac8b724',  'fileID: 11500000, guid: 2705215ac5b84b70bacc50632be6e391'),
    ('fileID: -886440066, guid: fe3602909296aa87b21c8e0e37462a6d',  'fileID: 11500000, guid: f89d3ab10c45d3149973aa264649d53e'),
    ('fileID: 320526709, guid: fe3602909296aa87b21c8e0e37462a6d',   'fileID: 11500000, guid: ee105370dda19044ba6cd8e8089d15ba')
]

ignore_folders = [
     os.path.join('input', 'Scripts'),
     os.path.join('input', 'Plugins'),
]

def is_ignored_folder(path):
    for ignore_folder in ignore_folders:
        if path.startswith(ignore_folder):
            print('Ignoring ' + path)
            return True

def is_valid_extension(file):
    ext = file.split('.')[1]
    return ext == 'asset' or ext == 'prefab'

def replace_guids(src_file, dest_file):
    src_txt = open(src_file, "r", encoding='utf-8').read()
    for (old, new) in replace_table:
        src_txt = src_txt.replace(old, new)
    open(dest_file, "w", encoding='utf-8', newline='').write(src_txt)

def walk_through_input():
    for dirpath, dirnames, filenames in os.walk('input'):
       
        if is_ignored_folder(dirpath):
            continue
        
        for file in filenames:
            src_file = os.path.join(dirpath, file)
            dest_file = os.path.join(dirpath.replace('input', 'output'), file)

            os.makedirs(os.path.dirname(dest_file), exist_ok=True)

            if is_valid_extension(file):
                replace_guids(src_file, dest_file)
            else:
                shutil.copy(src_file, dest_file)

walk_through_input()