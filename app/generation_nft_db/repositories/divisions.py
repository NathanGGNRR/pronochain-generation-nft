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

File: app/generation_nft_db/repositories/divisions.py
"""
from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import PronochainException
from app.generation_nft_db.models import countries as model_countries
from app.generation_nft_db.models import divisions as model_divisions
from app.generation_nft_db.schemas import divisions as schema_divisions


def get_division(
    db: Session, division_id: int, return_one: bool = True
) -> schema_divisions.DivisionNestedOut:
    """Récupère une division.

    Args:
        db (Session): session de la base de donnée.
        division_id (int): id division.
        return_one (bool, optional): retourne une seule ? Défaut à True.

    Returns:
        schema_divisions.DivisionNestedOut: division.
    """
    division_query = db.query(model_divisions.Division).filter(
        model_divisions.Division.id == division_id
    )
    return division_query.first() if return_one else division_query


def get_division_by_code(
    db: Session, division_code: int, return_one: bool = True
) -> schema_divisions.DivisionNestedOut:
    """Récupère une division par code.

    Args:
        db (Session): session de la base de donnée.
        division_code (int): code division.
        return_one (bool, optional): retourne une seule ? Défaut à True.

    Returns:
        schema_divisions.DivisionNestedOut: division.
    """
    division_code_query = db.query(model_divisions.Division).filter(
        model_divisions.Division.code == division_code
    )
    return division_code_query.first() if return_one else division_code_query


def get_divisions(
    db: Session, skip: int = 0, limit: int = 100
) -> List[schema_divisions.DivisionNestedOut]:
    """Récupère une liste de divisions.

    Args:
        db (Session): session de la base de donnée.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.

    Returns:
        List[schema_divisions.DivisionNestedOut]: liste de division.
    """
    return db.query(model_divisions.Division).offset(skip).limit(limit).all()


def get_divisions_by_country(
    db: Session, country_id: int
) -> List[schema_divisions.DivisionOut]:
    """Récupère une liste de divisions par pays.

    Args:
        db (Session): session de la base de donnée.
        country_id (int): id country.

    Raises:
        AttributeError: le pays n'existe pas.

    Returns:
        List[schema_divisions.DivisionOut]: liste de division.
    """
    try:
        country_divisions = (
            db.query(model_countries.Country)
            .filter(model_countries.Country.id == country_id)
            .first()
            .divisions
        )
    except Exception:
        raise AttributeError
    if any(country_divisions):
        return country_divisions
    return []


def get_divisions_by_country_code(
    db: Session, country_code: str
) -> List[schema_divisions.DivisionOut]:
    """Récupère une liste de divisions par pays par code.

    Args:
        db (Session): session de la base de donnée.
        country_code (str): code country.

    Raises:
        AttributeError: le pays n'existe pas.

    Returns:
        List[schema_divisions.DivisionOut]: liste de division.
    """
    try:
        country_divisions_code = (
            db.query(model_countries.Country)
            .filter(model_countries.Country.code == country_code)
            .first()
            .divisions
        )
    except Exception:
        raise AttributeError
    if any(country_divisions_code):
        return country_divisions_code
    return []


def create_division(
    db: Session, division: schema_divisions.DivisionCreate
) -> schema_divisions.DivisionNestedOut:
    """Crée une division.

    Args:
        db (Session): session de la base de donnée.
        division (schema_divisions.DivisionCreate): division.

    Raises:
        PronochainException: la division n'a pas été crée.

    Returns:
        schema_divisions.DivisionNestedOut: division.
    """
    try:
        db_division = model_divisions.Division(**division.dict())
        db.add(db_division)
        db.commit()
        db.refresh(db_division)
        return db_division
    except IntegrityError as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def update_division(
    db: Session, division_id: int, division: schema_divisions.DivisionUpdate
) -> schema_divisions.DivisionNestedOut:
    """Mettre à jour une division.

    Args:
        db (Session): session de la base de donnée.
        division_id (int): id division.
        division (schema_divisions.DivisionUpdate): division.

    Raises:
        PronochainException: la division n'a pas été mise à jour.

    Returns:
        schema_divisions.DivisionNestedOut: division
    """
    try:
        division = division.dict()
        db_division = get_division(db, division_id=division_id, return_one=False)
        db_division.update(division, synchronize_session=False)
        db.commit()
        db.refresh(db_division.first())
        return db_division.first()
    except Exception as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def delete_division(db: Session, division_id: int):
    """Supprime une division.

    Args:
        db (Session): session de la base de donnée.
        division_id (int): id division.

    Raises:
        PronochainException: la division n'a pas été supprimée.
    """
    db_division = get_division(db, division_id=division_id, return_one=False)
    if db_division.first() is not None:
        db_division.delete()
        db.commit()
    else:
        raise PronochainException("Division not found")


def delete_division_by_code(db: Session, division_code: int):
    """Supprime une division par code.

    Args:
        db (Session): session de la base de donnée.
        division_code (int): code division.

    Raises:
        PronochainException: la division n'a pas été supprimée.
    """
    db_division = get_division_by_code(
        db, division_code=division_code, return_one=False
    )
    if db_division.first() is not None:
        db_division.delete()
        db.commit()
    else:
        raise PronochainException("Division not found")
