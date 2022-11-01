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

File: app/generation_nft_api/routers/stats.py
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.generation_nft_api.dependencies import get_current_active_superuser, get_db
from app.generation_nft_db.repositories import stats as crud
from app.generation_nft_db.schemas.stats import (
    StatCreate,
    StatNestedOut,
    StatOut,
    StatTypeCreate,
    StatTypeOut,
    StatTypeUpdate,
    StatUpdate,
)
from app.settings import settings

router = APIRouter(
    prefix="/stats",
    tags=["stats"],
    responses={404: {"description": "Not found"}},
    dependencies=[]
    if settings.AUTH_DISABLED
    else [Depends(get_current_active_superuser)],
)

stat_type_not_found = "Stat type not found"


@router.get("/", response_model=List[StatNestedOut])
async def read_stats(db: Session = Depends(get_db)) -> List[StatNestedOut]:
    """Route pour récupérer une liste de stat.

    Args:
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Returns:
        List[StatNestedOut]: liste de stat.
    """
    return crud.get_stats(db)


@router.get("/stat-types", response_model=List[StatTypeOut])
async def read_stat_types(db: Session = Depends(get_db)) -> List[StatTypeOut]:
    """Route pour récupérer une liste de type de stat.

    Args:
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Returns:
        List[StatTypeOut]: liste de type de stat.
    """
    return crud.get_stat_types(db)


@router.get("/{stat_id}", response_model=StatNestedOut)
async def read_stat(stat_id: int, db: Session = Depends(get_db)) -> StatNestedOut:
    """Route pour récupérer une stat.

    Args:
        stat_id (int): id stat.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: la stat n'existe pas.

    Returns:
        StatNestedOut: stat.
    """
    db_stat = crud.get_stat(db, stat_id=stat_id)
    if db_stat is None:
        raise HTTPException(status_code=404, detail="Stat not found")
    return db_stat


@router.get("/code/{stat_code}", response_model=StatNestedOut)
async def read_stat_by_code(
    stat_code: int, db: Session = Depends(get_db)
) -> StatNestedOut:
    """Route pour récupérer une stat par code.

    Args:
        stat_code (int): code stat.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: la stat n'existe pas.

    Returns:
        StatNestedOut: stat.
    """
    db_stat_code = crud.get_stat_by_code(db, stat_code=stat_code)
    if db_stat_code is None:
        raise HTTPException(status_code=404, detail="Stat not found")
    return db_stat_code


@router.get("/stat-type/{stat_type_id}", response_model=StatTypeOut)
async def read_stat_type(
    stat_type_id: int, db: Session = Depends(get_db)
) -> StatTypeOut:
    """Route pour récupérer un type de stat.

    Args:
        stat_type_id (int): id stat type.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le type de stat n'existe pas.

    Returns:
        StatTypeOut: stat type.
    """
    db_stat_type = crud.get_stat_type(db, stat_type_id=stat_type_id)
    if db_stat_type is None:
        raise HTTPException(status_code=404, detail=stat_type_not_found)
    return db_stat_type


@router.get("/stat-type/code/{stat_type_id}", response_model=StatTypeOut)
async def read_stat_type_code(
    stat_type_code: int, db: Session = Depends(get_db)
) -> StatTypeOut:
    """Route pour récupérer un type de stat par code.

    Args:
        stat_type_code (int): code stat type.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le type de stat n'existe pas.

    Returns:
        StatTypeOut: stat type.
    """
    db_stat_type_code = crud.get_stat_type_by_code(db, stat_type_code=stat_type_code)
    if db_stat_type_code is None:
        raise HTTPException(status_code=404, detail=stat_type_not_found)
    return db_stat_type_code


@router.get("/type/{stat_type_id}", response_model=List[StatOut])
async def read_stats_by_type(
    stat_type_id: int, db: Session = Depends(get_db)
) -> List[StatOut]:
    """Route pour récupérer une liste de stat par type.

    Args:
        stat_type_id (int): id stat type.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le type de stat n'existe pas.

    Returns:
        List[StatOut]: liste de stat.
    """
    try:
        return crud.get_stats_by_type(db, stat_type_id=stat_type_id)
    except AttributeError:
        raise HTTPException(status_code=404, detail=stat_type_not_found)


