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

File: app/generation_nft_api/routers/rarities.py
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.generation_nft_api.dependencies import get_current_active_superuser, get_db
from app.generation_nft_db.repositories import rarities as crud
from app.generation_nft_db.schemas.rarities import RarityCreate, RarityOut, RarityUpdate
from app.settings import settings

router = APIRouter(
    prefix="/rarities",
    tags=["rarities"],
    responses={404: {"description": "Not found"}},
    dependencies=[]
    if settings.AUTH_DISABLED
    else [Depends(get_current_active_superuser)],
)


@router.get("/", response_model=List[RarityOut])
async def read_rarities(db: Session = Depends(get_db)) -> List[RarityOut]:
    """Route pour récupérer une liste de raretés.

    Args:
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Returns:
        List[RarityOut]: liste de raretés.
    """
    return crud.get_rarities(db)


@router.get("/{rarity_id}", response_model=RarityOut)
async def read_rarity(rarity_id: int, db: Session = Depends(get_db)) -> RarityOut:
    """Route pour récupérer une rareté.

    Args:
        rarity_id (int): id rarity.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: la rareté n'existe pas.

    Returns:
        RarityOut: rarity.
    """
    db_rarity = crud.get_rarity(db, rarity_id=rarity_id)
    if db_rarity is None:
        raise HTTPException(status_code=404, detail="Rarity not found")
    return db_rarity


@router.get("/code/{rarity_code}", response_model=RarityOut)
async def read_rarity_code(
    rarity_code: int, db: Session = Depends(get_db)
) -> RarityOut:
    """Route pour récupérer une rareté par code.

    Args:
        rarity_code (int): code rarity.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: la rareté n'existe pas.

    Returns:
        RarityOut: rarity
    """
    db_rarity_code = crud.get_rarity_by_code(db, rarity_code=rarity_code)
    if db_rarity_code is None:
        raise HTTPException(status_code=404, detail="Rarity not found")
    return db_rarity_code


@router.post("/", response_model=RarityOut)
def create_rarity(rarity: RarityCreate, db: Session = Depends(get_db)) -> RarityOut:
    """Route pour crée une rareté.

    Args:
        rarity (RarityCreate): rarity.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: la rareté n'a pas été crée.

    Returns:
        RarityOut: rarity.
    """
    try:
        return crud.create_rarity(db=db, rarity=rarity)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{rarity_id}", response_model=RarityOut)
def update_rarity(
    rarity_id: int, rarity: RarityUpdate, db: Session = Depends(get_db)
) -> RarityOut:
    """Route pour mettre à jour une rareté.

    Args:
        rarity_id (int): id rarity.
        rarity (RarityUpdate): rarity.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: la rareté n'a pas été mise à jour.

    Returns:
        RarityOut: rarity
    """
    try:
        return crud.update_rarity(db=db, rarity_id=rarity_id, rarity=rarity)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{rarity_id}")
def delete_rarity(rarity_id: int, db: Session = Depends(get_db)) -> Response:
    """Route pour supprimer une rareté.

    Args:
        rarity_id (int): id rarity
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: la rareté n'a pas été supprimée.

    Returns:
        Response: response.
    """
    try:
        crud.delete_rarity(db=db, rarity_id=rarity_id)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/code/{rarity_code}")
def delete_rarity_code(rarity_code: int, db: Session = Depends(get_db)) -> Response:
    """Route pour supprimer une rareté par code.

    Args:
        rarity_code (int): code rarity.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: la rareté n'a pas été supprimée.

    Returns:
        Response: response.
    """
    try:
        crud.delete_rarity_by_code(db=db, rarity_code=rarity_code)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
