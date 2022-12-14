# -*- coding: utf-8 -*-
r"""
.-----------------------------------------------------.

______                           _           _
| ___ \                         | |         (_)
| |_/ / __ ___  _ __   ___   ___| |__   __ _ _ _ __
|  __/ '__/ _ \| '_ \ / _ \ / __| '_ \ / _` | | '_ \
| |  | | | (_) | | | | (_) | (__| | | | (_| | | | | |
\_|  |_|  \___/|_| |_|\___/ \___|_| |_|\__,_|_|_| |_|


.-----------------------------------------------------.

 _____                           _   _               _   _ ______ _____
|  __ \                         | | (_)             | \ | ||  ___|_   _|
| |  \/ ___ _ __   ___ _ __ __ _| |_ _  ___  _ __   |  \| || |_    | |
| | __ / _ \ '_ \ / _ \ '__/ _` | __| |/ _ \| '_ \  | . ` ||  _|   | |
| |_\ \  __/ | | |  __/ | | (_| | |_| | (_) | | | | | |\  || |     | |
 \____/\___|_| |_|\___|_|  \__,_|\__|_|\___/|_| |_| \_| \_/\_|     \_/


.------------------------------------------------------------------------.

File: app/generation_nft/libraries/face/face_styling/constants.py
"""
from app.settings import settings

IRIS_CENTER_POINT = (151, 151)
IRIS_RADIAL = 39

TEMP_PATH = f"{settings.GENERATION_NFT_PATH}/libraries/face/face_styling/temp"  # chemin des svg temporaires

