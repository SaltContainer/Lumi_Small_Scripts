# THIS SCRIPT PREPARES THE ASSETRIPPER RIPPED RESOURCES FOLDER FOR USE IN THE BDSP DECOMP
# USE THIS TO BE ABLE TO RUN THE DECOMP

import os
import shutil

replace_table = [
    ('fileID: 1453722849, guid: 67dfb1fdfb2b407222eda8e23ac8b724',  'fileID: 11500000, guid: f4688fdb7df04437aeb418b961361dc5'), # TextMeshProUGUI
    ('fileID: -667331979, guid: 67dfb1fdfb2b407222eda8e23ac8b724',  'fileID: 11500000, guid: 71c1514a6bd24e1e882cebbe1904ce04'), # TMP_FontAsset
    ('fileID: 2019389346, guid: 67dfb1fdfb2b407222eda8e23ac8b724',  'fileID: 11500000, guid: 84a92b25f83d49b9bc132d206b370281'), # TMP_SpriteAsset
    ('fileID: -1936749209, guid: 67dfb1fdfb2b407222eda8e23ac8b724', 'fileID: 11500000, guid: ab2114bdc8544297b417dfefe9f1e410'), # TMP_StyleSheet
    ('fileID: -395462249, guid: 67dfb1fdfb2b407222eda8e23ac8b724',  'fileID: 11500000, guid: 2705215ac5b84b70bacc50632be6e391'), # TMP_Settings
    ('fileID: -886440066, guid: fe3602909296aa87b21c8e0e37462a6d',  'fileID: 11500000, guid: f89d3ab10c45d3149973aa264649d53e'), # SceneDatabase
    ('fileID: 320526709, guid: fe3602909296aa87b21c8e0e37462a6d',   'fileID: 11500000, guid: ee105370dda19044ba6cd8e8089d15ba'), # StartupSettings
    ('fileID: 16995157, guid: 9684ab7ac98f2cc8be57bb5146ddf8ea',    'fileID: 16995157, guid: 8b3f2f2bec6da5b4ebb51b260aab248b'), # DOTweenSettings
    
    ('fileID: 11500000, guid: af26a3094453c76e175f10cd07916725',    'fileID: 11500000, guid: f65ac5130cd73454198620d792d1b1b5'), # AudioManager
    ('fileID: 11500000, guid: 265df9f353450a19ef76f2e3d15b7baa',    'fileID: 11500000, guid: 4d6de2d8a24b6804c9ec41fdc5105aa4'), # AkInitializer
    ('fileID: 11500000, guid: aa2b8aed30a335a610a8cb7de2e6fc59',    'fileID: 11500000, guid: 81fc8a5d169fd8b40ba7a9e9ac1bbf45'), # AkGameObj
    ('fileID: 11500000, guid: 129b0eb9d315b2c154388d10621f18f5',    'fileID: 11500000, guid: d2c5a0a1b1437b045b2005ef7787cd85'), # AkAudioListener
    ('fileID: 11500000, guid: 3f096face3942b8b76f27adb02069efe',    'fileID: 11500000, guid: 435b238fdaa544b429f817b009a9ba96'), # Bloom
    ('fileID: 11500000, guid: 151ae2ca31de4cbb8d9fe3b7c23e2d8b',    'fileID: 11500000, guid: a6aeed9f1a877d2419c1ac40e58076dc'), # EffectManager
    ('fileID: 11500000, guid: 93583f25def0f6ca86cce2c3649e681c',    'fileID: 11500000, guid: 12b471aac34ea4a47ac22e579486ccad'), # Fader
    ('fileID: 11500000, guid: be9398d8e20ff4756943b9ee20892f26',    'fileID: 11500000, guid: 855888f17e06c2149afda4fe82b29028'), # FontManager
    ('fileID: 11500000, guid: d6a10a9c2a849ba4165ffb4d78ecf408',    'fileID: 11500000, guid: b020ff6ca6f6c2048a24bb7eb6f3cd54'), # FontMaterialData
    ('fileID: 11500000, guid: 5cc4e04fbf8c234954bcfbe063173710',    'fileID: 11500000, guid: 435b238fdaa544b429f817b009a9ba96'), # FXAA
    ('fileID: 11500000, guid: fa3f1a2d47bf9479853f992a9cd99dc9',    'fileID: 11500000, guid: 58f48747922227449bf85f0468298be1'), # GameManager
    ('fileID: 11500000, guid: 8566a150099689db717b1d575ebd117d',    'fileID: 11500000, guid: 89a36fa8cb67b054aa49b8c4f2ab6d63'), # MessageManager
    ('fileID: 11500000, guid: 4149db6cfc4376374957a6ef8a1086b2',    'fileID: 11500000, guid: 18b3b35e780deb6449264bb70b100f48'), # MsgWindowConfig
    ('fileID: 11500000, guid: 9d4e4b7cf44c2711657ccf1f6357f33c',    'fileID: 11500000, guid: 8175e9e7e6e6dea428aeb4ff32036261'), # MsgWindowManager
    ('fileID: 11500000, guid: e3bbf39e44ea87ce707f0d235ae690f4',    'fileID: 11500000, guid: f9f5538193f659845821f5fa9b54fdd9'), # MsgWindow
    ('fileID: 11500000, guid: 2a4f7888223e2e16ec26981e9e04f24d',    'fileID: 11500000, guid: 8590a4b10b3220649a9da015a94ecd35'), # WindowUIContents
    ('fileID: 11500000, guid: d8042ec113a2f751a8738cc4fee57d8b',    'fileID: 11500000, guid: dff014ff5c344194183e335338f85f1a'), # DOTweenAnimation
    ('fileID: 11500000, guid: 549088c9749fad39011ff971d5909cde',    'fileID: 11500000, guid: eb7251d3eafcb7d4585da0100df5df7c'), # WindowMessage
    ('fileID: 11500000, guid: 679222118d29066139668df3744c36c2',    'fileID: 11500000, guid: edae71040e4308a4f9bf9750c989fd23'), # MsgTextContainer
    ('fileID: 11500000, guid: e9979134a95d48a4be8f59ad9b0047f4',    'fileID: 11500000, guid: 271a7c27038e8ca4fa64a55ef60c0b72'), # WindowMsgText
    ('fileID: 11500000, guid: 229b64c070b65cc6aa1cbac68e50c648',    'fileID: 11500000, guid: 11abd00e6f234634caf92c142d760c45'), # IlcaNetComponent
    ('fileID: 11500000, guid: c0c558ec73e36a5cd8073d11280c4f0a',    'fileID: 11500000, guid: de42fc04137f9e14dbf9ce03357663a2'), # NetworkManager
    ('fileID: 11500000, guid: cb5ce94a80c66dce7b97eabe4ca71708',    'fileID: 11500000, guid: 522e3c54cce6825458aa39563e83d77e'), # NexInitializer
    ('fileID: 11500000, guid: 5c375ff265ce7124fc0f9d93c49f0bba',    'fileID: 11500000, guid: 43a2d212b348cbd4db3f2c7384a51d32'), # NowloadingController
    ('fileID: 11500000, guid: 761f81b00a6cc927eccd1a8456ae875c',    'fileID: 11500000, guid: f3c6a020f46c28b4a9a7799d20ec3cba'), # PokemonWalkingDatas
    ('fileID: 11500000, guid: c4f3f8a8e71740e986d36b5c309acab0',    'fileID: 11500000, guid: 0ced4888a89b3f04183517e5b9a3af07'), # PokemonData
    ('fileID: 11500000, guid: 43d3c42574634ba58f588e5eb44bb67e',    'fileID: 11500000, guid: 1f95b48be822d4744bffd180bdfa222f'), # Ranking2Board
    ('fileID: 11500000, guid: bc4b439570afd72e87d9b0db7d85ec1a',    'fileID: 11500000, guid: 06468eeefe4c36e41b0a3da4703272b6'), # RankingBoard
    ('fileID: 11500000, guid: 3c1340a7c8b78585b2f50d6249260568',    'fileID: 11500000, guid: c08c7f9e639e01e4c9b4f46737ed0185'), # TextFontData
    ('fileID: 11500000, guid: a2a9e0be1b586c7c69ee14a762f631fe',    'fileID: 11500000, guid: 72290dd61900725409c8577adbdfac01'), # UIManager
    ('fileID: 11500000, guid: c261b62f982afa632afe06048aa03363',    'fileID: 11500000, guid: e1a0638d784d6e848b01493c769dbbe1'), # UIModelViewController
    ('fileID: 11500000, guid: c03d05417659e87e2725ea67510a9b6a',    'fileID: 11500000, guid: af47fac975ff46841a3c6b07e3e9f4d8'), # EnvironmentController
    ('fileID: 11500000, guid: e83ee09714f92946151e18b798f64e89',    'fileID: 11500000, guid: d61a893039256b34e812cff78ec37da8'), # ModelViewBgCamera
    ('fileID: 11500000, guid: 78307eae56dcddce1eb9760de1964e0d',    'fileID: 11500000, guid: b5d83df269de3c14e96bcd504cb4ef48'), # RenderPriorityController
    ('fileID: 11500000, guid: c1cb69dd146a60706c29ad961420ebf6',    'fileID: 11500000, guid: e0ea7264f404fb140b5098fc304ef193'), # ModelViewReflectionCamera
    ('fileID: 11500000, guid: 6f1e2027157c2c864a03835c34be7c48',    'fileID: 11500000, guid: d2b29de3b4b85be4ab2fa2d5524f89d3'), # PostProcessFilter
    ('fileID: 11500000, guid: 3ef5d7767f7f48b4c2b87a6875268fb5',    'fileID: 11500000, guid: 1235fb9ba276440439e8c667130529a6')  # EnvironmentSettings
]

ignore_folders = [
     os.path.join('input', 'Scripts'),
     os.path.join('input', 'Plugins'),
     os.path.join('input', 'Shaders'),
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