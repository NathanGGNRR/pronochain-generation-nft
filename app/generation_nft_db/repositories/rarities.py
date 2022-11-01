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

File: app/generation_nft_db/repositories/rarities.py
"""
from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import PronochainException
from app.generation_nft_db.models import rarities as model_rarities
from app.generation_nft_db.schemas import rarities as schema_rarities


def get_rarity(
    db: Session, rarity_id: int, return_one: bool = True
) -> schema_rarities.RarityOut:
    """Récupère une rareté.

    Args:
        db (Session): session de la base de donnée.
        rarity_id (int): id rareté.
        return_one (bool, optional): retourne une seule ? Défaut à True.

    Returns:
        schema_rarities.RarityOut: rareté.
    """
    rarity_query = db.query(model_rarities.Rarity).filter(
        model_rarities.Rarity.id == rarity_id
    )
    return rarity_query.first() if return_one else rarity_query


def get_rarity_by_code(
    db: Session, rarity_code: int, return_one: bool = True
) -> schema_rarities.RarityOut:
    """Récupère une rareté par code.

    Args:
        db (Session): session de la base de donnée.
        rarity_code (int): code rareté.
        return_one (bool, optional): retourne une seule ? Défaut à True.

    Returns:
        schema_rarities.RarityOut: rareté.
    """
    rarity_code_query = db.query(model_rarities.Rarity).filter(
        model_rarities.Rarity.code == rarity_code
    )
    return rarity_code_query.first() if return_one else rarity_code_query


def get_rarities(db: Session) -> List[schema_rarities.RarityOut]:
    """Récupère une liste de raretés.

    Args:
        db (Session): session de la base de donnée.

    Returns:
        List[schema_rarities.RarityOut]: liste de raretés.
    """
    return db.query(model_rarities.Rarity).all()


def create_rarity(
    db: Session, rarity: schema_rarities.RarityCreate
) -> schema_rarities.RarityOut:
    """Crée une rareté.

    Args:
        db (Session): session de la base de donnée.
        rarity (schema_rarities.RarityCreate): rareté.

    Raises:
        PronochainException: la rareté n'a pas été crée.

    Returns:
        schema_rarities.RarityOut: rareté.
    """
    try:
        db_rarity = model_rarities.Rarity(**rarity.dict())
        db.add(db_rarity)
        db.commit()
        db.refresh(db_rarity)
        return db_rarity
    except IntegrityError as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def update_rarity(
    db: Session, rarity_id: int, rarity: schema_rarities.RarityUpdate
) -> schema_rarities.RarityOut:
    """Mettre à jour une rareté.

    Args:
        db (Session): session de la base de donnée.
        rarity_id (int): id rareté.
        rarity (schema_rarities.RarityUpdate): rareté.

    Raises:
        PronochainException: la rareté n'a pas été mise à jour.

    Returns:
        schema_rarities.RarityOut: rareté.
    """
    try:
        rarity = rarity.dict()
        db_rarity = get_rarity(db, rarity_id=rarity_id, return_one=False)
        db_rarity.update(rarity, synchronize_session=False)
        db.commit()
        db.refresh(db_rarity.first())
        return db_rarity.first()
    except Exception as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def delete_rarity(db: Session, rarity_id: int):
    """Supprime une rareté.

    Args:
        db (Session): session de la base de donnée.
        rarity_id (int): id rareté.

    Raises:
        PronochainException: la rareté n'a pas été supprimée.
    """
    db_rarity = get_rarity(db, rarity_id=rarity_id, return_one=False)
    if db_rarity.first() is not None:
        db_rarity.delete()
        db.commit()
    else:
        raise PronochainException("Rarity not found")


def delete_rarity_by_code(db: Session, rarity_code: int):
    """Supprime une rareté par code.

    Args:
        db (Session): session de la base de donnée.
        rarity_code (int): code rareté.

    Raises:
        PronochainException: la rareté n'a pas été supprimée.
    """
    db_rarity = get_rarity_by_code(db, rarity_code=rarity_code, return_one=False)
    if db_rarity.first() is not None:
        db_rarity.delete()
        db.commit()
    else:
        raise PronochainException("Rarity not found")
