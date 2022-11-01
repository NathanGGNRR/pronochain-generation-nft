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

File: app/generation_nft_api/routers/divisions.py
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.generation_nft_api.dependencies import get_current_active_superuser, get_db
from app.generation_nft_db.repositories import divisions as crud
from app.generation_nft_db.schemas.divisions import (
    DivisionCreate,
    DivisionNestedOut,
    DivisionOut,
    DivisionUpdate,
)
from app.settings import settings

router = APIRouter(
    prefix="/divisions",
    tags=["divisions"],
    responses={404: {"description": "Not found"}},
    dependencies=[]
    if settings.AUTH_DISABLED
    else [Depends(get_current_active_superuser)],
)


@router.get("/", response_model=List[DivisionNestedOut])
async def read_divisions(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[DivisionNestedOut]:
    """Route pour récupérer une liste de divisions.

    Args:
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Returns:
        List[DivisionNestedOut]: liste de division.
    """
    return crud.get_divisions(db, skip=skip, limit=limit)


@router.get("/{division_id}", response_model=DivisionNestedOut)
async def read_division(
    division_id: int, db: Session = Depends(get_db)
) -> DivisionNestedOut:
    """Route pour récupérer une division.

    Args:
        division_id (int): id division.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: la division n'existe pas.

    Returns:
        DivisionNestedOut: division.
    """
    db_division = crud.get_division(db, division_id=division_id)
    if db_division is None:
        raise HTTPException(status_code=404, detail="Division not found")
    return db_division


@router.get("/code/{division_code}", response_model=DivisionNestedOut)
async def read_division_code(
    division_code: int, db: Session = Depends(get_db)
) -> DivisionNestedOut:
    """Route pour récupérer une division par code.

    Args:
        division_code (int): code division.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: la division n'existe pas.

    Returns:
        DivisionNestedOut: division.
    """
    db_division_code = crud.get_division_by_code(db, division_code=division_code)
    if db_division_code is None:
        raise HTTPException(status_code=404, detail="Division not found")
    return db_division_code


@router.get("/country/{country_id}", response_model=List[DivisionOut])
async def read_divisions_by_country(
    country_id: int, db: Session = Depends(get_db)
) -> List[DivisionOut]:
    """Route pour récupérer une liste de division par pays.

    Args:
        country_id (int): id country.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le pays n'existe pas.

    Returns:
        List[DivisionOut]: liste de division.
    """
    try:
        return crud.get_divisions_by_country(db, country_id=country_id)
    except AttributeError:
        raise HTTPException(status_code=404, detail="Country not found")


@router.get("/country/code/{country_code}", response_model=List[DivisionOut])
async def read_division_by_country_code(
    country_code: str, db: Session = Depends(get_db)
) -> List[DivisionOut]:
    """Route pour récupérer une liste de division par pays par code.

    Args:
        country_code (str): code country.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le pays n'existe pas.

    Returns:
        List[DivisionOut]: liste de division.
    """
    try:
        return crud.get_divisions_by_country_code(db, country_code=country_code)
    except AttributeError:
        raise HTTPException(status_code=404, detail="Country not found")


@router.post("/", response_model=DivisionNestedOut)
def create_division(
    division: DivisionCreate, db: Session = Depends(get_db)
) -> DivisionNestedOut:
    """Route pour créer une division.

    Args:
        division (DivisionCreate): division.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: la division n'a pas été crée.

    Returns:
        DivisionNestedOut: division.
    """
    try:
        return crud.create_division(db=db, division=division)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{division_id}", response_model=DivisionNestedOut)
def update_division(
    division_id: int, division: DivisionUpdate, db: Session = Depends(get_db)
) -> DivisionNestedOut:
    """Route pour mettre à jour une division.

    Args:
        division_id (int): id division.
        division (DivisionUpdate): division.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: la division n'a pas été mise à jour.

    Returns:
        DivisionNestedOut: division.
    """
    try:
        return crud.update_division(db=db, division_id=division_id, division=division)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{division_id}")
def delete_division(division_id: int, db: Session = Depends(get_db)) -> Response:
    """Route pour supprimer une divsion.

    Args:
        division_id (int): id division.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: la division n'a pas été supprimée.

    Returns:
        Response: response.
    """
    try:
        crud.delete_division(db=db, division_id=division_id)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/code/{division_code}")
def delete_division_code(division_code: int, db: Session = Depends(get_db)) -> Response:
    """Route pour supprimer une divsion par code.

    Args:
        division_code (int): code division.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: la division n'a pas été supprimée.

    Returns:
        Response: response.
    """
    try:
        crud.delete_division_by_code(db=db, division_code=division_code)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
