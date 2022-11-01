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

File: app/generation_nft_db/schemas/stats.py
"""
from typing import List

from pydantic import BaseModel, constr

from app.generation_nft_db.schemas.positions import PositionOut


class Stat(BaseModel):
    """Stat schéma.

    Args:
        BaseModel (BaseModel): modèle pydantic.
    """

    code: int
    value: constr(max_length=255)


class StatType(BaseModel):
    """StatType schéma.

    Args:
        BaseModel (BaseModel): modèle pydantic.
    """

    code: int
    value: constr(max_length=255)


class StatOut(Stat):
    """StatOut schéma.

    Args:
        Stat (Stat): modèle Stat.
    """

    id: int

    class Config:
        """Classe config d'un modèle pydantic."""

        orm_mode = True


class StatTypeOut(StatType):
    """StatTypeOut schéma.

    Args:
        StatType (StatType): modèle StatType.
    """

    id: int

    class Config:
        """Classe config d'un modèle pydantic."""

        orm_mode = True


class StatNestedOut(StatOut):
    """StatNestedOut schéma.

    Args:
        StatOut (StatOut): modèle StatOut.
    """

    types: List[StatTypeOut]
    positions: List[PositionOut]


class StatCreate(Stat):
    """StatCreate schéma.

    Args:
        Stat (Stat): modèle Stat.
    """

    type_ids: List[int]
    position_ids: List[int]


class StatTypeCreate(StatType):
    """StatTypeCreate schéma.

    Args:
        StatType (StatType): modèle StatType.
    """

    pass


class StatUpdate(StatCreate):
    """StatUpdate schéma.

    Args:
        StatCreate (StatCreate): modèle StatCreate.
    """

    pass


class StatTypeUpdate(StatType):
    """StatTypeUpdate schéma.

    Args:
        StatType (StatType): modèle StatType.
    """

    pass
