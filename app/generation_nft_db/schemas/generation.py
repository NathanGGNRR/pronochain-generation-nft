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

File: app/generation_nft_db/schemas/generation.py
"""
from typing import Optional, Union

from fastapi import Form
from pydantic import BaseModel

from app.generation_nft_db.constants import (
    CardColor,
    CardPatternCode,
    CardShapeCode,
    CountryCode,
    EyesColor,
    HairColor,
    ShirtCrestContentCode,
    ShirtCrestPatternCode,
    ShirtCrestShapeCode,
    ShirtPatternCode,
    SkinColor,
)
from app.generation_nft_db.models.countries import Country
from app.generation_nft_db.models.names import Name
from app.generation_nft_db.models.nft_parts import Color, Element
from app.generation_nft_db.models.players import Player
from app.generation_nft_db.models.rarities import Rarity as RarityModel
from app.generation_nft_db.schemas.rarities import Rarity as RaritySchema


class CreateGeneration(BaseModel):
    """CreateGeneration schéma.

    Args:
        BaseModel (BaseModel): modèle pydantic.
    """

    card_shape_code: CardShapeCode
    card_pattern_code: CardPatternCode
    card_color: CardColor
    shirt_pattern_code: ShirtPatternCode
    shirt_crest_shape_code: ShirtCrestShapeCode
    shirt_crest_pattern_code: ShirtCrestPatternCode
    shirt_crest_content_code: ShirtCrestContentCode
    player_code: int = Form(...)
    player_first_name: str = Form(...)
    player_last_name: str = Form(...)
    country_code: CountryCode
    player_hair_color: HairColor
    player_skin_color: SkinColor
    player_eyes_color: EyesColor
    get_picture: bool = Form(False)


class GenerationPart(BaseModel):
    """GenerationPart schéma.

    Args:
        BaseModel (BaseModel): modèle pydantic.
    """

    name: str
    type: int
    channel: Optional[int]
    value: Union[Element, Color, Player, Name, Country, str]
    value_type: Optional[int]
    save_model: Optional[bool]
    save_model_name: Optional[str]
    add_to_combination: Optional[bool]
    rarity_length: Optional[int]
    rarity: Optional[Union[RarityModel, RaritySchema]]
    note: Optional[bool]

    class Config:
        """Classe config d'un modèle pydantic."""

        arbitrary_types_allowed = True


class ResponseIsAlive(BaseModel):
    """ResponseIsAlive schéma.

    Args:
        BaseModel (BaseModel): modèle pydantic.
    """

    status: int
    is_active: bool
