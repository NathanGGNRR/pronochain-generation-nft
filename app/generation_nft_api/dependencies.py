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

File: app/generation_nft_api/dependencies.py
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.generation_nft_db.database import SessionLocal
from app.generation_nft_db.models import User
from app.generation_nft_db.repositories.users import (
    get_user_by_token,
    is_active,
    is_superuser,
)
from app.generation_nft_db.schemas.tokens import TokenPayload
from app.settings import settings


def get_db() -> SessionLocal:
    """Récupère la session de la base de donnée.

    Returns:
        SessionLocal: session de la base de donnée.

    Yields:
        Iterator[SessionLocal]: session de la base de donnée.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/login/access-token",
)


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    """Récupère l'utilisateur connecté.

    Args:
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).
        token (str, optional): jwt token. Défaut à Depends(reusable_oauth2).

    Raises:
        HTTPException: impossible de valider l'authentification.
        HTTPException: l'utilisateur n'existe pas.

    Returns:
        User: user.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECURITY_SECRET_KEY,
            algorithms=[settings.SECURITY_ALGORITHM],
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = get_user_by_token(db, token_user_id=int(token_data.sub))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Récupère l'utilisateur actif connecté.

    Args:
        current_user (User, optional): utilisateur connecté. Défaut à Depends(get_current_user).

    Raises:
        HTTPException: utilisateur inactif.

    Returns:
        User: user.
    """
    if not is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """Récupère le super utilisateur actif connecté.

    Args:
        current_user (User, optional): utilisateur connecté. Défaut à Depends(get_current_user).

    Raises:
        HTTPException: l'utilisateur n'est pas super.

    Returns:
        User: user.
    """
    if not is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
