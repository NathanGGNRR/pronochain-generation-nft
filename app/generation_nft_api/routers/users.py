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

File: app/generation_nft_api/routers/users.py
"""
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.generation_nft_api.dependencies import (
    get_current_active_superuser,
    get_current_active_user,
    get_db,
)
from app.generation_nft_db.models import users as models_users
from app.generation_nft_db.repositories import users as crud
from app.generation_nft_db.schemas import users as schemas_users

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[schemas_users.UserOut])
def read_users(
    db: Session = Depends(get_db),
    current_user: models_users.User = Depends(get_current_active_superuser),
) -> List[schemas_users.UserOut]:
    """Route pour récupérer la liste des utilisateurs.

    Args:
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).
        current_user (models_users.User, optional): utilisateur connecté. Défaut à Depends(get_current_active_superuser).

    Returns:
        List[schemas_users.UserOut]: liste d'user.
    """
    return crud.get_users(db)


@router.get("/me", response_model=schemas_users.UserOut)
def read_user_me(
    db: Session = Depends(get_db),
    current_user: models_users.User = Depends(get_current_active_user),
) -> schemas_users.UserOut:
    """Route pour récupérer l'utilisateur connecté.

    Args:
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).
        current_user (models_users.User, optional): _description_. Defaults to Depends(get_current_active_user).

    Returns:
        schemas_users.UserOut: user.
    """
    return current_user


@router.get("/{user_id}", response_model=schemas_users.UserOut)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models_users.User = Depends(get_current_active_superuser),
) -> schemas_users.UserOut:
    """Route pour récupèrer un utilisateur.

    Args:
        user_id (int): id user.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).
        current_user (models_users.User, optional): _description_. Defaults to Depends(get_current_active_superuser).

    Returns:
        schemas_users.UserOut: user.
    """
    return crud.get_user(db, user_id=user_id)


@router.get("/login/{user_login}", response_model=schemas_users.UserOut)
def read_user_by_login(
    user_login: str,
    db: Session = Depends(get_db),
    current_user: models_users.User = Depends(get_current_active_superuser),
) -> schemas_users.UserOut:
    """Route pour récupérer un utilisateur avec son login.

    Args:
        user_login (str): login user.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).
        current_user (models_users.User, optional): _description_. Defaults to Depends(get_current_active_superuser).

    Returns:
        schemas_users.UserOut: user.
    """
    return crud.get_user(db, user_login=user_login)
