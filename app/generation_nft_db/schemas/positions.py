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

File: app/generation_nft_db/schemas/positions.py
"""
from pydantic import BaseModel, constr

from app.generation_nft_db.schemas.nft_parts import ElementOut


class Position(BaseModel):
    """Position schéma.

    Args:
        BaseModel (BaseModel): modèle pydantic.
    """

    code: int
    abbreviation: constr(max_length=10)
    value: constr(max_length=255)


class PositionType(BaseModel):
    """PositionType schéma.

    Args:
        BaseModel (BaseModel): modèle pydantic.
    """

    code: int
    abbreviation: constr(max_length=10)
    value: constr(max_length=255)


class PositionOut(Position):
    """PositionOut schéma.

    Args:
        Position (Position): modèle Position.
    """

    id: int

    class Config:
        """Classe config d'un modèle pydantic."""

        orm_mode = True


class PositionTypeOut(PositionType):
    """PositionTypeOut schéma.

    Args:
        PositionType (PositionType): modèle PositionType.
    """

    id: int

    class Config:
        """Classe config d'un modèle pydantic."""

        orm_mode = True


class PositionNestedOut(PositionOut):
    """PositionNestedOut schéma.

    Args:
        PositionOut (PositionOut): modèle PositionOut.
    """

    type: PositionTypeOut


class PositionTypeNestedOut(PositionTypeOut):
    """PositionTypeNestedOut schéma.

    Args:
        PositionTypeOut (PositionTypeOut): modèle PositionTypeOut.
    """

    element: ElementOut


class PositionCreate(Position):
    """PositionCreate schéma.

    Args:
        Position (Position): modèle Position.
    """

    type_id: int


class PositionTypeCreate(PositionType):
    """PositionTypeCreate schéma.

    Args:
        PositionType (PositionType): modèle PositionType.
    """

    element_id: int


class PositionUpdate(PositionCreate):
    """PositionUpdate schéma.

    Args:
        PositionCreate (PositionCreate): modèle PositionCreate.
    """

    pass


class PositionTypeUpdate(PositionType):
    """PositionTypeUpdate schéma.

    Args:
        PositionType (PositionType): modèle PositionType.
    """

    pass
