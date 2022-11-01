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

File: app/generation_nft_api/routers/names.py
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.generation_nft_api.dependencies import get_current_active_superuser, get_db
from app.generation_nft_db.repositories import names as crud
from app.generation_nft_db.schemas.names import (
    NameCreate,
    NameNestedOut,
    NameOut,
    NameTypeCreate,
    NameTypeOut,
    NameTypeUpdate,
    NameUpdate,
)
from app.settings import settings

router = APIRouter(
    prefix="/names",
    tags=["names"],
    responses={404: {"description": "Not found"}},
    dependencies=[]
    if settings.AUTH_DISABLED
    else [Depends(get_current_active_superuser)],
)

name_type_not_found = "Name type not found"


@router.get("/", response_model=List[NameNestedOut])
async def read_names(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[NameNestedOut]:
    """Route pour récupérer une liste de noms.

    Args:
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Returns:
        List[NameNestedOut]: liste de name.
    """
    return crud.get_names(db, skip=skip, limit=limit)


@router.get("/name-types", response_model=List[NameTypeOut])
async def read_name_types(db: Session = Depends(get_db)) -> List[NameTypeOut]:
    """Route pour récupérer une liste de type de nom.

    Args:
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Returns:
        List[NameTypeOut]: liste de name type.
    """
    return crud.get_name_types(db)


@router.get("/{name_id}", response_model=NameNestedOut)
async def read_name(name_id: int, db: Session = Depends(get_db)) -> NameNestedOut:
    """Route pour récupérer un nom.

    Args:
        name_id (int): id name.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le nom n'existe pas.

    Returns:
        NameNestedOut: name.
    """
    db_name = crud.get_name(db, name_id=name_id)
    if db_name is None:
        raise HTTPException(status_code=404, detail="Name not found")
    return db_name


@router.get("/name-type/{name_type_id}", response_model=NameTypeOut)
async def read_name_type(
    name_type_id: int, db: Session = Depends(get_db)
) -> NameTypeOut:
    """Route pour récupérer un type de nom.

    Args:
        name_type_id (int): id name type.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le type de nom n'existe pas.

    Returns:
        NameTypeOut: name type.
    """
    db_name_type = crud.get_name_type(db, name_type_id=name_type_id)
    if db_name_type is None:
        raise HTTPException(status_code=404, detail=name_type_not_found)
    return db_name_type


@router.get("/name-type/code/{name_type_code}", response_model=NameTypeOut)
async def read_name_type_by_code(
    name_type_code: int, db: Session = Depends(get_db)
) -> NameTypeOut:
    """Route pour récupérer un type de nom par code.

    Args:
        name_type_code (int): code name type.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le type de nom n'existe pas.

    Returns:
        NameTypeOut: name type.
    """
    db_name_type_code = crud.get_name_type_code(db, name_type_code=name_type_code)
    if db_name_type_code is None:
        raise HTTPException(status_code=404, detail=name_type_not_found)
    return db_name_type_code


@router.get("/type/{name_type_id}", response_model=List[NameOut])
async def read_names_by_type(
    name_type_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[NameOut]:
    """Route pour récupérer une liste de noms par type.

    Args:
        name_type_id (int): id name type.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le type de nom n'existe pas.

    Returns:
        List[NameOut]: liste de name.
    """
    try:
        return crud.get_names_by_type(
            db, name_type_id=name_type_id, skip=skip, limit=limit
        )
    except AttributeError:
        raise HTTPException(status_code=404, detail=name_type_not_found)


@router.get("/type/code/{name_type_code}", response_model=List[NameOut])
async def read_names_by_type_code(
    name_type_code: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[NameOut]:
    """Route pour récupérer une liste de noms par type par code.

    Args:
        name_type_code (int): code name type.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le type de nom n'existe pas.

    Returns:
        List[NameOut]: liste de name.
    """
    try:
        return crud.get_names_by_type_code(
            db, name_type_code=name_type_code, skip=skip, limit=limit
        )
    except AttributeError:
        raise HTTPException(status_code=404, detail=name_type_not_found)


@router.post("/", response_model=NameNestedOut)
def create_name(name: NameCreate, db: Session = Depends(get_db)) -> NameNestedOut:
    """Route pour créer un nom.

    Args:
        name (NameCreate): name.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le nom n'a pas été crée.

    Returns:
        NameNestedOut: name.
    """
    try:
        return crud.create_name(db=db, name=name)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/name-types", response_model=NameTypeOut)
def create_name_types(
    name_types: NameTypeCreate, db: Session = Depends(get_db)
) -> NameTypeOut:
    """Route pour créer un type de nom.

    Args:
        name_types (NameTypeCreate): name type.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le type de nom n'a pas été crée.

    Returns:
        NameTypeOut: name type.
    """
    try:
        return crud.create_name_type(db=db, name_type=name_types)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{name_id}", response_model=NameNestedOut)
def update_name(
    name_id: int, name: NameUpdate, db: Session = Depends(get_db)
) -> NameNestedOut:
    """Route pour mettre à jour un nom.

    Args:
        name_id (int): id name.
        name (NameUpdate): name.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le nom n'a pas été mis à jour.

    Returns:
        NameNestedOut: name.
    """
    try:
        return crud.update_name(db=db, name_id=name_id, name=name)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/name-types/{name_type_id}", response_model=NameTypeOut)
def update_name_type(
    name_type_id: int, name_type: NameTypeUpdate, db: Session = Depends(get_db)
) -> NameTypeOut:
    """Route pour mettre à jour un type de nom.

    Args:
        name_type_id (int): id name type.
        name_type (NameTypeUpdate): name type.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le type de nom n'a pas été mis à jour.

    Returns:
        NameTypeOut: name type.
    """
    try:
        return crud.update_name_type(
            db=db, name_type_id=name_type_id, name_type=name_type
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{name_id}")
def delete_name(name_id: int, db: Session = Depends(get_db)) -> Response:
    """Route pour supprimer un nom.

    Args:
        name_id (int): id name.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le nom n'a pas été supprimé.

    Returns:
        Response: reponse.
    """
    try:
        crud.delete_name(db=db, name_id=name_id)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/name-types/{name_type_id}")
def delete_name_type(name_type_id: int, db: Session = Depends(get_db)) -> Response:
    """Route pour supprimer un type de nom.

    Args:
        name_type_id (int): id name type.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le type de nom n'a pas été supprimé.

    Returns:
        Response: reponse.
    """
    try:
        crud.delete_name_type(db=db, name_type_id=name_type_id)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/name-types/code/{name_type_code}")
def delete_name_type_code(
    name_type_code: int, db: Session = Depends(get_db)
) -> Response:
    """Route pour supprimer un type de nom par code.

    Args:
        name_type_code (int): code name type.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le type de nom n'a pas été supprimé.

    Returns:
        Response: reponse.
    """
    try:
        crud.delete_name_type_by_code(db=db, name_type_code=name_type_code)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
