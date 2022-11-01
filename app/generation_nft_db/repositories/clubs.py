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

File: app/generation_nft_db/repositories/clubs.py
"""
from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.exceptions import PronochainException
from app.generation_nft_db.models import clubs as model_clubs
from app.generation_nft_db.models import countries as model_countries
from app.generation_nft_db.models import divisions as model_divisions
from app.generation_nft_db.models import players as model_players
from app.generation_nft_db.schemas import clubs as schema_clubs


def get_club(
    db: Session, club_id: int, return_one: bool = True
) -> schema_clubs.ClubNestedOut:
    """Récupère un club.

    Args:
        db (Session): session de la base de donnée.
        club_id (int): id club.
        return_one (bool, optional): retourne un seul ? Défaut à True.

    Returns:
        schema_clubs.ClubNestedOut: club.
    """
    club_query = db.query(model_clubs.Club).filter(model_clubs.Club.id == club_id)
    return club_query.first() if return_one else club_query


def get_club_by_code(
    db: Session, club_code: int, return_one: bool = True
) -> schema_clubs.ClubNestedOut:
    """Récupère un club par code.

    Args:
        db (Session): session de la base de donnée.
        club_code (int): code club.
        return_one (bool, optional): retourne un seul ? Défaut à True.

    Returns:
        schema_clubs.ClubNestedOut: club
    """
    club_code_query = db.query(model_clubs.Club).filter(
        model_clubs.Club.code == club_code
    )
    return club_code_query.first() if return_one else club_code_query


def get_club_by_player(db: Session, player_id: str) -> schema_clubs.ClubNestedOut:
    """Récupère un club par joueur.

    Args:
        db (Session): session de la base de donnée.
        player_id (str): id player.

    Returns:
        schema_clubs.ClubNestedOut: club.
    """
    return (
        db.query(model_players.Player)
        .filter(model_players.Player.id == player_id)
        .first()
        .club
    )


def get_club_by_player_code(
    db: Session, player_code: int
) -> schema_clubs.ClubNestedOut:
    """Récupère un club par joueur par code.

    Args:
        db (Session): session de la base de donnée.
        player_code (int): code player.

    Returns:
        schema_clubs.ClubNestedOut: club.
    """
    return (
        db.query(model_players.Player)
        .filter(model_players.Player.code == player_code)
        .first()
        .club
    )


def get_clubs(
    db: Session, skip: int = 0, limit: int = 100
) -> List[schema_clubs.ClubNestedOut]:
    """Récupère une liste de clubs.

    Args:
        db (Session): session de la base de donnée.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.

    Returns:
        List[schema_clubs.ClubNestedOut]: liste de club.
    """
    return db.query(model_clubs.Club).offset(skip).limit(limit).all()


def get_clubs_by_division(
    db: Session, division_id: int
) -> List[schema_clubs.ClubNestedOut]:
    """Récupère une liste de clubs par division.

    Args:
        db (Session): session de la base de donnée.
        division_id (int): id division.

    Raises:
        AttributeError: la division n'existe pas.

    Returns:
        List[schema_clubs.ClubNestedOut]: liste de club.
    """
    try:
        division_clubs = (
            db.query(model_divisions.Division)
            .filter(model_divisions.Division.id == division_id)
            .first()
            .clubs
        )
    except Exception:
        raise AttributeError
    if any(division_clubs):
        return division_clubs
    return []


def get_clubs_by_division_code(
    db: Session, division_code: int
) -> List[schema_clubs.ClubNestedOut]:
    """Récupère une liste de clubs par division par code.

    Args:
        db (Session): session de la base de donnée.
        division_code (int): code division.

    Raises:
        AttributeError: la division n'existe pas.

    Returns:
        List[schema_clubs.ClubNestedOut]: liste de club.
    """
    try:
        division_clubs_code = (
            db.query(model_divisions.Division)
            .filter(model_divisions.Division.code == division_code)
            .first()
            .clubs
        )
    except Exception:
        raise AttributeError
    if any(division_clubs_code):
        return division_clubs_code
    return []


def get_clubs_by_country(
    db: Session, country_id: int, skip: int = 0, limit: int = 100
) -> List[schema_clubs.ClubNestedOut]:
    """Récupère une liste de clubs par pays.

    Args:
        db (Session): session de la base de donnée.
        country_id (int): id country.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.

    Raises:
        AttributeError: le pays n'existe pas.

    Returns:
        List[schema_clubs.ClubNestedOut]: liste de club.
    """
    try:
        return (
            db.query(model_countries.Country)
            .filter(model_countries.Country.id == country_id)
            .first()
            .clubs[skip : skip + limit]
        )
    except Exception:
        raise AttributeError


def get_clubs_by_country_code(
    db: Session, country_code: str, skip: int = 0, limit: int = 100
) -> List[schema_clubs.ClubNestedOut]:
    """Récupère une liste de clubs par pays par code.

    Args:
        db (Session): session de la base de donnée.
        country_code (str): code country.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.

    Raises:
        AttributeError: le pays n'existe pas.

    Returns:
        List[schema_clubs.ClubNestedOut]: liste de club.
    """
    try:
        return (
            db.query(model_countries.Country)
            .filter(model_countries.Country.code == country_code)
            .first()
            .clubs[skip : skip + limit]
        )
    except Exception:
        raise AttributeError


def create_club(
    db: Session, club: schema_clubs.ClubCreate
) -> schema_clubs.ClubNestedOut:
    """Crée un club.

    Args:
        db (Session): session de la base de donnée.
        club (schema_clubs.ClubCreate): club.

    Raises:
        PronochainException: le club n'a pas été crée.

    Returns:
        schema_clubs.ClubNestedOut: club.
    """
    try:
        db_club = model_clubs.Club(**club.dict())
        db.add(db_club)
        db.commit()
        db.refresh(db_club)
        return db_club
    except IntegrityError as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def update_club(
    db: Session, club_id: int, club: schema_clubs.ClubUpdate
) -> schema_clubs.ClubNestedOut:
    """Mettre à jour un club.

    Args:
        db (Session): session de la base de donnée.
        club_id (int): id club.
        club (schema_clubs.ClubUpdate): club.

    Raises:
        PronochainException: le club n'a pas été mis à jour.

    Returns:
        schema_clubs.ClubNestedOut: club.
    """
    try:
        club = club.dict()
        db_club = get_club(db, club_id=club_id, return_one=False)
        db_club.update(club, synchronize_session=False)
        db.commit()
        db.refresh(db_club.first())
        return db_club.first()
    except Exception as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def delete_club(db: Session, club_id: int):
    """Supprime un club.

    Args:
        db (Session): session de la base de donnée.
        club_id (int): id club.

    Raises:
        PronochainException: le club n'a pas été supprimé.
    """
    db_club = get_club(db, club_id=club_id, return_one=False)
    if db_club.first() is not None:
        db_club.delete()
        db.commit()
    else:
        raise PronochainException("Club not found")


def delete_club_by_code(db: Session, club_code: int):
    """Supprime un club par code.

    Args:
        db (Session): session de la base de donnée.
        club_code (int): code club.

    Raises:
        PronochainException: le club n'a pas été supprimé.
    """
    db_club = get_club_by_code(db, club_code=club_code, return_one=False)
    if db_club.first() is not None:
        db_club.delete()
        db.commit()
    else:
        raise PronochainException("Club not found")
