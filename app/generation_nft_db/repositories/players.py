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

File: app/generation_nft_db/repositories/players.py
"""
import warnings
from dataclasses import fields
from typing import List

import requests
from fastapi import UploadFile
from psycopg2 import IntegrityError
from sqlalchemy import and_, func
from sqlalchemy.orm import Session, joinedload

from app.exceptions import PronochainException
from app.generation_nft.libraries.storage.storage import Storage
from app.generation_nft_api.utils import convert_player_names, convert_players_names
from app.generation_nft_db.constants import NameTypeCode, StatCode
from app.generation_nft_db.core.utils import add_into_database
from app.generation_nft_db.models import clubs as model_clubs
from app.generation_nft_db.models import countries as model_countries
from app.generation_nft_db.models import names as model_names
from app.generation_nft_db.models import players as model_players
from app.generation_nft_db.models import positions as model_positions
from app.generation_nft_db.models import rarities as model_rarities
from app.generation_nft_db.models import stats as model_stats
from app.generation_nft_db.schemas import players as schema_players
from app.settings import settings

warnings.filterwarnings("ignore")

nft_storage = Storage()

application_json = "application/json"


def get_player(
    db: Session, player_id: int, return_one: bool = True
) -> schema_players.PlayerNestedOut:
    """Récupère un joueur.

    Args:
        db (Session): session de la base de donnée.
        player_id (int): id player.
        return_one (bool, optional): retourne un seul ? Défaut à True.

    Returns:
        schema_players.PlayerNestedOut: player.
    """
    player_query = db.query(model_players.Player).filter(
        model_players.Player.id == player_id
    )
    return convert_player_names(player_query.first()) if return_one else player_query


def get_player_by_code(
    db: Session, player_code: int, return_one: bool = True
) -> schema_players.PlayerNestedOut:
    """Récupère un joueur par code.

    Args:
        db (Session): session de la base de donnée.
        player_code (int): code player.
        return_one (bool, optional): retourne un seul ? Défaut à True.

    Returns:
        schema_players.PlayerNestedOut: player.
    """
    player_code_query = db.query(model_players.Player).filter(
        model_players.Player.code == player_code
    )
    return (
        convert_player_names(player_code_query.first())
        if return_one
        else player_code_query
    )


def get_players(
    db: Session, skip: int = 0, limit: int = 100
) -> List[schema_players.PlayerNestedOut]:
    """Récupère une liste de players.

    Args:
        db (Session): session de la base de donnée.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.

    Returns:
        List[schema_players.PlayerNestedOut]: liste de players.
    """
    return convert_players_names(
        db.query(model_players.Player).offset(skip).limit(limit).all()
    )


def get_players_by_country(
    db: Session, country_id: int, skip: int = 0, limit: int = 100
) -> List[schema_players.PlayerNestedOut]:
    """Récupère une liste de players par pays.

    Args:
        db (Session): session de la base de donnée.
        country_id (int): id country.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.

    Raises:
        AttributeError: le pays n'existe pas.

    Returns:
        List[schema_players.PlayerNestedOut]: liste de players.
    """
    try:
        return convert_players_names(
            db.query(model_countries.Country)
            .filter(model_countries.Country.id == country_id)
            .first()
            .players[skip : skip + limit]
        )
    except Exception:
        raise AttributeError


def get_players_by_country_code(
    db: Session, country_code: str, skip: int = 0, limit: int = 100
) -> List[schema_players.PlayerNestedOut]:
    """Récupère une liste de players par pays par code.

    Args:
        db (Session): session de la base de donnée.
        country_code (str): code country.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.

    Raises:
        AttributeError: le pays n'existe pas.

    Returns:
        List[schema_players.PlayerNestedOut]: liste de players.
    """
    try:
        return convert_players_names(
            db.query(model_countries.Country)
            .filter(model_countries.Country.code == country_code)
            .first()
            .players[skip : skip + limit]
        )
    except Exception:
        raise AttributeError


def get_players_by_club(
    db: Session, club_id: int, skip: int = 0, limit: int = 100
) -> List[schema_players.PlayerNestedOut]:
    """Récupère une liste de players par club.

    Args:
        db (Session): session de la base de donnée.
        club_id (int): id club.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.

    Raises:
        AttributeError: le club n'existe pas.

    Returns:
        List[schema_players.PlayerNestedOut]: liste de players.
    """
    try:
        return convert_players_names(
            db.query(model_clubs.Club)
            .filter(model_clubs.Club.id == club_id)
            .first()
            .players[skip : skip + limit]
        )
    except Exception:
        raise AttributeError


def get_players_by_club_code(
    db: Session, club_code: int, skip: int = 0, limit: int = 100
) -> List[schema_players.PlayerNestedOut]:
    """Récupère une liste de players par club par code.

    Args:
        db (Session): session de la base de donnée.
        club_code (int): code club.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.

    Raises:
        AttributeError: le club n'existe pas.

    Returns:
        List[schema_players.PlayerNestedOut]: liste de players.
    """
    try:
        return convert_players_names(
            db.query(model_clubs.Club)
            .filter(model_clubs.Club.code == club_code)
            .first()
            .players[skip : skip + limit]
        )
    except Exception:
        raise AttributeError


def get_players_by_rarity(
    db: Session, rarity_id: int, skip: int = 0, limit: int = 100
) -> List[schema_players.PlayerNestedOut]:
    """Récupère une liste de players par rareté.

    Args:
        db (Session): session de la base de donnée.
        rarity_id (int): id rareté.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.

    Raises:
        AttributeError: la rareté n'existe pas.

    Returns:
        List[schema_players.PlayerNestedOut]: liste de players.
    """
    try:
        return convert_players_names(
            db.query(model_rarities.Rarity)
            .filter(model_rarities.Rarity.id == rarity_id)
            .first()
            .players[skip : skip + limit]
        )
    except Exception:
        raise AttributeError


def get_players_by_rarity_code(
    db: Session, rarity_code: int, skip: int = 0, limit: int = 100
) -> List[schema_players.PlayerNestedOut]:
    """Récupère une liste de players par rareté par code.

    Args:
        db (Session): session de la base de donnée.
        rarity_code (int): code rareté.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.

    Raises:
        AttributeError: la rareté n'existe pas.

    Returns:
        List[schema_players.PlayerNestedOut]: liste de players.
    """
    try:
        return convert_players_names(
            db.query(model_rarities.Rarity)
            .filter(model_rarities.Rarity.code == rarity_code)
            .first()
            .players[skip : skip + limit]
        )
    except Exception:
        raise AttributeError


def get_players_by_first_name(
    db: Session, first_name_id: int, skip: int = 0, limit: int = 100
) -> List[schema_players.PlayerNestedOut]:
    """Récupère une liste de players par prénom.

    Args:
        db (Session): session de la base de donnée.
        first_name_id (int): id first name.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.

    Raises:
        AttributeError: le prénom n'existe pas.

    Returns:
        List[schema_players.PlayerNestedOut]: liste de players.
    """
    try:
        return convert_players_names(
            db.query(model_names.Name)
            .filter(model_names.Name.id == first_name_id)
            .first()
            .players[skip : skip + limit]
        )
    except Exception:
        raise AttributeError


def get_players_by_first_name_code(
    db: Session, first_name_code: int, skip: int = 0, limit: int = 100
) -> List[schema_players.PlayerNestedOut]:
    """Récupère une liste de players par prénom par code.

    Args:
        db (Session): session de la base de donnée.
        first_name_code (int): code first name.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.

    Raises:
        AttributeError: le prénom n'existe pas.

    Returns:
        List[schema_players.PlayerNestedOut]: liste de players.
    """
    try:
        return convert_players_names(
            db.query(model_names.Name)
            .filter(model_names.Name.code == first_name_code)
            .first()
            .players[skip : skip + limit]
        )
    except Exception:
        raise AttributeError


def get_players_by_last_name(
    db: Session, last_name_id: int, skip: int = 0, limit: int = 100
) -> List[schema_players.PlayerNestedOut]:
    """Récupère une liste de players par nom de famille.

    Args:
        db (Session): session de la base de donnée.
        last_name_id (int): id last name.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.

    Raises:
        AttributeError: le nom de famille n'existe pas.

    Returns:
        List[schema_players.PlayerNestedOut]: liste de players.
    """
    try:
        return convert_players_names(
            db.query(model_names.Name)
            .filter(model_names.Name.id == last_name_id)
            .first()
            .players[skip : skip + limit]
        )
    except Exception:
        raise AttributeError


def get_players_by_last_name_code(
    db: Session, last_name_code: int, skip: int = 0, limit: int = 100
) -> List[schema_players.PlayerNestedOut]:
    """Récupère une liste de players par nom de famille par code.

    Args:
        db (Session): session de la base de donnée.
        last_name_code (int): code last name.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.

    Raises:
        AttributeError: le nom de famille n'existe pas.

    Returns:
        List[schema_players.PlayerNestedOut]: liste de players.
    """
    try:
        return convert_players_names(
            db.query(model_names.Name)
            .filter(model_names.Name.code == last_name_code)
            .first()
            .players[skip : skip + limit]
        )
    except Exception:
        raise AttributeError


def get_players_by_height(
    db: Session, height: int, skip: int = 0, limit: int = 100
) -> List[schema_players.PlayerNestedOut]:
    """Récupère une liste de players par taille.

    Args:
        db (Session): session de la base de donnée.
        height (int): taille.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.

    Returns:
        List[schema_players.PlayerNestedOut]: liste de players.
    """
    return convert_players_names(
        db.query(model_players.Player)
        .filter(model_players.Player.height == height)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_players_by_weight(
    db: Session, weight: int, skip: int = 0, limit: int = 100
) -> List[schema_players.PlayerNestedOut]:
    """Récupère une liste de players par poids.

    Args:
        db (Session): session de la base de donnée.
        weight (int): poids.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.

    Returns:
        List[schema_players.PlayerNestedOut]: liste de players.
    """
    return convert_players_names(
        db.query(model_players.Player)
        .filter(model_players.Player.weight == weight)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_players_by_age(
    db: Session, age: int, skip: int = 0, limit: int = 100
) -> List[schema_players.PlayerNestedOut]:
    """Récupère une liste de players par age.

    Args:
        db (Session): session de la base de donnée.
        age (int): age.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.

    Returns:
        List[schema_players.PlayerNestedOut]: liste de players.
    """
    return convert_players_names(
        db.query(model_players.Player)
        .filter(model_players.Player.age == age)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_player(
    db: Session, player: schema_players.PlayerCreate, file: UploadFile
) -> schema_players.PlayerNestedOut:
    """Crée un player.

    Args:
        db (Session): session de la base de donnée.
        player (schema_players.PlayerCreate): player.
        file (UploadFile): photo du joueur.

    Raises:
        PronochainException: le player n'a pas été crée.

    Returns:
        schema_players.PlayerNestedOut: player.
    """
    try:
        first_name = player.first_name
        last_name = player.last_name
        country_ids = player.country_ids
        position_ids = player.position_ids

        stats = []
        for field in fields(player):
            field_name = field.name.upper()
            field_value = getattr(player, field.name)
            if hasattr(StatCode, field_name):
                stat = (
                    db.query(model_stats.Stat)
                    .filter(
                        model_stats.Stat.code == getattr(StatCode, field_name).value
                    )
                    .first()
                )
                stats.append(
                    schema_players.PlayerStatCreate(stat_id=stat.id, value=field_value)
                )

        if settings.STORE_NFT_PART:
            response = nft_storage.add(file.file)
            db_player = model_players.Player(
                code=player.code,
                age=player.age,
                birth=player.birth,
                height=player.height,
                weight=player.weight,
                club_id=player.club_id,
                cid=response.value.cid,
                filename=file.filename,
            )
        else:
            db_player = model_players.Player(
                code=player.code,
                age=player.age,
                birth=player.birth,
                height=player.height,
                weight=player.weight,
                club_id=player.club_id,
                cid=None,
                filename=None,
            )

        db_first_name = (
            db.query(model_names.Name)
            .options(joinedload(model_names.Name.type))
            .filter(
                and_(
                    model_names.NameType.code == NameTypeCode.FIRST_NAME.value,
                    func.lower(model_names.Name.value) == first_name.lower(),
                )
            )
            .first()
        )
        if db_first_name is None:
            first_name_type = (
                db.query(model_names.NameType)
                .filter(model_names.NameType.code == NameTypeCode.FIRST_NAME.value)
                .first()
            )
            db_first_name = model_names.Name(value=first_name, type=first_name_type)
            add_into_database(db, db_first_name)

        db_last_name = (
            db.query(model_names.Name)
            .options(joinedload(model_names.Name.type))
            .filter(
                and_(
                    model_names.NameType.code == NameTypeCode.LAST_NAME.value,
                    func.lower(model_names.Name.value) == last_name.lower(),
                )
            )
            .first()
        )
        if db_last_name is None:
            last_name_type = (
                db.query(model_names.NameType)
                .filter(model_names.NameType.code == NameTypeCode.LAST_NAME.value)
                .first()
            )
            db_last_name = model_names.Name(value=last_name, type=last_name_type)
            add_into_database(db, db_last_name)

        db_player.first_name = db_first_name
        db_player.last_name = db_last_name

        if (
            db_countries := db.query(model_countries.Country).filter(
                model_countries.Country.id.in_(country_ids)
            )
        ).count():
            db_player.countries = db_countries.all()
        if (
            db_positions := db.query(model_positions.Position).filter(
                model_positions.Position.id.in_(position_ids)
            )
        ).count():
            db_player.positions = db_positions.all()

        db.add(db_player)
        db.commit()
        db.refresh(db_player)

        for stat in stats:
            stat.player_id = db_player.id
            db_player_stat = model_players.PlayerStat(**stat.dict())
            db.add(db_player_stat)
            db.commit()
            db.refresh(db_player_stat)

        return convert_player_names(db_player)
    except IntegrityError as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def update_player(
    db: Session, player_id: int, player: schema_players.PlayerUpdate, file: UploadFile
) -> schema_players.PlayerNestedOut:
    """Mettre à jour un player.

    Args:
        db (Session): session de la base de donnée.
        player_id (int): id player.
        player (schema_players.PlayerUpdate): player.
        file (UploadFile): photo du joueur.

    Raises:
        PronochainException: le player n'a pas été mis à jour.

    Returns:
        schema_players.PlayerNestedOut: player.
    """
    try:
        first_name = player.first_name
        last_name = player.last_name
        country_ids = player.country_ids
        position_ids = player.position_ids

        player_dict = {
            "code": player.code,
            "age": player.age,
            "birth": player.birth,
            "height": player.height,
            "weight": player.weight,
            "club_id": player.club_id,
            "cid": None,
            "filename": None,
        }

        stats = []
        for field in fields(player):
            field_name = field.name.upper()
            field_value = getattr(player, field.name)
            if hasattr(StatCode, field_name):
                stat = (
                    db.query(model_stats.Stat)
                    .filter(
                        model_stats.Stat.code == getattr(StatCode, field_name).value
                    )
                    .first()
                )
                stats.append(
                    schema_players.PlayerStatCreate(stat_id=stat.id, value=field_value)
                )

        db_player = get_player(db, player_id=player_id, return_one=False)
        db_player_first = db_player.first()

        db_player_first.countries = []
        db_player_first.positions = []
        db.commit()

        if settings.STORE_NFT_PART:
            nft_storage.delete(db_player_first.cid)
            response = nft_storage.add(file.file)
            player_dict["cid"] = (response.value.cid,)
            player_dict["filename"] = file.filename

        db_player.update(player_dict, synchronize_session=False)

        db_first_name = (
            db.query(model_names.Name)
            .options(joinedload(model_names.Name.type))
            .filter(
                and_(
                    model_names.NameType.code == NameTypeCode.FIRST_NAME.value,
                    func.lower(model_names.Name.value) == first_name.lower(),
                )
            )
            .first()
        )
        if db_first_name is None:
            first_name_type = (
                db.query(model_names.NameType)
                .filter(model_names.NameType.code == NameTypeCode.FIRST_NAME.value)
                .first()
            )
            db_first_name = model_names.Name(value=first_name, type=first_name_type)
            add_into_database(db, db_first_name)

        db_last_name = (
            db.query(model_names.Name)
            .options(joinedload(model_names.Name.type))
            .filter(
                and_(
                    model_names.NameType.code == NameTypeCode.LAST_NAME.value,
                    func.lower(model_names.Name.value) == last_name.lower(),
                )
            )
            .first()
        )
        if db_last_name is None:
            last_name_type = (
                db.query(model_names.NameType)
                .filter(model_names.NameType.code == NameTypeCode.LAST_NAME.value)
                .first()
            )
            db_last_name = model_names.Name(value=last_name, type=last_name_type)
            add_into_database(db, db_last_name)

        db_player_first.first_name = db_first_name
        db_player_first.last_name = db_last_name

        if (
            db_countries := db.query(model_countries.Country).filter(
                model_countries.Country.id.in_(country_ids)
            )
        ).count():
            db_player_first.countries = db_countries.all()
        if (
            db_positions := db.query(model_positions.Position).filter(
                model_positions.Position.id.in_(position_ids)
            )
        ).count():
            db_player_first.positions = db_positions.all()

        db.commit()
        db.refresh(db_player_first)

        db.query(model_players.PlayerStat).filter(
            model_players.PlayerStat.player_id == db_player_first.id
        ).delete()
        for stat in stats:
            stat.player_id = db_player.id
            db_player_stat = model_players.PlayerStat(**stat.dict())
            db.add(db_player_stat)
            db.commit()
            db.refresh(db_player_stat)

        return convert_player_names(db_player_first)
    except Exception as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def delete_player(db: Session, player_id: int):
    """Supprime un player.

    Args:
        db (Session): session de la base de donnée.
        player_id (int): id player.

    Raises:
        PronochainException: le player n'a pas été supprimé.
    """
    db_player = get_player(db, player_id=player_id, return_one=False)
    if db_player.first() is not None:
        if settings.STORE_NFT_PART:
            nft_storage.delete(db_player.first().cid)
        db_player.delete()
        db.commit()
    else:
        raise PronochainException("Player not found")


def delete_player_by_code(db: Session, player_code: int):
    """Supprime un player par code.

    Args:
        db (Session): session de la base de donnée.
        player_code (int): code player.

    Raises:
        PronochainException: le player n'a pas été supprimé.
    """
    db_player = get_player_by_code(db, player_code=player_code, return_one=False)
    if db_player.first() is not None:
        if settings.STORE_NFT_PART:
            nft_storage.delete(db_player.first().cid)
        db_player.delete()
        db.commit()
    else:
        raise PronochainException("Player not found")


def generate_car() -> schema_players.ResponseCarApi:
    """Génère un fichier CAR.

    Returns:
        schema_players.ResponseCarApi: response car api class.
    """
    headers = {"accept": application_json, "Content-Type": application_json}
    response = requests.post(
        f"http://{settings.CAR_API_SERVER}/generate-car", headers=headers
    )
    return schema_players.ResponseCarApi.parse_obj(response.json())


def upload_car() -> schema_players.ResponseCarApi:
    """Héberge le fichier CAR dans nft.storage.

    Returns:
        schema_players.ResponseCarApi: response car api class.
    """
    headers = {"accept": application_json, "Content-Type": application_json}
    response = requests.post(
        f"http://{settings.CAR_API_SERVER}/upload-car",
        json={"token": settings.NFT_STORAGE_API_KEY},
        headers=headers,
    )
    return schema_players.ResponseCarApi.parse_obj(response.json())


if __name__ == "__main__":
    headers = {"accept": application_json, "Content-Type": application_json}
    response = requests.post(
        f"http://{settings.CAR_API_SERVER}/upload-car",
        json={"token": settings.NFT_STORAGE_API_KEY},
        headers=headers,
    )
    test = schema_players.ResponseCarApi.parse_obj(response.json())
    print(test)
