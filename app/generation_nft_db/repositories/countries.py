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

File: app/generation_nft_db/repositories/countries.py
"""
from typing import List

from fastapi import UploadFile
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import PronochainException
from app.generation_nft.libraries.storage.storage import Storage
from app.generation_nft_db.models import countries as model_countries
from app.generation_nft_db.schemas import countries as schema_countries
from app.settings import settings

nft_storage = Storage()


def get_country(
    db: Session, country_id: int, return_one: bool = True
) -> schema_countries.CountryOut:
    """Récupère un pays.

    Args:
        db (Session): session de la base de donnée.
        country_id (int): id country.
        return_one (bool, optional): retourne un seul ? Défaut à True.

    Returns:
        schema_countries.CountryOut: country.
    """
    country_query = db.query(model_countries.Country).filter(
        model_countries.Country.id == country_id
    )
    return country_query.first() if return_one else country_query


def get_country_by_code(
    db: Session, country_code: str, return_one: bool = True
) -> schema_countries.CountryOut:
    """Récupère un pays par code.

    Args:
        db (Session): session de la base de donnée.
        country_code (str): code country.
        return_one (bool, optional): retourne un seul ? Défaut à True.

    Returns:
        schema_countries.CountryOut: country.
    """
    country_code_query = db.query(model_countries.Country).filter(
        model_countries.Country.code == country_code
    )
    return country_code_query.first() if return_one else country_code_query


def get_countries(
    db: Session, skip: int = 0, limit: int = 100
) -> List[schema_countries.CountryOut]:
    """Récupère une liste de pays.

    Args:
        db (Session): session de la base de donnée.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.

    Returns:
        List[schema_countries.CountryOut]: liste de country.
    """
    return db.query(model_countries.Country).offset(skip).limit(limit).all()


def create_country(
    db: Session, code: str, value: str, file: UploadFile
) -> schema_countries.CountryOut:
    """Crée un pays.

    Args:
        db (Session): session de la base de donnée.
        code (str): code du pays.
        value (str): nom du pays.
        file (UploadFile): drapeau du pays.

    Raises:
        PronochainException: le pays n'a pas été crée.

    Returns:
        schema_countries.CountryOut: country.
    """
    try:
        if settings.STORE_NFT_PART:
            response = nft_storage.add(file.file)
            db_country = model_countries.Country(
                code=code, value=value, cid=response.value.cid, filename=file.filename
            )
        else:
            db_country = model_countries.Country(
                code=code, value=value, cid=None, filename=None
            )
        db.add(db_country)
        db.commit()
        db.refresh(db_country)
        return db_country
    except IntegrityError as e:
        nft_storage.delete(response.value.cid)
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def update_country(
    db: Session, country_id: int, code: str, value: str, file: UploadFile
) -> schema_countries.CountryOut:
    """Mettre à jour un pays.

    Args:
        db (Session): session de la base de donnée.
        country_id (int): id country.
        code (str): code du pays.
        value (str): nom du pays.
        file (UploadFile): drapeau du pays.

    Raises:
        PronochainException: le pays n'a pas été mis à jour.

    Returns:
        schema_countries.CountryOut: country.
    """
    try:
        db_country = get_country(db, country_id=country_id, return_one=False)
        country = {"code": code, "value": value, "cid": None, "filename": None}

        if settings.STORE_NFT_PART:
            nft_storage.delete(db_country.first().cid)
            response = nft_storage.add(file.file)
            country["cid"] = (response.value.cid,)
            country["filename"] = file.filename

        db_country.update(country, synchronize_session=False)
        db.commit()
        db.refresh(db_country.first())
        return db_country.first()
    except Exception as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def delete_country(db: Session, country_id: int):
    """Supprime un pays.

    Args:
        db (Session): session de la base de donnée.
        country_id (int): id country.

    Raises:
        PronochainException: le pays n'a pas été supprimé.
    """
    db_country = get_country(db, country_id=country_id, return_one=False)
    if db_country.first() is not None:
        if settings.STORE_NFT_PART:
            nft_storage.delete(db_country.first().cid)
        db_country.delete()
        db.commit()
    else:
        raise PronochainException("Country not found")


def delete_country_by_code(db: Session, country_code: str):
    """Supprime un pays par code.

    Args:
        db (Session): session de la base de donnée.
        country_code (str): code country.

    Raises:
        PronochainException: le pays n'a pas été supprimé.
    """
    db_country = get_country_by_code(db, country_code=country_code, return_one=False)
    if db_country.first() is not None:
        if settings.STORE_NFT_PART:
            nft_storage.delete(db_country.first().cid)
        db_country.delete()
        db.commit()
    else:
        raise PronochainException("Country not found")
