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

File: app/generation_nft_api/routers/positions.py
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.generation_nft_api.dependencies import get_current_active_superuser, get_db
from app.generation_nft_db.repositories import positions as crud
from app.generation_nft_db.schemas.positions import (
    PositionCreate,
    PositionNestedOut,
    PositionOut,
    PositionTypeCreate,
    PositionTypeNestedOut,
    PositionTypeUpdate,
    PositionUpdate,
)
from app.settings import settings

router = APIRouter(
    prefix="/positions",
    tags=["positions"],
    responses={404: {"description": "Not found"}},
    dependencies=[]
    if settings.AUTH_DISABLED
    else [Depends(get_current_active_superuser)],
)

position_type_not_found = "Position type not found"


@router.get("/", response_model=List[PositionNestedOut])
async def read_positions(db: Session = Depends(get_db)) -> List[PositionNestedOut]:
    """Route pour récupérer une liste de positions.

    Args:
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Returns:
        List[PositionNestedOut]: liste de position.
    """
    return crud.get_positions(db)


@router.get("/position-types", response_model=List[PositionTypeNestedOut])
async def read_position_types(
    db: Session = Depends(get_db),
) -> List[PositionTypeNestedOut]:
    """Route pour récupérer une liste de type de position.

    Args:
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Returns:
        List[PositionTypeNestedOut]: liste de position type.
    """
    return crud.get_position_types(db)


@router.get("/{position_id}", response_model=PositionNestedOut)
async def read_position(
    position_id: int, db: Session = Depends(get_db)
) -> PositionNestedOut:
    """Route pour récupérer une position.

    Args:
        position_id (int): id position.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: la position n'existe pas.

    Returns:
        PositionNestedOut: position.
    """
    db_position = crud.get_position(db, position_id=position_id)
    if db_position is None:
        raise HTTPException(status_code=404, detail="Position not found")
    return db_position


@router.get("/code/{position_code}", response_model=PositionNestedOut)
async def read_position_code(
    position_code: int, db: Session = Depends(get_db)
) -> PositionNestedOut:
    """Route pour récupérer une position par code.

    Args:
        position_code (int): code position.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: la position n'existe pas.

    Returns:
        PositionNestedOut: position.
    """
    db_position_code = crud.get_position_by_code(db, position_code=position_code)
    if db_position_code is None:
        raise HTTPException(status_code=404, detail="Position not found")
    return db_position_code


@router.get("/position-type/{position_type_id}", response_model=PositionTypeNestedOut)
async def read_position_type(
    position_type_id: int, db: Session = Depends(get_db)
) -> PositionTypeNestedOut:
    """Route pour récupérer un type de position.

    Args:
        position_type_id (int): id position type.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le type de position n'existe pas.

    Returns:
        PositionTypeNestedOut: position type.
    """
    db_position_type = crud.get_position_type(db, position_type_id=position_type_id)
    if db_position_type is None:
        raise HTTPException(status_code=404, detail=position_type_not_found)
    return db_position_type


@router.get(
    "/position-type/code/{position_type_code}", response_model=PositionTypeNestedOut
)
async def read_position_type_code(
    position_type_code: int, db: Session = Depends(get_db)
) -> PositionTypeNestedOut:
    """Route pour récupérer un type de position par code.

    Args:
        position_type_code (int): code position type.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le type de position n'existe pas.

    Returns:
        PositionTypeNestedOut: position type.
    """
    db_position_type_code = crud.get_position_type_by_code(
        db, position_type_code=position_type_code
    )
    if db_position_type_code is None:
        raise HTTPException(status_code=404, detail=position_type_not_found)
    return db_position_type_code


@router.get("/type/{position_type_id}", response_model=List[PositionOut])
async def read_positions_by_type(
    position_type_id: int, db: Session = Depends(get_db)
) -> List[PositionOut]:
    """Route pour récupérer une liste de position par type.

    Args:
        position_type_id (int): id position type.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le type de position n'existe pas.

    Returns:
        List[PositionOut]: liste de position.
    """
    try:
        return crud.get_positions_by_type(db, position_type_id=position_type_id)
    except AttributeError:
        raise HTTPException(status_code=404, detail=position_type_not_found)


