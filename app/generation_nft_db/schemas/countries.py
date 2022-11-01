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

File: app/generation_nft_db/schemas/countries.py
"""
from typing import Optional

from pydantic import BaseModel, constr


class Country(BaseModel):
    """Country schéma.

    Args:
        BaseModel (BaseModel): modèle pydantic.
    """

    code: constr(max_length=2)
    value: constr(max_length=255)


class CountryOut(Country):
    """CountryOut schéma.

    Args:
        Country (Country): modèle Country.
    """

    id: int
    cid: Optional[str]
    filename: Optional[str]

    class Config:
        """Classe config d'un modèle pydantic."""

        orm_mode = True


class CountryCreate(Country):
    """CountryCreate schéma.

    Args:
        Country (Country): modèle Country.
    """

    pass


class CountryUpdate(Country):
    """CountryUpdate schéma.

    Args:
        Country (Country): modèle Country.
    """

    pass
