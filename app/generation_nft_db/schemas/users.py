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

File: app/generation_nft_db/schemas/users.py
"""
from typing import Optional

from pydantic import BaseModel, constr


class User(BaseModel):
    """User schéma.

    Args:
        BaseModel (BaseModel): modèle pydantic.
    """

    login: constr(max_length=255)
    is_active: Optional[bool] = True
    is_superuser: bool = False


class UserOut(User):
    """UserOut schéma.

    Args:
        User (User): modèle User.
    """

    id: int

    class Config:
        """Classe config d'un modèle pydantic."""

        orm_mode = True


class UserCreate(User):
    """UserCreate schéma.

    Args:
        User (User): modèle User.
    """

    password: str


class UserInDB(UserOut):
    """UserInDB schéma.

    Args:
        UserOut (UserOut): modèle UserOut.
    """

    hashed_password: str