@router.get("/type/code/{position_type_code}", response_model=List[PositionOut])
async def read_positions_by_type_code(
    position_type_code: int, db: Session = Depends(get_db)
) -> List[PositionOut]:
    """Route pour récupérer une liste de position par type par code.

    Args:
        position_type_code (int): code position type.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: e type de position n'existe pas.

    Returns:
        List[PositionOut]: liste de position.
    """
    try:
        return crud.get_positions_by_type_code(
            db, position_type_code=position_type_code
        )
    except AttributeError:
        raise HTTPException(status_code=404, detail=position_type_not_found)


@router.post("/", response_model=PositionNestedOut)
def create_position(
    position: PositionCreate, db: Session = Depends(get_db)
) -> PositionNestedOut:
    """Route pour crée une position.

    Args:
        position (PositionCreate): position
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: la position n'a pas été crée.

    Returns:
        PositionNestedOut: position.
    """
    try:
        return crud.create_position(db=db, position=position)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/position-types", response_model=PositionTypeNestedOut)
def create_position_types(
    position_types: PositionTypeCreate, db: Session = Depends(get_db)
) -> PositionTypeNestedOut:
    """Route pour crée un type de position.

    Args:
        position_types (PositionTypeCreate): position type.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le type de position n'a pas été crée.

    Returns:
        PositionTypeNestedOut: position type.
    """
    try:
        return crud.create_position_type(db=db, position_type=position_types)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{position_id}", response_model=PositionNestedOut)
def update_position(
    position_id: int, position: PositionUpdate, db: Session = Depends(get_db)
) -> PositionNestedOut:
    """Route pour mettre à jour une position.

    Args:
        position_id (int): id position.
        position (PositionUpdate): position.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: la position n'a pas été mise à jour.

    Returns:
        PositionNestedOut: position.
    """
    try:
        return crud.update_position(db=db, position_id=position_id, position=position)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/position-types/{position_type_id}", response_model=PositionTypeNestedOut)
def update_position_type(
    position_type_id: int,
    position_type: PositionTypeUpdate,
    db: Session = Depends(get_db),
) -> PositionTypeNestedOut:
    """Route pour mettre à jour un type de position.

    Args:
        position_type_id (int): id position type.
        position_type (PositionTypeUpdate): position type.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le type de position n'a pas été mis à jour.

    Returns:
        PositionTypeNestedOut: position type.
    """
    try:
        return crud.update_position_type(
            db=db, position_type_id=position_type_id, position_type=position_type
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{position_id}")
def delete_position(position_id: int, db: Session = Depends(get_db)) -> Response:
    """Route pour supprimer une position.

    Args:
        position_id (int): id position.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: la position n'a pas été supprimée.

    Returns:
        Response: response.
    """
    try:
        crud.delete_position(db=db, position_id=position_id)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/code/{position_code}")
def delete_position_code(position_code: int, db: Session = Depends(get_db)) -> Response:
    """Route pour supprimer une position par code.

    Args:
        position_code (int): code position.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: la position n'a pas été supprimée.

    Returns:
        Response: response.
    """
    try:
        crud.delete_position_by_code(db=db, position_code=position_code)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/position-types/{position_type_id}")
def delete_position_type(
    position_type_id: int, db: Session = Depends(get_db)
) -> Response:
    """Route pour supprimer un type de position.

    Args:
        position_type_id (int): id position type.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le type de position n'a pas été supprimé.

    Returns:
        Response: response.
    """
    try:
        crud.delete_position_type(db=db, position_type_id=position_type_id)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/position-types/code/{position_type_code}")
def delete_position_type_code(
    position_type_code: int, db: Session = Depends(get_db)
) -> Response:
    """Route pour supprimer un type de position par code.

    Args:
        position_type_code (int): code position type.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le type de position n'a pas été supprimé.

    Returns:
        Response: response.
    """
    try:
        crud.delete_position_type_by_code(db=db, position_type_code=position_type_code)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
