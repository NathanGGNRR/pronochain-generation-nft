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

File: app/generation_nft_db/schemas/players.py
"""
from datetime import date
from typing import List, Optional

from fastapi import Form, Query
from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from app.generation_nft_db.schemas.clubs import ClubOut
from app.generation_nft_db.schemas.countries import CountryOut
from app.generation_nft_db.schemas.positions import PositionOut
from app.generation_nft_db.schemas.rarities import RarityOut


class Player(BaseModel):
    """Player schéma.

    Args:
        BaseModel (BaseModel): modèle pydantic.
    """

    code: int
    age: int
    birth: date
    height: int
    weight: int


class PlayerStat(BaseModel):
    """PlayerStat schéma.

    Args:
        BaseModel (BaseModel): modèle pydantic.
    """

    player_id: int
    stat_id: int
    value: int

    class Config:
        """Classe config d'un modèle pydantic."""

        orm_mode = True


class PlayerStatCreate(BaseModel):
    """PlayerStatCreate schéma.

    Args:
        BaseModel (BaseModel): modèle pydantic.
    """

    player_id: Optional[int]
    stat_id: int
    value: int


class PlayerOut(Player):
    """PlayerOut schéma.

    Args:
        Player (Player): modèle Player.
    """

    id: int
    cid: Optional[str]
    filename: Optional[str]

    class Config:
        """Classe config d'un modèle pydantic."""

        orm_mode = True


class PlayerNestedOut(PlayerOut):
    """PlayerNestedOut schéma.

    Args:
        PlayerOut (PlayerOut): modèle PlayerOut.
    """

    first_name: Optional[str]
    last_name: str
    countries: List[CountryOut]
    positions: List[PositionOut]
    stats: List[PlayerStat]
    club: ClubOut
    Rarity: RarityOut


@dataclass
class PlayerCreate:
    """PlayerCreate FastAPI dataclass pour les paramètres d'une route API."""

    code: int = Form(...)
    first_name: str = Form(...)
    last_name: str = Form(...)
    age: int = Form(...)
    birth: date = Form(...)
    height: int = Form(...)
    weight: int = Form(...)
    club_id: int = Form(...)
    rarity_id: int = Form(...)
    country_ids: Optional[List[int]] = Query(None)
    position_ids: Optional[List[int]] = Query(None)
    goalkeeping: int = Form(..., title="Goalkeeping")
    mental: int = Form(..., title="Mental")
    physical: int = Form(..., title="Physical")
    technical: int = Form(..., title="Technical")
    aerial_ability: int = Form(..., title="Aerial Ability")
    command_of_area: int = Form(..., title="Command Of Area")
    communication: int = Form(..., title="Communication")
    eccentricity: int = Form(..., title="Eccentricity")
    first_touch: int = Form(..., title="First Touch")
    handling: int = Form(..., title="Handling")
    kicking: int = Form(..., title="Kicking")
    one_on_ones: int = Form(..., title="One On Ones")
    passing: int = Form(..., title="Passing")
    tendency_to_punch: int = Form(..., title="Tendency To Punch")
    reflexes: int = Form(..., title="Reflexes")
    rushing_out: int = Form(..., title="Rushing Out")
    throwing: int = Form(..., title="Throwing")
    corners: int = Form(..., title="Corners")
    crossing: int = Form(..., title="Crossing")
    dribbling: int = Form(..., title="Dribbling")
    finishing: int = Form(..., title="Finishing")
    freekicks: int = Form(..., title="Freekicks")
    heading: int = Form(..., title="Heading")
    long_shots: int = Form(..., title="Long Shots")
    long_throws: int = Form(..., title="Long Throws")
    marking: int = Form(..., title="Marking")
    penalty_taking: int = Form(..., title="Penalty Taking")
    tackling: int = Form(..., title="Tackling")
    technique: int = Form(..., title="Technique")
    aggression: int = Form(..., title="Aggression")
    anticipation: int = Form(..., title="Anticipation")
    bravery: int = Form(..., title="Bravery")
    composure: int = Form(..., title="Composure")
    concentration: int = Form(..., title="Concentration")
    decisions: int = Form(..., title="Decisions")
    determination: int = Form(..., title="Determination")
    flair: int = Form(..., title="Flair")
    leadership: int = Form(..., title="Leadership")
    off_the_ball: int = Form(..., title="Off The Ball")
    positioning: int = Form(..., title="Positioning")
    teamwork: int = Form(..., title="Teamwork")
    vision: int = Form(..., title="Vision")
    workrate: int = Form(..., title="Workrate")
    consistency: int = Form(..., title="Consistency")
    dirtiness: int = Form(..., title="Dirtiness")
    versatility: int = Form(..., title="Versatility")
    ambition: int = Form(..., title="Ambition")
    loyalty: int = Form(..., title="Loyalty")
    pressure: int = Form(..., title="Pressure")
    professional: int = Form(..., title="Professional")
    acceleration: int = Form(..., title="Acceleration")
    agility: int = Form(..., title="Agility")
    balance: int = Form(..., title="Balance")
    jumping: int = Form(..., title="Jumping")
    natural_fitness: int = Form(..., title="Natural Fitness")
    pace: int = Form(..., title="Pace")
    stamina: int = Form(..., title="Stamina")
    strength: int = Form(..., title="Strength")
    adaptability: int = Form(..., title="Adaptability")


class PlayerUpdate(PlayerCreate):
    """PlayerUpdate schéma.

    Args:
        PlayerCreate (PlayerCreate): modèle PlayerCreate.
    """

    pass


class FileCID(BaseModel):
    """FileCID schéma.

    Args:
        BaseModel (BaseModel): modèle pydantic.
    """

    code: Optional[int]
    cid: Optional[str]


class ResponseCarApi(BaseModel):
    """ResponseCarApi schéma.

    Args:
        BaseModel (BaseModel): modèle pydantic.
    """

    status: int
    output: Optional[str]
    cid: Optional[str]
    error: Optional[str]
    files: Optional[List[FileCID]]
