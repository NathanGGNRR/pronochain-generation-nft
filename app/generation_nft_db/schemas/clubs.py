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

File: app/generation_nft_db/schemas/clubs.py
"""
from typing import Optional

from pydantic import BaseModel, constr

from app.generation_nft_db.schemas.countries import CountryOut
from app.generation_nft_db.schemas.divisions import DivisionOut
from app.generation_nft_db.schemas.nft_parts import ColorOut


class Club(BaseModel):
    """Club schéma.

    Args:
        BaseModel (BaseModel): modèle pydantic.
    """

    code: int
    name: constr(max_length=255)


class ClubOut(Club):
    """ClubOut schéma.

    Args:
        Club (Club): modèle Club.
    """

    id: int

    class Config:
        """Classe config d'un modèle pydantic."""

        orm_mode = True


class ClubNestedOut(ClubOut):
    """ClubNestedOut schéma.

    Args:
        ClubOut (ClubOut): modèle ClubOut.
    """

    country: CountryOut
    division: DivisionOut
    first_color: ColorOut
    second_color: ColorOut


class ClubCreate(Club):
    """ClubCreate schéma.

    Args:
        Club (Club): modèle Club.
    """

    country_id: Optional[int]
    division_id: Optional[int]
    first_color_id: Optional[int]
    second_color_id: Optional[int]


class ClubUpdate(ClubCreate):
    """ClubUpdate schéma.

    Args:
        ClubCreate (ClubCreate): modèle ClubCreate.
    """

    pass