NOSE_POINT = [
    [189, 193, 245],
    [245, 193, 687],
    [245, 687, 122],
    [245, 122, 188],
    [188, 122, 694],
    [188, 694, 196],
    [188, 196, 655],
    [188, 655, 174],
    [174, 655, 656],
    [174, 640, 236],
    [236, 640, 134],
    [134, 220, 723],
    [723, 220, 725],
    [725, 727, 45],
    [725, 220, 727],
    [45, 727, 646],
    [237, 727, 646],
    [413, 417, 465],
    [465, 417, 689],
    [465, 689, 351],
    [465, 351, 412],
    [412, 351, 696],
    [412, 696, 419],
    [412, 419, 670],
    [412, 670, 399],
    [399, 669, 670],
    [399, 641, 456],
    [456, 641, 363],
    [363, 641, 724],
    [641, 724, 726],
    [281, 641, 726],
    [363, 440, 724],
    [724, 726, 440],
    [275, 726, 728],
    [726, 440, 728],
    [174, 198, 236],
    [236, 198, 134],
    [134, 198, 131],
    [134, 131, 220],
    [134, 640, 723],
    [51, 640, 725],
    [640, 723, 725],
    [725, 45, 51],
    [220, 131, 115],
    [399, 456, 420],
    [456, 420, 363],
    [363, 420, 360],
    [363, 360, 440],
    [440, 360, 344],
    [655, 196, 656],
    [656, 196, 701],
    [656, 701, 3],
    [640, 3, 708],
    [640, 708, 51],
    [670, 419, 669],
    [669, 419, 703],
    [669, 703, 248],
    [641, 248, 710],
    [641, 710, 281],
    [726, 281, 275],
    [193, 8, 685],
    [193, 685, 690],
    [193, 690, 687],
    [687, 690, 122],
    [122, 690, 692],
    [122, 692, 699],
    [122, 699, 694],
    [694, 699, 196],
    [196, 699, 697],
    [196, 697, 706],
    [196, 706, 701],
    [701, 706, 3],
    [3, 706, 704],
    [3, 704, 713],
    [3, 713, 708],
    [708, 713, 51],
    [51, 713, 711],
    [51, 711, 681],
    [51, 45, 681],
    [45, 681, 649],
    [417, 8, 686],
    [417, 686, 691],
    [417, 691, 689],
    [689, 691, 351],
    [351, 691, 693],
    [351, 693, 700],
    [351, 700, 696],
    [696, 700, 419],
    [419, 700, 698],
    [419, 698, 707],
    [419, 703, 707],
    [703, 707, 248],
    [248, 707, 705],
    [248, 705, 714],
    [248, 714, 710],
    [710, 714, 281],
    [281, 714, 712],
    [281, 712, 683],
    [281, 683, 275],
    [275, 683, 651],
    [685, 8, 168],
    [685, 168, 690],
    [690, 168, 688],
    [690, 688, 6],
    [690, 6, 692],
    [692, 6, 699],
    [699, 6, 695],
    [699, 695, 197],
    [699, 197, 697],
    [697, 197, 706],
    [706, 197, 702],
    [706, 702, 195],
    [706, 195, 704],
    [704, 195, 713],
    [713, 195, 709],
    [713, 709, 5],
    [713, 5, 711],
    [711, 5, 681],
    [681, 5, 682],
    [681, 682, 649],
    [649, 682, 4],
    [686, 8, 168],
    [686, 168, 691],
    [691, 168, 688],
    [691, 688, 6],
    [691, 6, 693],
    [693, 6, 700],
    [700, 6, 695],
    [700, 695, 197],
    [700, 197, 698],
    [698, 197, 707],
    [707, 197, 702],
    [707, 702, 195],
    [707, 195, 705],
    [705, 195, 714],
    [714, 195, 709],
    [714, 709, 5],
    [714, 5, 712],
    [712, 5, 683],
    [683, 5, 682],
    [683, 682, 651],
    [651, 682, 4],
    [198, 49, 131],
    [131, 49, 48],
    [131, 48, 115],
    [115, 48, 219],
    [115, 219, 218],
    [49, 102, 48],
    [102, 48, 64],
    [115, 220, 218],
    [220, 218, 237],
    [220, 237, 727],
    [45, 646, 648],
    [45, 648, 649],
    [649, 648, 4],
    [4, 648, 650],
    [4, 650, 652],
    [4, 651, 652],
    [651, 652, 275],
    [275, 652, 654],
    [275, 654, 728],
    [728, 654, 457],
    [440, 457, 438],
    [440, 438, 344],
    [344, 438, 439],
    [344, 439, 278],
    [278, 294, 331],
    [278, 279, 331],
    [420, 360, 279],
    [360, 279, 278],
    [360, 344, 278],
    [48, 64, 219],
    [219, 64, 235],
    [219, 235, 59],
    [219, 59, 166],
    [219, 218, 166],
    [218, 166, 79],
    [218, 79, 239],
    [218, 237, 239],
    [237, 646, 44],
    [647, 646, 44],
    [647, 646, 648],
    [647, 648, 1],
    [1, 648, 650],
    [1, 650, 652],
    [1, 652, 653],
    [653, 652, 654],
    [653, 654, 274],
    [274, 654, 457],
    [457, 728, 440],
    [457, 459, 438],
    [438, 459, 309],
    [438, 309, 392],
    [438, 392, 439],
    [439, 392, 289],
    [439, 289, 455],
    [439, 455, 294],
    [294, 455, 460],
    [278, 439, 294],
    [237, 239, 241],
    [237, 241, 44],
    [44, 241, 125],
    [44, 125, 647],
    [653, 19, 354],
    [274, 354, 461],
    [274, 461, 457],
    [457, 461, 459],
    [64, 240, 235],
    [235, 240, 75],
    [235, 59, 75],
    [59, 75, 717],
    [59, 166, 717],
    [166, 717, 60],
    [166, 60, 79],
    [79, 60, 718],
    [79, 718, 238],
    [79, 238, 239],
    [239, 238, 241],
    [125, 647, 19],
    [19, 647, 1],
    [19, 1, 653],
    [354, 653, 274],
    [459, 461, 458],
    [459, 458, 309],
    [309, 458, 719],
    [309, 290, 719],
    [309, 290, 392],
    [392, 290, 720],
    [392, 720, 289],
    [289, 720, 305],
    [289, 305, 455],
    [455, 294, 460],
    [455, 305, 460],
    [240, 75, 99],
    [240, 99, 97],
    [75, 60, 99],
    [75, 717, 60],
    [60, 99, 20],
    [60, 718, 20],
    [20, 718, 238],
    [20, 99, 242],
    [20, 238, 242],
    [238, 242, 241],
    [241, 242, 141],
    [241, 141, 125],
    [125, 141, 94],
    [125, 94, 19],
    [19, 94, 354],
    [354, 94, 370],
    [354, 370, 461],
    [461, 462, 458],
    [461, 370, 462],
    [458, 462, 250],
    [458, 719, 250],
    [250, 462, 328],
    [250, 328, 290],
    [250, 719, 290],
    [290, 720, 305],
    [290, 328, 305],
    [305, 460, 328],
    [460, 328, 326],
    [99, 97, 242],
    [97, 242, 141],
    [97, 141, 2],
    [2, 141, 94],
    [2, 94, 370],
    [2, 370, 326],
    [326, 370, 462],
    [326, 462, 328],
    [641, 248, 730],
    [248, 730, 669],
    [669, 730, 399],
    [730, 456, 641],
    [730, 456, 399],
    [640, 3, 729],
    [3, 729, 656],
    [729, 656, 174],
    [729, 174, 236],
    [729, 236, 640],
]

LEFT_NARE_POINT = [
    [79, 238, 718],
    [718, 238, 20],
    [79, 166, 60],
    [79, 718, 60],
    [718, 20, 60],
    [166, 60, 717],
    [166, 59, 717],
    [59, 75, 717],
    [60, 75, 717],
]

RIGHT_NARE_POINT = [
    [309, 458, 719],
    [250, 458, 719],
    [309, 719, 290],
    [250, 719, 290],
    [309, 392, 290],
    [392, 720, 290],
    [290, 720, 305],
    [392, 720, 289],
    [305, 720, 289],
]
