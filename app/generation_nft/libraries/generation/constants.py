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

File: app/generation_nft/libraries/generation/constants.py
"""
from enum import Enum

from app.generation_nft_db.models.countries import Country
from app.generation_nft_db.models.names import Name
from app.generation_nft_db.models.nft_parts import Color, Element
from app.generation_nft_db.models.players import Player


class PartType(Enum):
    """Part type liste.

    Args:
        Enum (enum): enumération.
    """

    PICTURE = 1
    TEXT = 2
    COLOR = 3
    TEXT_COLOR = 4
    TEXT_VALUE = 5


class ValueType(Enum):
    """Value type liste.

    Args:
        Enum (enum): enumération.
    """

    ELEMENT = 1
    COLOR = 2
    NAME = 3
    COUNTRY = 4
    PLAYER = 5
    TEXT = 6


class PictureChannel(Enum):
    """Picture channel liste.

    Args:
        Enum (enum): enumération.
    """

    RGB = 1
    RGBA = 2


class PartName(Enum):
    """Part name liste.

    Args:
        Enum (enum): enumération.
    """

    CARD_SHAPE = "card_shape"
    CARD_PATTERN = "card_pattern"
    CARD_COLOR = "card_color"
    SHIRT_PATTERN = "shirt_pattern"
    CREST_SHAPE = "crest_shape"
    CREST_PATTERN = "crest_pattern"
    CREST_CONTENT = "crest_content"
    PLAYER_PICTURE = "player_picture"
    PLAYER = "player"
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"
    COUNTRY_FLAG = "country_flag"
    SKIN_COLOR = "skin_color"
    MOUTH_COLOR = "mouth_color"
    HAIR_COLOR = "hair_color"
    EYES_COLOR = "eyes_color"
    IRIS_PICTURE = "iris_picture"
    SHIRT_PICTURE = "shirt_picture"
    PEC_PICTURE = "pec_picture"
    FIRST_COLOR = "first_color"
    SECOND_COLOR = "second_color"
    STAR = "star"
    MENTAL = "icon_mental"
    PHYSICAL = "icon_physical"
    AGE = "icon_age"
    HEIGHT = "icon_height"
    WEIGHT = "icon_weight"
    CLUB = "club"
    POSITION = "icon_position"
    MENTAL_NOTE = "mental_note"
    PHYSICAL_NOTE = "physical_note"
    POSITION_NOTE = "position_note"
    NFT_COUNT = "nft_count"
    GLOBAL_NOTE = "global_note"


RARITIES_PARTS = [
    {
        "name": PartName.CARD_SHAPE.value,
        "model": Element,
        "element_type_code": 1,
        "nft_part_code": 1,
        "type": PartType.PICTURE.value,
        "channel": PictureChannel.RGBA.value,
        "add_to_combination": True,
        "value_type": ValueType.ELEMENT.value,
    },
    {
        "name": PartName.CARD_PATTERN.value,
        "model": Element,
        "element_type_code": 2,
        "nft_part_code": 1,
        "type": PartType.PICTURE.value,
        "channel": PictureChannel.RGBA.value,
        "add_to_combination": True,
        "value_type": ValueType.ELEMENT.value,
    },
    {
        "name": PartName.CARD_COLOR.value,
        "model": Color,
        "nft_part_code": 1,
        "type": PartType.COLOR.value,
        "add_to_combination": True,
        "value_type": ValueType.COLOR.value,
    },
    {
        "name": PartName.SHIRT_PATTERN.value,
        "model": Element,
        "element_type_code": 2,
        "nft_part_code": 2,
        "type": PartType.PICTURE.value,
        "channel": PictureChannel.RGBA.value,
        "add_to_combination": True,
        "value_type": ValueType.ELEMENT.value,
    },
    {
        "name": PartName.CREST_SHAPE.value,
        "model": Element,
        "element_type_code": 1,
        "nft_part_code": 3,
        "type": PartType.PICTURE.value,
        "channel": PictureChannel.RGB.value,
        "add_to_combination": True,
        "value_type": ValueType.ELEMENT.value,
    },
    {
        "name": PartName.CREST_PATTERN.value,
        "model": Element,
        "element_type_code": 2,
        "nft_part_code": 3,
        "type": PartType.PICTURE.value,
        "channel": PictureChannel.RGB.value,
        "add_to_combination": True,
        "value_type": ValueType.ELEMENT.value,
    },
    {
        "name": PartName.CREST_CONTENT.value,
        "model": Element,
        "element_type_code": 3,
        "nft_part_code": 3,
        "type": PartType.PICTURE.value,
        "with_parent": PartName.CREST_SHAPE.value,
        "channel": PictureChannel.RGB.value,
        "add_to_combination": True,
        "value_type": ValueType.ELEMENT.value,
    },
    {
        "name": PartName.PLAYER_PICTURE.value,
        "model": Player,
        "type": PartType.PICTURE.value,
        "save_model": True,
        "save_model_name": PartName.PLAYER.value,
        "channel": PictureChannel.RGB.value,
        "add_to_combination": True,
        "value_type": ValueType.PLAYER.value,
    },
]

RANDOM_PARTS = [
    {
        "name": PartName.FIRST_NAME.value,
        "model": Name,
        "name_type_code": 1,
        "type": PartType.TEXT_VALUE.value,
        "add_to_combination": True,
        "value_type": ValueType.NAME.value,
    },
    {
        "name": PartName.LAST_NAME.value,
        "model": Name,
        "name_type_code": 2,
        "type": PartType.TEXT_VALUE.value,
        "add_to_combination": True,
        "value_type": ValueType.NAME.value,
    },
    {
        "name": PartName.COUNTRY_FLAG.value,
        "model": Country,
        "type": PartType.PICTURE.value,
        "channel": PictureChannel.RGBA.value,
        "add_to_combination": True,
        "value_type": ValueType.COUNTRY.value,
    },
    {
        "name": PartName.SKIN_COLOR.value,
        "model": Color,
        "face_part_code": 1,
        "type": PartType.COLOR.value,
        "add_to_combination": True,
        "value_type": ValueType.COLOR.value,
    },
    {
        "name": PartName.MOUTH_COLOR.value,
        "model": Color,
        "depend_face_part_color": True,
        "type": PartType.COLOR.value,
        "add_to_combination": True,
        "value_type": ValueType.COLOR.value,
    },
    {
        "name": PartName.HAIR_COLOR.value,
        "model": Color,
        "face_part_code": 2,
        "type": PartType.COLOR.value,
        "add_to_combination": True,
        "value_type": ValueType.COLOR.value,
    },
    {
        "name": PartName.EYES_COLOR.value,
        "model": Color,
        "face_part_code": 3,
        "type": PartType.COLOR.value,
        "add_to_combination": True,
        "value_type": ValueType.COLOR.value,
    },
]

CONSTANT_PARTS = [
    {
        "name": PartName.IRIS_PICTURE.value,
        "model": Element,
        "element_code": 46,
        "type": PartType.PICTURE.value,
        "channel": PictureChannel.RGBA.value,
        "add_to_combination": False,
    },
    {
        "name": PartName.PEC_PICTURE.value,
        "model": Element,
        "element_code": 35,
        "type": PartType.PICTURE.value,
        "channel": PictureChannel.RGBA.value,
        "add_to_combination": False,
    },
    {
        "name": PartName.SHIRT_PICTURE.value,
        "model": Element,
        "element_code": 36,
        "type": PartType.PICTURE.value,
        "channel": PictureChannel.RGB.value,
        "add_to_combination": False,
    },
    {
        "name": PartName.FIRST_COLOR.value,
        "model": Color,
        "type": PartType.COLOR.value,
        "add_to_combination": False,
    },
    {
        "name": PartName.SECOND_COLOR.value,
        "model": Color,
        "type": PartType.COLOR.value,
        "add_to_combination": False,
    },
    {
        "name": PartName.STAR.value,
        "model": Element,
        "element_code": 65,
        "type": PartType.PICTURE.value,
        "channel": PictureChannel.RGBA.value,
        "add_to_combination": False,
    },
    {
        "name": PartName.MENTAL.value,
        "model": Element,
        "element_code": 44,
        "type": PartType.PICTURE.value,
        "channel": PictureChannel.RGBA.value,
        "add_to_combination": False,
    },
    {
        "name": PartName.PHYSICAL.value,
        "model": Element,
        "element_code": 45,
        "type": PartType.PICTURE.value,
        "channel": PictureChannel.RGBA.value,
        "add_to_combination": False,
    },
    {
        "name": PartName.AGE.value,
        "model": Element,
        "element_code": 41,
        "type": PartType.PICTURE.value,
        "channel": PictureChannel.RGBA.value,
        "add_to_combination": False,
    },
    {
        "name": PartName.HEIGHT.value,
        "model": Element,
        "element_code": 42,
        "type": PartType.PICTURE.value,
        "channel": PictureChannel.RGBA.value,
        "add_to_combination": False,
    },
    {
        "name": PartName.WEIGHT.value,
        "model": Element,
        "element_code": 43,
        "type": PartType.PICTURE.value,
        "channel": PictureChannel.RGBA.value,
        "add_to_combination": False,
    },
]
