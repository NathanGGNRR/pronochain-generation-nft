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

File: app/generation_nft_db/repositories/positions.py
"""
from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.exceptions import PronochainException
from app.generation_nft_db.models import positions as model_positions
from app.generation_nft_db.schemas import positions as schema_positions


def get_position(
    db: Session, position_id: int, return_one: bool = True
) -> schema_positions.PositionNestedOut:
    """Récupère une position.

    Args:
        db (Session): session de la base de donnée.
        position_id (int): id position.
        return_one (bool, optional): retourne une seule ? Défaut à True.

    Returns:
        schema_positions.PositionNestedOut: position.
    """
    position_query = (
        db.query(model_positions.Position)
        .options(joinedload(model_positions.Position.type))
        .filter(model_positions.Position.id == position_id)
    )
    return position_query.first() if return_one else position_query


def get_position_by_code(
    db: Session, position_code: int, return_one: bool = True
) -> schema_positions.PositionNestedOut:
    """Récupère une position par code.

    Args:
        db (Session): session de la base de donnée.
        position_code (int): code position.
        return_one (bool, optional): retourne une seule ? Défaut à True.

    Returns:
        schema_positions.PositionNestedOut: position.
    """
    position_code_query = db.query(model_positions.Position).filter(
        model_positions.Position.code == position_code
    )
    return position_code_query.first() if return_one else position_code_query


def get_position_type(
    db: Session, position_type_id: int, return_one: bool = True
) -> schema_positions.PositionTypeNestedOut:
    """Récupère un type de position.

    Args:
        db (Session): session de la base de donnée.
        position_type_id (int): id position type.
        return_one (bool, optional): retourne un seul ? Défaut à True.

    Returns:
        schema_positions.PositionTypeNestedOut: position type.
    """
    position_type_query = db.query(model_positions.PositionType).filter(
        model_positions.PositionType.id == position_type_id
    )
    return position_type_query.first() if return_one else position_type_query


def get_position_type_by_code(
    db: Session, position_type_code: int, return_one: bool = True
) -> schema_positions.PositionTypeNestedOut:
    """Récupère un type de position par code.

    Args:
        db (Session): session de la base de donnée.
        position_type_code (int): code position type.
        return_one (bool, optional): retourne un seul ? Défaut à True.

    Returns:
        schema_positions.PositionTypeNestedOut: position type.
    """
    position_type_code_query = db.query(model_positions.PositionType).filter(
        model_positions.PositionType.code == position_type_code
    )
    return position_type_code_query.first() if return_one else position_type_code_query


def get_positions(db: Session) -> List[schema_positions.PositionNestedOut]:
    """Récupère une liste de positions.

    Args:
        db (Session): session de la base de donnée.

    Returns:
        List[schema_positions.PositionNestedOut]: liste de positions.
    """
    return (
        db.query(model_positions.Position)
        .options(joinedload(model_positions.Position.type))
        .all()
    )


def get_position_types(db: Session) -> list[schema_positions.PositionTypeNestedOut]:
    """Récupère une liste de type de positions.

    Args:
        db (Session): session de la base de donnée.

    Returns:
        list[schema_positions.PositionTypeNestedOut]: liste de type de positions.
    """
    return db.query(model_positions.PositionType).all()


def get_positions_by_type(
    db: Session, position_type_id: int
) -> list[schema_positions.PositionOut]:
    """Récupère une liste de position par type.

    Args:
        db (Session): session de la base de donnée.
        position_type_id (int): id position type.

    Raises:
        AttributeError: le type de position n'existe pas.

    Returns:
        list[schema_positions.PositionOut]: liste de positions.
    """
    try:
        type_positions = (
            db.query(model_positions.PositionType)
            .filter(model_positions.PositionType.id == position_type_id)
            .first()
            .positions
        )
    except Exception:
        raise AttributeError
    if any(type_positions):
        return type_positions
    return []


def get_positions_by_type_code(
    db: Session, position_type_code: int
) -> list[schema_positions.PositionOut]:
    """Récupère une liste de position par type par code.

    Args:
        db (Session): session de la base de donnée.
        position_type_code (int): code position type.

    Raises:
        AttributeError: le type de position n'existe pas.

    Returns:
        list[schema_positions.PositionOut]: liste de positions.
    """
    try:
        type_positions_code = (
            db.query(model_positions.PositionType)
            .filter(model_positions.PositionType.code == position_type_code)
            .first()
            .positions
        )
    except Exception:
        raise AttributeError
    if any(type_positions_code):
        return type_positions_code
    return []


def create_position(
    db: Session, position: schema_positions.PositionCreate
) -> schema_positions.PositionNestedOut:
    """Crée une position.

    Args:
        db (Session): session de la base de donnée.
        position (schema_positions.PositionCreate): position.

    Raises:
        PronochainException: la position n'a pas été crée.

    Returns:
        schema_positions.PositionNestedOut: position.
    """
    try:
        db_position = model_positions.Position(**position.dict())
        db.add(db_position)
        db.commit()
        db.refresh(db_position)
        return db_position
    except IntegrityError as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def create_position_type(
    db: Session, position_type: schema_positions.PositionTypeCreate
) -> schema_positions.PositionTypeNestedOut:
    """Crée un type de position.

    Args:
        db (Session): session de la base de donnée.
        position_type (schema_positions.PositionTypeCreate): position type.

    Raises:
        PronochainException: le type de position n'a pas été crée.

    Returns:
        schema_positions.PositionTypeNestedOut: position type.
    """
    try:
        db_position_type = model_positions.PositionType(**position_type.dict())
        db.add(db_position_type)
        db.commit()
        db.refresh(db_position_type)
        return db_position_type
    except IntegrityError as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def update_position(
    db: Session, position_id: int, position: schema_positions.PositionUpdate
) -> schema_positions.PositionNestedOut:
    """Mettre à jour une position.

    Args:
        db (Session): session de la base de donnée.
        position_id (int): id position.
        position (schema_positions.PositionUpdate): position.

    Raises:
        PronochainException: la position n'a pas été mise à jour.

    Returns:
        schema_positions.PositionNestedOut: position.
    """
    try:
        position = position.dict()
        db_position = get_position(db, position_id=position_id, return_one=False)
        db_position.update(position, synchronize_session=False)
        db.commit()
        db.refresh(db_position.first())
        return db_position.first()
    except Exception as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def update_position_type(
    db: Session,
    position_type_id: int,
    position_type: schema_positions.PositionTypeUpdate,
) -> schema_positions.PositionTypeNestedOut:
    """Mettre à jour un type de position.

    Args:
        db (Session): session de la base de donnée.
        position_type_id (int): id position type.
        position_type (schema_positions.PositionTypeUpdate): position type.

    Raises:
        PronochainException: le type de position n'a pas été mis à jour.

    Returns:
        schema_positions.PositionTypeNestedOut: position type.
    """
    try:
        position_type = position_type.dict()
        db_position_type = get_position_type(
            db, position_type_id=position_type_id, return_one=False
        )
        db_position_type.update(position_type, synchronize_session=False)
        db.commit()
        db.refresh(db_position_type)
        return db_position_type
    except Exception as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def delete_position(db: Session, position_id: int):
    """Supprime une position.

    Args:
        db (Session): session de la base de donnée.
        position_id (int): id position.

    Raises:
        Exception: la position n'a pas été supprimée.
    """
    db_position = get_position(db, position_id=position_id, return_one=False)
    if db_position.first() is not None:
        db_position.delete()
        db.commit()
    else:
        raise PronochainException("Position not found")


def delete_position_by_code(db: Session, position_code: int):
    """Supprime une position par code.

    Args:
        db (Session): session de la base de donnée.
        position_code (int): code position.

    Raises:
        PronochainException: la position n'a pas été supprimée.
    """
    db_position = get_position_by_code(
        db, position_code=position_code, return_one=False
    )
    if db_position.first() is not None:
        db_position.delete()
        db.commit()
    else:
        raise PronochainException("Position not found")


def delete_position_type(db: Session, position_type_id: int):
    """Supprime un type de position.

    Args:
        db (Session): session de la base de donnée.
        position_type_id (int): id position type.

    Raises:
        PronochainException: le type de position n'a pas été supprimée.
    """
    db_position_type = get_position_type(
        db, position_type_id=position_type_id, return_one=False
    )
    if db_position_type.first() is not None:
        db_position_type.delete()
        db.commit()
    else:
        raise PronochainException("PositionType not found")


def delete_position_type_by_code(db: Session, position_type_code: int):
    """Supprime un type de position par code.

    Args:
        db (Session): session de la base de donnée.
        position_type_code (int): code position type.

    Raises:
        PronochainException: le type de position n'a pas été supprimée.
    """
    db_position_type = get_position_type_by_code(
        db, position_type_code=position_type_code, return_one=False
    )
    if db_position_type.first() is not None:
        db_position_type.delete()
        db.commit()
    else:
        raise PronochainException("PositionType not found")
