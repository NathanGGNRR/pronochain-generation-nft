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

File: app/generation_nft_db/repositories/names.py
"""
from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import PronochainException
from app.generation_nft_db.models import names as model_names
from app.generation_nft_db.schemas import names as schema_names


def get_name(
    db: Session, name_id: int, return_one: bool = True
) -> schema_names.NameNestedOut:
    """Récupère un nom.

    Args:
        db (Session): session de la base de donnée.
        name_id (int): id name.
        return_one (bool, optional): retourne un seul ? Défaut à True.

    Returns:
        schema_names.NameNestedOut: name.
    """
    name_query = db.query(model_names.Name).filter(model_names.Name.id == name_id)
    return name_query.first() if return_one else name_query


def get_name_type(
    db: Session, name_type_id: int, return_one: bool = True
) -> schema_names.NameTypeOut:
    """Récupère le type d'un nom.

    Args:
        db (Session): session de la base de donnée.
        name_type_id (int): id name type.
        return_one (bool, optional): retourne un seul ? Défaut à True.

    Returns:
        schema_names.NameTypeOut: name type.
    """
    name_type_query = db.query(model_names.NameType).filter(
        model_names.NameType.id == name_type_id
    )
    return name_type_query.first() if return_one else name_type_query


def get_name_type_by_code(
    db: Session, name_type_code: int, return_one: bool = True
) -> schema_names.NameTypeOut:
    """Récupère le type d'un nom par code.

    Args:
        db (Session): session de la base de donnée.
        name_type_code (int): code name type.
        return_one (bool, optional): retourne un seul ? Défaut à True.

    Returns:
        schema_names.NameTypeOut: name type.
    """
    name_type_code_query = db.query(model_names.NameType).filter(
        model_names.NameType.code == name_type_code
    )
    return name_type_code_query.first() if return_one else name_type_code_query


def get_names(
    db: Session, skip: int = 0, limit: int = 100
) -> List[schema_names.NameNestedOut]:
    """Récupère une liste de noms.

    Args:
        db (Session): session de la base de donnée.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.

    Returns:
        List[schema_names.NameNestedOut]: liste de name.
    """
    return db.query(model_names.Name).offset(skip).limit(limit).all()


def get_name_types(db: Session) -> List[schema_names.NameTypeOut]:
    """Récupère une liste de type de noms.

    Args:
        db (Session): session de la base de donnée.

    Returns:
        List[schema_names.NameTypeOut]: liste de name type.
    """
    return db.query(model_names.NameType).all()


def get_names_by_type(
    db: Session, name_type_id: int, skip: int = 0, limit: int = 100
) -> List[schema_names.NameOut]:
    """Récupère une liste de noms par type.

    Args:
        db (Session): session de la base de donnée.
        name_type_id (int): id name type.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.

    Raises:
        AttributeError: le type de nom n'existe pas.

    Returns:
        List[schema_names.NameOut]: liste de name.
    """
    try:
        return (
            db.query(model_names.NameType)
            .filter(model_names.NameType.id == name_type_id)
            .first()
            .names[skip : skip + limit]
        )
    except Exception:
        raise AttributeError


def get_names_by_type_code(
    db: Session, name_type_code: int, skip: int = 0, limit: int = 100
) -> List[schema_names.NameOut]:
    """Récupère une liste de noms par type par code.

    Args:
        db (Session): session de la base de donnée.
        name_type_code (int): code name type.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.

    Raises:
        AttributeError: le type de nom n'existe pas.

    Returns:
        List[schema_names.NameOut]: liste de name.
    """
    try:
        return (
            db.query(model_names.NameType)
            .filter(model_names.NameType.code == name_type_code)
            .first()
            .names[skip : skip + limit]
        )
    except Exception:
        raise AttributeError


def create_name(
    db: Session, name: schema_names.NameCreate
) -> schema_names.NameNestedOut:
    """Crée un nom.

    Args:
        db (Session): session de la base de donnée.
        name (schema_names.NameCreate): name.

    Raises:
        PronochainException: le nom n'a pas été crée.

    Returns:
        schema_names.NameNestedOut: name
    """
    try:
        db_name = model_names.Name(**name.dict())
        db.add(db_name)
        db.commit()
        db.refresh(db_name)
        return db_name
    except IntegrityError as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def create_name_type(
    db: Session, name_type: schema_names.NameTypeCreate
) -> schema_names.NameTypeOut:
    """Crée un type de nom.

    Args:
        db (Session): session de la base de donnée.
        name_type (schema_names.NameTypeCreate): name type.

    Raises:
        PronochainException: le type de nom n'a pas été crée.

    Returns:
        schema_names.NameTypeOut: name type.
    """
    try:
        db_name_type = model_names.NameType(**name_type.dict())
        db.add(db_name_type)
        db.commit()
        db.refresh(db_name_type)
        return db_name_type
    except IntegrityError as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def update_name(
    db: Session, name_id: int, name: schema_names.NameUpdate
) -> schema_names.NameNestedOut:
    """Mettre à jour un nom.

    Args:
        db (Session): session de la base de donnée.
        name_id (int): id name.
        name (schema_names.NameUpdate): name.

    Raises:
        PronochainException: le nom n'a pas été mis à jour.

    Returns:
        schema_names.NameNestedOut: name.
    """
    try:
        name = name.dict()
        db_name = get_name(db, name_id=name_id, return_one=False)
        db_name.update(name, synchronize_session=False)
        db.commit()
        db.refresh(db_name.first())
        return db_name.first()
    except Exception as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def update_name_type(
    db: Session, name_type_id: int, name_type: schema_names.NameTypeUpdate
) -> schema_names.NameTypeOut:
    """Mettre à jour le type d'un nom.

    Args:
        db (Session): session de la base de donnée.
        name_type_id (int): id name type.
        name_type (schema_names.NameTypeUpdate): name type.

    Raises:
        PronochainException: le type de nom n'a pas été mis à jour.

    Returns:
        schema_names.NameTypeOut: name type.
    """
    try:
        name_type = name_type.dict()
        db_name_type = get_name_type(db, name_type_id=name_type_id, return_one=False)
        db_name_type.update(name_type, synchronize_session=False)
        db.commit()
        db.refresh(db_name_type.first())
        return db_name_type.first()
    except Exception as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def delete_name(db: Session, name_id: int):
    """Supprime un nom.

    Args:
        db (Session): session de la base de donnée.
        name_id (int): id name.

    Raises:
        PronochainException: le nom n'a pas été supprimé.
    """
    db_name = get_name(db, name_id=name_id, return_one=False)
    if db_name.first() is not None:
        db_name.delete()
        db.commit()
    else:
        raise PronochainException("Name not found")


def delete_name_type(db: Session, name_type_id: int):
    """Supprime un type de nom.

    Args:
        db (Session): session de la base de donnée.
        name_type_id (int): id name type.

    Raises:
        PronochainException: le type de nom n'a pas été supprimé.
    """
    db_name_type = get_name_type(db, name_type_id=name_type_id, return_one=False)
    if db_name_type.first() is not None:
        db_name_type.delete()
        db.commit()
    else:
        raise PronochainException("NameType not found")


def delete_name_type_by_code(db: Session, name_type_code: int):
    """Supprime un type de nom par code.

    Args:
        db (Session): session de la base de donnée.
        name_type_code (int): code name type.

    Raises:
        PronochainException: le type de nom n'a pas été supprimé.
    """
    db_name_type = get_name_type_by_code(
        db, name_type_code=name_type_code, return_one=False
    )
    if db_name_type.first() is not None:
        db_name_type.delete()
        db.commit()
    else:
        raise PronochainException("NameType not found")
