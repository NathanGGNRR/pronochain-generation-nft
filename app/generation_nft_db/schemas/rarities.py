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

File: app/generation_nft_db/schemas/rarities.py
"""
from pydantic import BaseModel, constr


class Rarity(BaseModel):
    """Rarity schéma.

    Args:
        BaseModel (BaseModel): modèle pydantic.
    """

    code: int
    name: constr(max_length=255)
    percentage: float


class RarityOut(Rarity):
    """RarityOut schéma.

    Args:
        Rarity (Rarity): modèle Rarity.
    """

    id: int

    class Config:
        """Classe config d'un modèle pydantic."""

        orm_mode = True


class RarityCreate(Rarity):
    """RarityCreate schéma.

    Args:
        Rarity (Rarity): modèle Rarity.
    """

    pass


class RarityUpdate(Rarity):
    """RarityUpdate schéma.

    Args:
        Rarity (Rarity): modèle Rarity.
    """

    pass
