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

File: app/generation_nft_db/repositories/users.py
"""
from typing import List, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import PronochainException
from app.generation_nft_db.core.security import get_password_hash, verify_password
from app.generation_nft_db.models import users as model_users
from app.generation_nft_db.schemas import users as schemas_users


def get_user_by_token(db: Session, token_user_id: int) -> schemas_users.UserOut:
    """Récupérer un utilisateur grâce au token.

    Args:
        db (Session): session de la base de donnée.
        token_user_id (int): id du token utilisateur.

    Returns:
        schemas_users.UserOut: utilisateur.
    """
    return (
        db.query(model_users.User).filter(model_users.User.id == token_user_id).first()
    )


def get_user(db: Session, user_id: int) -> schemas_users.UserOut:
    """Récupére un utilisateur.

    Args:
        db (Session): session de la base de donnée.
        user_id (int): id utilisateur.

    Returns:
        schemas_users.UserOut: utilisateur.
    """
    return db.query(model_users.User).filter(model_users.User.id == user_id).first()


def get_user_by_login(db: Session, user_login: str) -> schemas_users.UserOut:
    """Récupère utilisateur avec son login.

    Args:
        db (Session): session de la base de donnée.
        user_login (str): login utilisateur.

    Returns:
        schemas_users.UserOut: utilisateur.
    """
    return (
        db.query(model_users.User).filter(model_users.User.login == user_login).first()
    )


def check_user(db: Session, login: str) -> schemas_users.UserInDB:
    """Vérifie si l'utilisateur existe avec un login.

    Args:
        db (Session): session de la base de donnée.
        login (str): login utilisateur.

    Returns:
        schemas_users.UserInDB: utilisateur.
    """
    return db.query(model_users.User).filter(model_users.User.login == login).first()


def get_users(db: Session) -> List[schemas_users.UserOut]:
    """Récupère une liste d'utilisateur.

    Args:
        db (Session): session de la base de donnée.

    Returns:
        List[schemas_users.UserOut]: liste d'utilisateur.
    """
    return db.query(model_users.User).all()


def authenticate(
    db: Session, login: str, password: str
) -> Optional[schemas_users.UserOut]:
    """Authentification d'un utilisateur.

    Args:
        db (Session): session de la base de donnée.
        login (str): login utilisateur.
        password (str): mot de passe utilisateur.

    Returns:
        Optional[schemas_users.UserOut]: utilisateur.
    """
    user = check_user(db, login=login)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def is_active(user: schemas_users.User) -> bool:
    """Vérifie si l'utilisateur est actif.

    Args:
        user (schemas_users.User): utilisateur.

    Returns:
        bool: est actif ?
    """
    return user.is_active


def is_superuser(user: schemas_users.User) -> bool:
    """Vérifie si l'utilisateur est un super utilisateur.

    Args:
        user (schemas_users.User): utilisateur.

    Returns:
        bool: est un super utilisateur ?
    """
    return user.is_superuser


def create_user(
    db: Session, user: schemas_users.UserCreate, commit: bool = True
) -> schemas_users.UserOut:
    """Crée un utilisateur.

    Args:
        db (Session): session de la base de donnée.
        user (schemas_users.UserCreate): utilisateur.
        commit (bool, optional): met à jour directement. Défaut à True.

    Raises:
        PronochainException: l'utilisateur n'a pas été crée.

    Returns:
        schemas_users.UserOut: utilisateur.
    """
    try:
        user_dict = user.dict()
        hashed_password = get_password_hash(user_dict.pop("password"))
        db_user = model_users.User(**user_dict, hashed_password=hashed_password)
        db.add(db_user)
        if commit:
            db.commit()
            db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])
