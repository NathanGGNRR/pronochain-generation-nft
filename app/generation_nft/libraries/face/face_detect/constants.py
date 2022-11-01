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

File: app/generation_nft/libraries/face/face_detect/contants.py
"""

from app.settings import settings

CAFFE_FILES = [
    {
        "url": f"https://drive.google.com/u/1/uc?id={settings.DEPLOY_PROTOTXT_URL_ID}&export=download",
        "file": settings.FACE_DETECT_DEPLOY_FILE,
        "parent_path": settings.FACE_DETECT_MODELS_PATH,
    },
    {
        "url": f"https://drive.google.com/u/1/uc?id={settings.CAFFEMODEL_URL_ID}&export=download",
        "file": settings.FACE_DETECT_CAFFE_FILE,
        "parent_path": settings.FACE_DETECT_MODELS_PATH,
    },
]