@router.get("/type/code/{stat_type_code}", response_model=List[StatOut])
async def read_stats_by_type_code(
    stat_type_code: int, db: Session = Depends(get_db)
) -> List[StatOut]:
    """Route pour récupérer une liste de stat par type par code.

    Args:
        stat_type_code (int): code stat type.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le type de stat n'existe pas.

    Returns:
        List[StatOut]: liste de stat.
    """
    try:
        return crud.get_stats_by_type_code(db, stat_type_code=stat_type_code)
    except AttributeError:
        raise HTTPException(status_code=404, detail=stat_type_not_found)


@router.post("/", response_model=StatNestedOut)
def create_stat(stat: StatCreate, db: Session = Depends(get_db)) -> StatNestedOut:
    """Route pour créer une stat.

    Args:
        stat (StatCreate): stat.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: la stat n'a pas été crée.

    Returns:
        StatNestedOut: stat.
    """
    try:
        return crud.create_stat(db=db, stat=stat)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/stat-types", response_model=StatTypeOut)
def create_stat_types(
    stat_type: StatTypeCreate, db: Session = Depends(get_db)
) -> StatTypeOut:
    """Route pour créer un type de stat.

    Args:
        stat_type (StatTypeCreate): stat type.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le type de stat n'a pas été crée.

    Returns:
        StatTypeOut: stat type.
    """
    try:
        return crud.create_stat_type(db=db, stat_type=stat_type)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{stat_id}", response_model=StatNestedOut)
def update_stat(
    stat_id: int, stat: StatUpdate, db: Session = Depends(get_db)
) -> StatNestedOut:
    """Route pour mettre à jour une stat.

    Args:
        stat_id (int): id stat.
        stat (StatUpdate): stat.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: la stat n'a pas été mise à jour.

    Returns:
        StatNestedOut: stat.
    """
    try:
        return crud.update_stat(db=db, stat_id=stat_id, stat=stat)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/stat-types/{stat_type_id}", response_model=StatTypeOut)
def update_stat_type(
    stat_type_id: int, stat_type: StatTypeUpdate, db: Session = Depends(get_db)
) -> StatTypeOut:
    """Route pour mettre à jour le type de stat.

    Args:
        stat_type_id (int): id stat type.
        stat_type (StatTypeUpdate): stat type.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le type de stat n'a pas été mise à jour.

    Returns:
        StatTypeOut: stat type.
    """
    try:
        return crud.update_stat_type(
            db=db, stat_type_id=stat_type_id, stat_type=stat_type
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{stat_id}")
def delete_stat(stat_id: int, db: Session = Depends(get_db)) -> Response:
    """Route pour supprimer une stat.

    Args:
        stat_id (int): id stat.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: la stat n'a pas été supprimée.

    Returns:
        Response: response.
    """
    try:
        crud.delete_stat(db=db, stat_id=stat_id)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/code/{stat_code}")
def delete_stat_code(stat_code: int, db: Session = Depends(get_db)) -> Response:
    """Route pour supprimer une stat par code.

    Args:
        stat_code (int): code stat.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: la stat n'a pas été supprimée.

    Returns:
        Response: response.
    """
    try:
        crud.delete_stat_by_code(db=db, stat_code=stat_code)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/stat-types/{stat_type_id}")
def delete_stat_type(stat_type_id: int, db: Session = Depends(get_db)) -> Response:
    """Route pour supprimer un type de stat.

    Args:
        stat_type_id (int): id stat type.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le type de stat n'a pas été supprimé.

    Returns:
        Response: response.
    """
    try:
        crud.delete_stat_type(db=db, stat_type_id=stat_type_id)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/stat-types/code/{stat_type_code}")
def delete_stat_type_code(
    stat_type_code: int, db: Session = Depends(get_db)
) -> Response:
    """Route pour supprimer un type de stat par code.

    Args:
        stat_type_code (int): code stat type.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le type de stat n'a pas été supprimé.

    Returns:
        Response: response.
    """
    try:
        crud.delete_stat_type_by_code(db=db, stat_type_code=stat_type_code)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
