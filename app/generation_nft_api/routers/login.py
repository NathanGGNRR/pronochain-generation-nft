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
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.generation_nft_api.dependencies import get_current_user, get_db
from app.generation_nft_db.core.security import create_access_token
from app.generation_nft_db.models.users import User
from app.generation_nft_db.repositories.users import authenticate, is_active
from app.generation_nft_db.schemas.tokens import Token
from app.generation_nft_db.schemas.users import UserOut
from app.settings import settings

router = APIRouter(tags=["login"], responses={404: {"description": "Not found"}})


@router.post("/login/access-token", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> dict:
    """Route pour se connecter.

    Args:
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).
        form_data (OAuth2PasswordRequestForm, optional): formulaire de connexion. Défaut à Depends().

    Raises:
        HTTPException: login ou mot de passe incorrect.
        HTTPException: l'utilisateur est inactive.

    Returns:
        dict: token.
    """
    user = authenticate(db, login=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect login or password")
    elif not is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login/test-token", response_model=UserOut)
def test_token(current_user: User = Depends(get_current_user)) -> UserOut:
    """Route pour tester la validité le token.

    Args:
        current_user (User, optional): utilisateur actif. Défaut à Depends(get_current_user).

    Returns:
        UserOut: user.
    """
    return current_user
