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

File: app/generation_nft_api/routers/generation.py
"""
import requests
from fastapi import APIRouter, Depends, HTTPException, Response
from requests import Session

from app import logger_api
from app.generation_nft.libraries.generation.generation import Generation
from app.generation_nft_api.dependencies import get_current_active_superuser, get_db
from app.generation_nft_db.models import users as models_users
from app.generation_nft_db.schemas.generation import CreateGeneration, ResponseIsAlive
from app.settings import settings

router = APIRouter(
    prefix="/generation",
    tags=["generation"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/generate",
    responses={200: {"content": {"image/png": {}}}},
    response_class=Response,
)
async def generate_nft(
    rating: float,
    get_picture: bool = False,
    current_user: models_users.User = Depends(get_current_active_superuser),
) -> Response:
    """Route pour générer aléatoirement un NFT.

    Args:
        rating (float): côte.
        get_picture (bool, optional): renvoyer une image. Défaut à False.
        current_user (models_users.User, optional): utilisateur connecté. Défaut à Depends(get_current_active_superuser).

    Raises:
        HTTPException: la génération aléatoire du NFT a échouée.

    Returns:
        Response: response.
    """
    generation = Generation(rating)
    try:
        nft = generation.generate_nft(get_picture=get_picture)
        if get_picture:
            return Response(content=nft, media_type="image/png")
        return Response(content=nft, media_type="application/text")
    except Exception as err:
        logger_api.error(str(err))
        raise HTTPException(status_code=404, detail=str(err))


@router.post(
    "/create", responses={200: {"content": {"image/png": {}}}}, response_class=Response
)
async def create_nft(
    nft_parts: CreateGeneration = Depends(),
    current_user: models_users.User = Depends(get_current_active_superuser),
) -> Response:
    """Route pour créer un NFT.

    Args:
        nft_parts (CreateGeneration, optional): parties du NFT. Défaut à Depends().
        current_user (models_users.User, optional): utilisateur connecté. Défaut à Depends(get_current_active_superuser).

    Raises:
        HTTPException: la création du NFT a échouée.

    Returns:
        Response: response.
    """
    generation = Generation()
    try:
        nft = generation.generate_nft(
            params=nft_parts, get_picture=nft_parts.get_picture
        )
        if nft_parts.get_picture:
            return Response(content=nft, media_type="image/png")
        return Response(content=nft, media_type="application/text")
    except Exception as err:
        logger_api.error(str(err))
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/is-alive", response_model=ResponseIsAlive)
async def is_alive(db: Session = Depends(get_db)) -> ResponseIsAlive:
    """Route pour vérifier l'état de l'API.

    Args:
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Returns:
        ResponseIsAlive: status code et nom du retour.
    """
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    response = requests.get(
        f"http://{settings.CAR_API_SERVER}/is-alive", headers=headers
    )
    car_api_response = ResponseIsAlive.parse_obj(response.json())
    is_active = db.is_active and car_api_response.is_active
    return ResponseIsAlive(
        status=200 if is_active else 400,
        is_active=db.is_active and car_api_response.is_active,
    )
