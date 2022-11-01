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

File: app/generation_nft/libraries/card/constants.py
"""
from enum import Enum

from app.generation_nft.libraries.generation.constants import PartName


class Type(Enum):
    """Classe héritant de la classe native Enum. Permet d'énumérer les différents types des parties à rajouter sur la carte."""

    FONT = 0
    PICTURE = 1
    PICTURES = 2


class Content(Enum):
    """Classe héritant de la classe native Enum. Permet d'énumérer les différents types de contenu à rajouter sur la carte."""

    TEXT = 0
    ATTRIBUTE = 1


class Anchor(Enum):
    """Classe héritant de la classe native Enum. Permet d'énumérer les différents référence de position des parties à rajouter sur la carte."""

    DEFAULT = "lt"
    TOP_MIDDLE = "mt"
    TOP_RIGHT = "tr"
    BOTTOM_MIDDLE = "mb"


class Direction(Enum):
    """Classe héritant de la classe native Enum. Permet d'énumérer les directions vers où boucler un élement sur la carte."""

    LEFT = 0
    RIGHT = 1


class PictureName(Enum):
    """Classe héritant de la classe native Enum. Permet d'énumérer les différents images avec des spécificités à rajouter sur la carte."""

    SHIRT_FACE = 0
    STAR = 1
    FLAG_AND_CREST = 2
    POSITION = 3
    MENTAL = 4
    PHYSICAL = 5
    AGE = 6
    HEIGHT = 7
    WEIGHT = 8


class OrientationResize(Enum):
    """Classe héritant de la classe native Enum. Permet d'énumérer les différents orientations possibles pour redimensionner une image."""

    WIDTH = 0
    HEIGHT = 1


MARGIN = 100
FONT_SIZE_NOTE = 100

WHITE_COLOR = [254, 254, 254]
GRAY_COLOR = [204, 204, 204]
STAR_COLOR = [49, 236, 249]

COORDINATES_PARTS = [
    {
        "type": Type.FONT.value,
        "content": Content.ATTRIBUTE.value,
        "value": "global_note",
        "color": [255, 0, 0],
        "anchor": Anchor.DEFAULT.value,
        "fill": WHITE_COLOR,
        "size": 640,
        "opacity": 255,
    },
    {
        "type": Type.FONT.value,
        "content": Content.TEXT.value,
        "value": "/100",
        "color": [255, 0, 0],
        "anchor": Anchor.DEFAULT.value,
        "depending": True,
        "last_x": True,
        "last_y": False,
        "fill": GRAY_COLOR,
        "size": 250,
        "opacity": 160,
    },
    {
        "type": Type.FONT.value,
        "content": Content.ATTRIBUTE.value,
        "value": PartName.FIRST_NAME.value,
        "color": [0, 255, 0],
        "anchor": Anchor.TOP_MIDDLE.value,
        "fill": WHITE_COLOR,
        "size": 250,
        "opacity": 255,
    },
    {
        "type": Type.FONT.value,
        "content": Content.ATTRIBUTE.value,
        "value": PartName.LAST_NAME.value,
        "anchor": Anchor.TOP_MIDDLE.value,
        "uppercase": True,
        "depending": True,
        "last_x": False,
        "last_y": True,
        "fill": WHITE_COLOR,
        "size": 300,
        "opacity": 255,
    },
    {
        "name": PictureName.FLAG_AND_CREST.value,
        "type": Type.PICTURES.value,
        "depending": True,
        "color": [0, 255, 0],
        "childs": [
            {
                "content": Content.ATTRIBUTE.value,
                "value": PartName.COUNTRY_FLAG.value,
                "resize": 350,
                "resize_orientation": OrientationResize.HEIGHT.value,
                "margin": 25,
            },
            {
                "content": Content.ATTRIBUTE.value,
                "value": "drawing_crest",
                "anchor": Anchor.TOP_MIDDLE.value,
                "with_text": "club",
                "resize": 350,
                "resize_orientation": OrientationResize.HEIGHT.value,
                "margin": 25,
            },
        ],
    },
    {
        "name": PictureName.SHIRT_FACE.value,
        "type": Type.PICTURE.value,
        "content": Content.ATTRIBUTE.value,
        "value": "drawing_shirt",
        "color": [0, 255, 255],
        "anchor": Anchor.BOTTOM_MIDDLE.value,
        "fade_in": True,
    },
    {
        "name": PictureName.STAR.value,
        "type": Type.PICTURE.value,
        "content": Content.ATTRIBUTE.value,
        "value": PartName.STAR.value,
        "color": [128, 128, 128],
        "loop": 5,
        "direction": Direction.LEFT.value,
        "anchor": Anchor.DEFAULT.value,
        "opacity": 128,
    },
    {
        "name": PictureName.POSITION.value,
        "type": Type.PICTURE.value,
        "content": Content.ATTRIBUTE.value,
        "value": PartName.POSITION.value,
        "color": [0, 0, 255],
        "anchor": Anchor.TOP_MIDDLE.value,
        "resize": 150,
        "resize_orientation": OrientationResize.HEIGHT.value,
        "with_text": PartName.POSITION_NOTE.value,
    },
    {
        "name": PictureName.MENTAL.value,
        "type": Type.PICTURE.value,
        "content": Content.ATTRIBUTE.value,
        "value": PartName.MENTAL.value,
        "color": [255, 0, 255],
        "anchor": Anchor.TOP_MIDDLE.value,
        "resize": 150,
        "resize_orientation": OrientationResize.HEIGHT.value,
        "with_text": PartName.MENTAL_NOTE.value,
    },
    {
        "name": PictureName.PHYSICAL.value,
        "type": Type.PICTURE.value,
        "content": Content.ATTRIBUTE.value,
        "value": PartName.PHYSICAL.value,
        "color": [255, 255, 0],
        "anchor": Anchor.TOP_MIDDLE.value,
        "resize": 150,
        "resize_orientation": OrientationResize.HEIGHT.value,
        "with_text": PartName.PHYSICAL_NOTE.value,
    },
    {
        "name": PictureName.AGE.value,
        "type": Type.PICTURE.value,
        "content": Content.ATTRIBUTE.value,
        "value": PartName.AGE.value,
        "color": [128, 0, 0],
        "anchor": Anchor.TOP_MIDDLE.value,
        "resize": 150,
        "resize_orientation": OrientationResize.HEIGHT.value,
        "with_text": "age_note",
    },
    {
        "name": PictureName.HEIGHT.value,
        "type": Type.PICTURE.value,
        "content": Content.ATTRIBUTE.value,
        "value": PartName.HEIGHT.value,
        "color": [0, 128, 0],
        "anchor": Anchor.TOP_MIDDLE.value,
        "resize": 150,
        "resize_orientation": OrientationResize.HEIGHT.value,
        "with_text": "height_note",
    },
    {
        "name": PictureName.WEIGHT.value,
        "type": Type.PICTURE.value,
        "content": Content.ATTRIBUTE.value,
        "value": PartName.WEIGHT.value,
        "color": [0, 0, 128],
        "anchor": Anchor.TOP_MIDDLE.value,
        "resize": 150,
        "resize_orientation": OrientationResize.HEIGHT.value,
        "with_text": "weight_note",
    },
    {
        "type": Type.FONT.value,
        "content": Content.ATTRIBUTE.value,
        "value": PartName.NFT_COUNT.value,
        "color": [128, 128, 0],
        "anchor": Anchor.TOP_MIDDLE.value,
        "fill": WHITE_COLOR,
        "size": 75,
        "opacity": 255,
    },
]
