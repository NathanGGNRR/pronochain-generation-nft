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

File: app/generation_nft_db/schemas/names.py
"""
from pydantic import BaseModel, constr


class Name(BaseModel):
    """Name schéma.

    Args:
        BaseModel (BaseModel): modèle pydantic.
    """

    value: constr(max_length=255)


class NameType(BaseModel):
    """NameType schéma.

    Args:
        BaseModel (BaseModel): modèle pydantic.
    """

    code: int
    value: constr(max_length=100)


class NameOut(Name):
    """NameOut schéma.

    Args:
        Name (Name): modèle Name.
    """

    id: int

    class Config:
        """Classe config d'un modèle pydantic."""

        orm_mode = True


class NameTypeOut(NameType):
    """NameTypeOut schéma.

    Args:
        NameType (NameType): modèle NameType.
    """

    id: int

    class Config:
        """Classe config d'un modèle pydantic."""

        orm_mode = True


class NameNestedOut(NameOut):
    """NameNestedOut schéma.

    Args:
        NameOut (NameOut): modèle NameOut.
    """

    type: NameTypeOut


class NameCreate(Name):
    """NameCreate schéma.

    Args:
        Name (Name): modèle Name.
    """

    type_id: int


class NameUpdate(NameCreate):
    """NameUpdate schéma.

    Args:
        NameCreate (NameCreate): modèle NameCreate.
    """

    pass


class NameTypeCreate(NameType):
    """NameTypeCreate schéma.

    Args:
        NameType (NameType): modèle NameType.
    """

    pass


class NameTypeUpdate(NameType):
    """NameTypeUpdate schéma.

    Args:
        NameType (NameType): modèle NameType.
    """

    pass
