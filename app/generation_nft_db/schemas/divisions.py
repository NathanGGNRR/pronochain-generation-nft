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

File: app/generation_nft_db/schemas/divisions.py
"""
from pydantic import BaseModel, constr

from app.generation_nft_db.schemas.countries import CountryOut


class Division(BaseModel):
    """Division schéma.

    Args:
        BaseModel (BaseModel): modèle pydantic.
    """

    code: int
    name: constr(max_length=255)


class DivisionOut(Division):
    """DivisionOut schéma.

    Args:
        Division (Division): modèle Division.
    """

    id: int

    class Config:
        """Classe config d'un modèle pydantic."""

        orm_mode = True


class DivisionNestedOut(DivisionOut):
    """DivisionNestedOut schéma.

    Args:
        DivisionOut (DivisionOut): modèle DivisionOut.
    """

    country: CountryOut


class DivisionCreate(Division):
    """DivisionCreate schéma.

    Args:
        Division (Division): modèle Division.
    """

    country_id: int


class DivisionUpdate(Division):
    """DivisionUpdate schéma.

    Args:
        Division (Division): modèle Division.
    """

    pass
