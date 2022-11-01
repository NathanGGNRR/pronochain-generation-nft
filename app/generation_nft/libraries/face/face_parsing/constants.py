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

File: app/generation_nft/libraries/face/face_parsing/constants.py
"""
from enum import Enum
from pathlib import Path

import torch

from app.generation_nft.libraries.face.face_landmarks.constants import (
    DOWN_NOSE,
    EXTERN_MOUTH,
    INTERN_MOUTH,
    LEFT_EYE,
    LEFT_EYE_IRIS,
    LEFT_EYE_LEFT_POINT,
    LEFT_EYE_RIGHT_POINT,
    LEFT_EYELID,
    LEFT_NECK,
    LEFT_UP_EYE,
    LEFT_UP_EYELID,
    NOSE,
    RIGHT_EYE,
    RIGHT_EYE_IRIS,
    RIGHT_EYE_LEFT_POINT,
    RIGHT_EYE_RIGHT_POINT,
    RIGHT_EYELID,
    RIGHT_NECK,
    RIGHT_UP_EYE,
    RIGHT_UP_EYELID,
)
from app.generation_nft.libraries.face.face_parsing.model import BiSeNet
from app.settings import settings


class FaceParts(Enum):
    """Face parts liste.

    Args:
        Enum (enum): enumération.
    """

    BACKGROUND = 0
    SKIN = 1
    RIGHT_BROW = 2
    LEFT_BROW = 3
    RIGHT_EYE = 4
    LEFT_EYE = 5
    GLASSES = 6
    RIGHT_EAR = 7
    LEFT_EAR = 8
    HEADWEAR = 9
    NOSE = 10
    MOUTH_INTERIOR = 11
    TOP_LIP = 12
    BOTTOM_LIP = 13
    NECK = 14
    EARWEAR = 15
    CLOTHING = 16
    HAIR = 17
    NECKWEAR = 18


class PartName(Enum):
    """Part name liste.

    Args:
        Enum (enum): enumération.
    """

    BACKGROUND = ("background",)
    LEFT_EYE_CLEAN = ("left_eye_clean",)
    RIGHT_EYE_CLEAN = ("right_eye_clean",)
    LEFT_EYELID_CLEAN = ("left_eyelid_clean",)
    RIGHT_EYELID_CLEAN = ("right_eyelid_clean",)
    NOSE_CLEAN = ("nose_clean",)
    INTERN_MOUTH_CLEAN = ("intern_mouth_clean",)
    MOUTH_CLEAN = ("mouth_clean",)
    HAIR = ("hair",)
    LEFT_EAR = ("left_ear",)
    RIGHT_EAR = ("right_ear",)
    LEFT_BROW = ("left_brow",)
    RIGHT_BROW = ("right_brow",)
    BEARD = ("beard",)
    SKIN = ("skin",)
    NOSE = ("nose",)
    LEFT_EYE = ("left_eye",)
    RIGHT_EYE = ("right_eye",)
    MOUTH = ("mouth",)
    NECK = "neck"


FACE_PARSING_MODELS = [
    {
        "url": f"https://drive.google.com/u/1/uc?id={settings.FACE_PARTS_URL_ID}&export=download",
        "file": settings.FACE_PARSING_MODEL_FILE,
        "parent_path": settings.FACE_PARSING_MODEL_PATH,
    }
]


class Config(object):
    """Classes de stockage contenant toutes les configurations nécessaires au bon fonctionnement du deep learning."""

    def __init__(self, device: str, num_classes: int = 19, input_channels: int = 3):
        """Initialisation de la classe Config.

        Args:
            device (str): valeurs possibles : "cuda:0" ou "cpu".
            num_classes (int, optional): nombre d'éléments différents à détecter. Par défaut 19.
            input_channels (int, optional): format des données d'entrée. Par défaut 3.
        """
        self.PRETRAINED_PATH = f"{settings.GENERATION_NFT_PATH}/libraries/face/face_parsing/pre_trained"  # chemin des modèles pré-entrainés
        self.FACE_PART_CLASS_RGB_VALUES = [
            [
                FaceParts.BACKGROUND.value,
                FaceParts.BACKGROUND.value,
                FaceParts.BACKGROUND.value,
            ],
            [FaceParts.SKIN.value, FaceParts.SKIN.value, FaceParts.SKIN.value],
            [
                FaceParts.RIGHT_BROW.value,
                FaceParts.RIGHT_BROW.value,
                FaceParts.RIGHT_BROW.value,
            ],
            [
                FaceParts.LEFT_BROW.value,
                FaceParts.LEFT_BROW.value,
                FaceParts.LEFT_BROW.value,
            ],
            [
                FaceParts.RIGHT_EYE.value,
                FaceParts.RIGHT_EYE.value,
                FaceParts.RIGHT_EYE.value,
            ],
            [
                FaceParts.LEFT_EYE.value,
                FaceParts.LEFT_EYE.value,
                FaceParts.LEFT_EYE.value,
            ],
            [
                FaceParts.GLASSES.value,
                FaceParts.GLASSES.value,
                FaceParts.GLASSES.value,
            ],
            [
                FaceParts.RIGHT_EAR.value,
                FaceParts.RIGHT_EAR.value,
                FaceParts.RIGHT_EAR.value,
            ],
            [
                FaceParts.LEFT_EAR.value,
                FaceParts.LEFT_EAR.value,
                FaceParts.LEFT_EAR.value,
            ],
            [
                FaceParts.HEADWEAR.value,
                FaceParts.HEADWEAR.value,
                FaceParts.HEADWEAR.value,
            ],
            [
                FaceParts.NOSE.value,
                FaceParts.NOSE.value,
                FaceParts.NOSE.value,
            ],
            [
                FaceParts.MOUTH_INTERIOR.value,
                FaceParts.MOUTH_INTERIOR.value,
                FaceParts.MOUTH_INTERIOR.value,
            ],
            [
                FaceParts.TOP_LIP.value,
                FaceParts.TOP_LIP.value,
                FaceParts.TOP_LIP.value,
            ],
            [
                FaceParts.BOTTOM_LIP.value,
                FaceParts.BOTTOM_LIP.value,
                FaceParts.BOTTOM_LIP.value,
            ],
            [
                FaceParts.NECK.value,
                FaceParts.NECK.value,
                FaceParts.NECK.value,
            ],
            [FaceParts.EARWEAR.value, FaceParts.EARWEAR.value, FaceParts.EARWEAR.value],
            [
                FaceParts.CLOTHING.value,
                FaceParts.CLOTHING.value,
                FaceParts.CLOTHING.value,
            ],
            [FaceParts.HAIR.value, FaceParts.HAIR.value, FaceParts.HAIR.value],
            [
                FaceParts.NECKWEAR.value,
                FaceParts.NECKWEAR.value,
                FaceParts.NECKWEAR.value,
            ],
        ]  # différentes valeurs de RGB du masque correspondant au partie d'un visage

        self.FACE_PART_COLORS = [
            [255, 255, 255],  # BACKGROUND BLANC
            [255, 0, 85],  # SKIN BLEU
            [255, 170, 0],  # RIGHT_BROW BLEU CLAIRE
            [255, 85, 0],  # LEFT_BROW BLEU FONCER
            [255, 0, 170],  # RIGHT_EYE ROSE FONCER
            [0, 255, 0],  # LEFT_EYE VERT CLAIRE
            [85, 255, 0],  # GLASSES IDK
            [0, 0, 255],  # RIGHT_EAR ROUGE
            [255, 0, 255],  # LEFT_EAR VERT
            [0, 255, 170],  # HEADWEAR IDK
            [170, 255, 0],  # NOSE TURQUOISE
            [85, 0, 255],  # MOUTH_INTERIOR ROSE FONCER
            [170, 0, 255],  # TOP LIP ROSE CLAIRE
            [0, 85, 255],  # BOTTOM_LIP ORANGE CLAIRE
            [0, 170, 255],  # NECK JAUNE
            [255, 255, 0],  # EARWEAR
            [0, 170, 255],  # CLOTHING CYAN
            [0, 128, 255],  # HAIR ORANGE
            [0, 255, 85],  # VERT
        ]  # nouvelle colorisation après la prédiction, permet de visualiser le résultat obtenu pour le modèle des parties du visages

        self.CLEAN_FACE_PARTS = [
            {
                "name": PartName.BACKGROUND.value,
                "clean_color": self.FACE_PART_COLORS[0],
                "parts": [
                    FaceParts.CLOTHING.value,
                    FaceParts.NECKWEAR.value,
                    FaceParts.NECK.value,
                ],
            },
            {
                "name": PartName.SKIN.value,
                "clean_color": self.FACE_PART_COLORS[1],
                "parts": [
                    FaceParts.SKIN.value,
                    FaceParts.RIGHT_EYE.value,
                    FaceParts.LEFT_EYE.value,
                    FaceParts.NOSE.value,
                    FaceParts.MOUTH_INTERIOR.value,
                    FaceParts.TOP_LIP.value,
                    FaceParts.BOTTOM_LIP.value,
                ],
            },
            {
                "name": PartName.RIGHT_BROW.value,
                "clean_color": self.FACE_PART_COLORS[2],
                "parts": [
                    FaceParts.RIGHT_BROW.value,
                    FaceParts.LEFT_BROW.value,
                ],
            },
            {
                "name": PartName.RIGHT_EAR.value,
                "clean_color": self.FACE_PART_COLORS[7],
                "parts": [
                    FaceParts.RIGHT_EAR.value,
                    FaceParts.LEFT_EAR.value,
                ],
            },
            {
                "name": PartName.NOSE.value,
                "clean_color": self.FACE_PART_COLORS[10],
                "parts": [
                    FaceParts.NOSE.value,
                ],
            },
        ]

        self.CLEAN_HAIR_PARTS = [
            {
                "name": PartName.BACKGROUND.value,
                "clean_color": self.FACE_PART_COLORS[0],
                "parts": [
                    FaceParts.CLOTHING.value,
                    FaceParts.NECKWEAR.value,
                    FaceParts.NECK.value,
                    FaceParts.SKIN.value,
                    FaceParts.RIGHT_EYE.value,
                    FaceParts.LEFT_EYE.value,
                    FaceParts.NOSE.value,
                    FaceParts.MOUTH_INTERIOR.value,
                    FaceParts.TOP_LIP.value,
                    FaceParts.BOTTOM_LIP.value,
                    FaceParts.RIGHT_BROW.value,
                    FaceParts.LEFT_BROW.value,
                    FaceParts.LEFT_EAR.value,
                    FaceParts.RIGHT_EAR.value,
                    FaceParts.NOSE.value,
                ],
            },
            {
                "name": PartName.HAIR.value,
                "clean_color": self.FACE_PART_COLORS[-2],
                "parts": [
                    FaceParts.HAIR.value,
                ],
            },
        ]

        # Converti le format device texte en format torch device
        self.DEVICE = torch.device(device)
        self.INPUT_CHANNELS = input_channels  # format des données d'entrée
        self.NUM_CLASSES = num_classes  # nombre de parties à détecter
        self.FACE_MODEL = "BiSeNet"  # nom du modèle BiSeNet
        # taille recommandée par le machine learning. Prendre des images ayant le même ratio 256x256 ...
        self.INPUT_IMAGE_SIZE = 512
        self.MODEL = BiSeNet(
            resnet=settings.RESNET_URL,
            n_classes=self.NUM_CLASSES,
        )
        self.PRETRAINED_MODEL_PATH = Path(f"{self.PRETRAINED_PATH}/face_parts.pth")
        self.SKIN_HSV_COLOR = [130, 255, 255]
        self.HAIR_HSV_COLOR = [15, 255, 255]
        self.SKIN_COLOR = self.FACE_PART_COLORS[1]
        self.HAIR_COLOR = self.FACE_PART_COLORS[-2]
        self.BROW_COLOR = self.FACE_PART_COLORS[2]
        self.EAR_COLOR = self.FACE_PART_COLORS[7]
        self.NOSE_COLOR = self.FACE_PART_COLORS[10]
        self.EAR_POINT = 127

        self.LANDMARK_SELECTED_PARTS = [
            {
                "name": PartName.LEFT_EYE_CLEAN.value,
                "clean_func": "to_skin_color",
                "points": LEFT_EYE,
            },
            {
                "name": PartName.RIGHT_EYE_CLEAN.value,
                "clean_func": "to_skin_color",
                "points": RIGHT_EYE,
            },
            {
                "name": PartName.LEFT_EYELID_CLEAN.value,
                "clean_func": "to_skin_color",
                "points": LEFT_EYELID,
            },
            {
                "name": PartName.RIGHT_EYELID_CLEAN.value,
                "clean_func": "to_skin_color",
                "points": RIGHT_EYELID,
            },
            {
                "name": PartName.NOSE_CLEAN.value,
                "clean_func": "to_skin_color",
                "points": NOSE,
                "offset_y": 20,
            },
            {
                "name": PartName.INTERN_MOUTH_CLEAN.value,
                "clean_func": "to_skin_color",
                "points": INTERN_MOUTH,
            },
            {
                "name": PartName.MOUTH_CLEAN.value,
                "clean_func": "to_skin_color",
                "points": EXTERN_MOUTH,
                "offset_y": 10,
            },
        ]

        self.SELECTED_PARTS = [
            {
                "name": PartName.RIGHT_EAR.value,
                "clean_func": "to_skin_color",
                "hsv_color": [0, 255, 255],
            },
            {
                "name": PartName.RIGHT_BROW.value,
                "clean_func": "to_skin_color",
                "hsv_color": [100, 255, 255],
            },
            {
                "name": PartName.HAIR.value,
                "clean_func": "to_skin_color",
                "hsv_color": self.HAIR_HSV_COLOR,
            },
            {
                "name": PartName.SKIN.value,
                "draw_func": "skin",
                "hsv_color": self.SKIN_HSV_COLOR,
            },
            {
                "name": PartName.RIGHT_EAR.value,
                "draw_func": "ear",
                "hsv_color": [0, 255, 255],
            },
            {
                "name": PartName.HAIR.value,
                "draw_func": "hair",
                "hsv_color": self.HAIR_HSV_COLOR,
                "depend_on": PartName.SKIN.value,
            },
            {
                "name": PartName.RIGHT_BROW.value,
                "draw_func": "brow",
                "hsv_color": [100, 255, 255],
            },
            # {
            #     "name": PartName.BEARD.value,
            #     "draw_func": "beard",
            #     "depend_on": PartName.RIGHT_EAR.value
            # },
            {
                "name": PartName.NOSE.value,
                "draw_func": "nose",
                "hsv_color": [80, 255, 255],
                "depend_on": PartName.NOSE_CLEAN.value,
                "parts": [DOWN_NOSE],
            },
            {
                "name": PartName.LEFT_EYE.value,
                "draw_func": "eye",
                "depend_on": PartName.LEFT_EYE_CLEAN.value,
                "parts": [
                    LEFT_EYE_IRIS,
                    LEFT_UP_EYE,
                    LEFT_UP_EYELID,
                    LEFT_EYELID,
                    LEFT_EYE_LEFT_POINT,
                    LEFT_EYE_RIGHT_POINT,
                ],
            },
            {
                "name": PartName.RIGHT_EYE.value,
                "draw_func": "eye",
                "depend_on": PartName.RIGHT_EYE_CLEAN.value,
                "parts": [
                    RIGHT_EYE_IRIS,
                    RIGHT_UP_EYE,
                    RIGHT_UP_EYELID,
                    RIGHT_EYELID,
                    RIGHT_EYE_LEFT_POINT,
                    RIGHT_EYE_RIGHT_POINT,
                ],
            },
            {
                "name": PartName.MOUTH.value,
                "draw_func": "mouth",
                "depend_on": PartName.MOUTH_CLEAN.value,
                "parts": [INTERN_MOUTH],
            },
            {
                "name": PartName.NECK.value,
                "draw_func": "neck",
                "parts": [LEFT_NECK, RIGHT_NECK],
            },
        ]
