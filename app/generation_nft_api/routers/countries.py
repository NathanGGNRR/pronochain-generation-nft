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

File: app/generation_nft_api/routers/countries.py
"""
from typing import List

from fastapi import APIRouter, Depends, File, Form, HTTPException, Response, UploadFile
from sqlalchemy.orm import Session

from app.generation_nft_api.dependencies import get_current_active_superuser, get_db
from app.generation_nft_db.repositories import countries as crud
from app.generation_nft_db.schemas.countries import CountryOut
from app.settings import settings

router = APIRouter(
    prefix="/countries",
    tags=["countries"],
    responses={404: {"description": "Not found"}},
    dependencies=[]
    if settings.AUTH_DISABLED
    else [Depends(get_current_active_superuser)],
)


@router.get("/", response_model=List[CountryOut])
async def read_countries(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[CountryOut]:
    """Route pour récupérer une liste de pays.

    Args:
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Returns:
        List[CountryOut]: liste de country.
    """
    return crud.get_countries(db, skip=skip, limit=limit)


@router.get("/{country_id}", response_model=CountryOut)
async def read_country(country_id: int, db: Session = Depends(get_db)) -> CountryOut:
    """Route pour récupérer un pays.

    Args:
        country_id (int): id country.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le pays n'existe pas.

    Returns:
        CountryOut: country.
    """
    db_country = crud.get_country(db, country_id=country_id)
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return db_country


@router.get("/code/{country_code}", response_model=CountryOut)
async def read_country_by_code(
    country_code: str, db: Session = Depends(get_db)
) -> CountryOut:
    """Route pour récupérer un pays par code.

    Args:
        country_code (str): code country.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le pays n'existe pas.

    Returns:
        CountryOut: country.
    """
    db_country_code = crud.get_country_by_code(db, country_code=country_code)
    if db_country_code is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return db_country_code


@router.post("/", response_model=CountryOut)
def create_country(
    code: str = Form(...),
    value: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> CountryOut:
    """Route pour créer un pays.

    Args:
        code (str, optional): code du pays. Défaut à Form(...).
        value (str, optional): nom du pays. Défaut à Form(...).
        file (UploadFile, optional): drapeau du pays. Défaut à File(...).
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le pays n'a pas été crée.

    Returns:
        CountryOut: country.
    """
    try:
        return crud.create_country(db=db, code=code, value=value, file=file)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{country_id}", response_model=CountryOut)
def update_country(
    country_id: int,
    code: str = Form(...),
    value: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> CountryOut:
    """Route pour mettre à jour un pays.

    Args:
        country_id (int): id country.
        code (str, optional): code du pays. Défaut à Form(...).
        value (str, optional): nom du pays. Défaut à Form(...).
        file (UploadFile, optional): drapeau du pays. Défaut à File(...).
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le pays n'a pas été mis à jour.

    Returns:
        CountryOut: country.
    """
    try:
        return crud.update_country(
            db=db, country_id=country_id, code=code, value=value, file=file
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{country_id}")
def delete_country(country_id: int, db: Session = Depends(get_db)) -> Response:
    """Route pour supprimer un pays.

    Args:
        country_id (int): id country.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le pays n'a pas été supprimé.

    Returns:
        Response: response.
    """
    try:
        crud.delete_country(db=db, country_id=country_id)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/code/{country_code}")
def delete_country_code(country_code: str, db: Session = Depends(get_db)) -> Response:
    """Route pour supprimer un pays par code.

    Args:
        country_code (str): code country.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le pays n'a pas été supprimé.

    Returns:
        Response: response.
    """
    try:
        crud.delete_country_by_code(db=db, country_code=country_code)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
