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

File: app/generation_nft_db/repositories/stats.py
"""
from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import PronochainException
from app.generation_nft_db.models import positions as model_positions
from app.generation_nft_db.models import stats as model_stats
from app.generation_nft_db.schemas import stats as schema_stats


def get_stat(
    db: Session, stat_id: int, return_one: bool = True
) -> schema_stats.StatNestedOut:
    """Récupère une stat.

    Args:
        db (Session): session de la base de donnée.
        stat_id (int): id stat.
        return_one (bool, optional): retourne une seule ? Défaut à True.

    Returns:
        schema_stats.StatNestedOut: stat.
    """
    stat_query = db.query(model_stats.Stat).filter(model_stats.Stat.id == stat_id)
    return stat_query.first() if return_one else stat_query


def get_stat_by_code(
    db: Session, stat_code: int, return_one: bool = True
) -> schema_stats.StatNestedOut:
    """Récupère une stat par son code.

    Args:
        db (Session): session de la base de donnée.
        stat_code (int): code stat.
        return_one (bool, optional): retourne une seule ? Défaut à True.

    Returns:
        schema_stats.StatNestedOut: stat.
    """
    stat_code_query = db.query(model_stats.Stat).filter(
        model_stats.Stat.code == stat_code
    )
    return stat_code_query.first() if return_one else stat_code_query


def get_stat_type(
    db: Session, stat_type_id: int, return_one: bool = True
) -> schema_stats.StatTypeOut:
    """Récupère un type de stat.

    Args:
        db (Session): session de la base de donnée.
        stat_type_id (int): id stat type.
        return_one (bool, optional): retourne un seul ? Défaut à True.

    Returns:
        schema_stats.StatTypeOut: stat type.
    """
    stat_type_query = db.query(model_stats.StatType).filter(
        model_stats.StatType.id == stat_type_id
    )
    return stat_type_query.first() if return_one else stat_type_query


def get_stat_type_by_code(
    db: Session, stat_type_code: int, return_one: bool = True
) -> schema_stats.StatTypeOut:
    """Récupère un type de stat par son code.

    Args:
        db (Session): session de la base de donnée.
        stat_type_code (int): code stat type.
        return_one (bool, optional): retourne un seul ? Défaut à True.

    Returns:
        schema_stats.StatTypeOut: stat type.
    """
    stat_type_code_query = db.query(model_stats.StatType).filter(
        model_stats.StatType.code == stat_type_code
    )
    return stat_type_code_query.first() if return_one else stat_type_code_query


def get_stats(db: Session) -> List[schema_stats.StatNestedOut]:
    """Récupère une liste de stat.

    Args:
        db (Session): session de la base de donnée.

    Returns:
        List[schema_stats.StatNestedOut]: liste de stat.
    """
    return db.query(model_stats.Stat).all()


def get_stat_types(db: Session) -> List[schema_stats.StatTypeOut]:
    """Récupère une liste de type de stat.

    Args:
        db (Session): session de la base de donnée.

    Returns:
        List[schema_stats.StatTypeOut]: liste de stat type.
    """
    return db.query(model_stats.StatType).all()


def get_stats_by_type(db: Session, stat_type_id: int) -> List[schema_stats.StatOut]:
    """Récupère une liste de stat par type.

    Args:
        db (Session): session de la base de donnée.
        stat_type_id (int): id stat type.

    Raises:
        AttributeError: le type de stat n'existe pas.

    Returns:
        List[schema_stats.StatOut]: stat.
    """
    try:
        type_stats = (
            db.query(model_stats.StatType)
            .filter(model_stats.StatType.id == stat_type_id)
            .first()
            .stats
        )
    except Exception:
        raise AttributeError
    if any(type_stats):
        return type_stats
    return []


def get_stats_by_type_code(
    db: Session, stat_type_code: int
) -> List[schema_stats.StatOut]:
    """Récupère une liste de stat par type par code.

    Args:
        db (Session): session de la base de donnée.
        stat_type_code (int): code stat type.

    Raises:
        AttributeError: le type de stat n'existe pas.

    Returns:
        List[schema_stats.StatOut]: stat.
    """
    try:
        type_stats_code = (
            db.query(model_stats.StatType)
            .filter(model_stats.StatType.code == stat_type_code)
            .first()
            .stats
        )
    except Exception:
        raise AttributeError
    if any(type_stats_code):
        return type_stats_code
    return []


def create_stat(
    db: Session, stat: schema_stats.StatCreate
) -> schema_stats.StatNestedOut:
    """Crée une stat.

    Args:
        db (Session): session de la base de donnée.
        stat (schema_stats.StatCreate): stat.

    Raises:
        PronochainException: la stat n'a pas été crée.

    Returns:
        schema_stats.StatNestedOut: stat.
    """
    try:
        stat_dict = stat.dict()
        type_ids = stat_dict.pop("type_ids")
        position_ids = stat_dict.pop("position_ids")
        db_stat = model_stats.Stat(**stat_dict)
        if (
            db_types := db.query(model_stats.StatType).filter(
                model_stats.StatType.id.in_(type_ids)
            )
        ).count():
            db_stat.types = db_types.all()
        if (
            db_positions := db.query(model_positions.Position).filter(
                model_positions.Position.id.in_(position_ids)
            )
        ).count():
            db_stat.positions = db_positions.all()
        db.add(db_stat)
        db.commit()
        db.refresh(db_stat)
        return db_stat
    except IntegrityError as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def create_stat_type(
    db: Session, stat_type: schema_stats.StatTypeCreate
) -> schema_stats.StatTypeOut:
    """Crée un type de stat.

    Args:
        db (Session): session de la base de donnée.
        stat_type (schema_stats.StatTypeCreate): stat type.

    Raises:
        PronochainException: le type de stat n'a pas été crée.

    Returns:
        schema_stats.StatTypeOut: stat type.
    """
    try:
        db_stat_type = model_stats.StatType(**stat_type.dict())
        db.add(db_stat_type)
        db.commit()
        db.refresh(db_stat_type)
        return db_stat_type
    except IntegrityError as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def update_stat(
    db: Session, stat_id: int, stat: schema_stats.StatUpdate
) -> schema_stats.StatNestedOut:
    """Mettre à jour une stat.

    Args:
        db (Session): session de la base de donnée.
        stat_id (int): id stat.
        stat (schema_stats.StatUpdate): stat.

    Raises:
        PronochainException: la stat n'a pas été mise à jour.

    Returns:
        schema_stats.StatNestedOut: stat.
    """
    try:
        stat = stat.dict()
        type_ids = stat.pop("type_ids")
        position_ids = stat.pop("position_ids")
        db_stat = get_stat(db, stat_id=stat_id, return_one=False)
        db_stat_first = db_stat.first()
        db_stat_first.types = []
        db_stat_first.positions = []
        db.commit()

        db_stat.update(stat, synchronize_session=False)
        if (
            db_types := db.query(model_stats.StatType).filter(
                model_stats.StatType.id.in_(type_ids)
            )
        ).count():
            db_stat_first.types = db_types.all()
        if (
            db_positions := db.query(model_positions.Position).filter(
                model_positions.Position.id.in_(position_ids)
            )
        ).count():
            db_stat.positions = db_positions.all()
        db.commit()
        db.refresh(db_stat_first)
        return db_stat_first
    except Exception as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def update_stat_type(
    db: Session, stat_type_id: int, stat_type: schema_stats.StatTypeUpdate
) -> schema_stats.StatTypeOut:
    """Mettre à jour le type d'une stat.

    Args:
        db (Session): session de la base de donnée.
        stat_type_id (int): id stat type.
        stat_type (schema_stats.StatTypeUpdate): stat type.

    Raises:
        PronochainException: le type de stat n'a pas été mis à jour.

    Returns:
        schema_stats.StatTypeOut: stat type.
    """
    try:
        stat_type = stat_type.dict()
        db_stat_type = get_stat_type(db, stat_type_id=stat_type_id, return_one=False)
        db_stat_type.update(stat_type, synchronize_session=False)
        db.commit()
        db.refresh(db_stat_type.first())
        return db_stat_type.first()
    except Exception as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def delete_stat(db: Session, stat_id: int):
    """Supprime une stat.

    Args:
        db (Session): session de la base de donnée.
        stat_id (int): id stat.

    Raises:
        PronochainException: la stat n'a pas été supprimée.
    """
    db_stat = get_stat(db, stat_id=stat_id, return_one=False)
    if db_stat.first() is not None:
        db_stat.delete()
        db.commit()
    else:
        raise PronochainException("Stat not found")


def delete_stat_by_code(db: Session, stat_code: int):
    """Supprime une stat par code.

    Args:
        db (Session): session de la base de donnée.
        stat_code (int): code stat.

    Raises:
        PronochainException: la stat n'a pas été supprimée.
    """
    db_stat = get_stat_by_code(db, stat_code=stat_code, return_one=False)
    if db_stat.first() is not None:
        db_stat.delete()
        db.commit()
    else:
        raise PronochainException("Stat not found")


def delete_stat_type(db: Session, stat_type_id: int):
    """Supprime un type de stat.

    Args:
        db (Session): session de la base de donnée.
        stat_type_id (int): id stat type.

    Raises:
        PronochainException: le type de stat n'a pas été supprimé.
    """
    db_stat_type = get_stat_type(db, stat_type_id=stat_type_id, return_one=False)
    if db_stat_type.first() is not None:
        db_stat_type.delete()
        db.commit()
    else:
        raise PronochainException("StatType not found")


def delete_stat_type_by_code(db: Session, stat_type_code: int):
    """Supprime un type de stat par code.

    Args:
        db (Session): session de la base de donnée.
        stat_type_code (int): code stat type.

    Raises:
        PronochainException: le type de stat n'a pas été supprimé.
    """
    db_stat_type = get_stat_type_by_code(
        db, stat_type_code=stat_type_code, return_one=False
    )
    if db_stat_type.first() is not None:
        db_stat_type.delete()
        db.commit()
    else:
        raise PronochainException("StatType not found")
