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

File: app/generation_nft_api/routers/players.py
"""
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile
from sqlalchemy.orm import Session

from app.generation_nft_api.dependencies import get_current_active_superuser, get_db
from app.generation_nft_db.repositories import players as crud
from app.generation_nft_db.schemas.players import (
    PlayerCreate,
    PlayerNestedOut,
    PlayerUpdate,
)
from app.settings import settings

router = APIRouter(
    prefix="/players",
    tags=["players"],
    responses={404: {"description": "Not found"}},
    dependencies=[]
    if settings.AUTH_DISABLED
    else [Depends(get_current_active_superuser)],
)


@router.get("/{player_id}", response_model=PlayerNestedOut)
async def read_player(player_id: int, db: Session = Depends(get_db)) -> PlayerNestedOut:
    """Route pour récupérer un joueur.

    Args:
        player_id (int): id player.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le joueur n'existe pas.

    Returns:
        PlayerNestedOut: player.
    """
    db_player = crud.get_player(db, player_id=player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_player


@router.get("/code/{player_code}", response_model=PlayerNestedOut)
async def read_player_by_code(
    player_code: str, db: Session = Depends(get_db)
) -> PlayerNestedOut:
    """Route pour récupérer un joueur par code.

    Args:
        player_code (str): code player.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le joueur n'existe pas.

    Returns:
        PlayerNestedOut: player.
    """
    db_player_code = crud.get_player_by_code(db, player_code=player_code)
    if db_player_code is None:
        raise HTTPException(status_code=404, detail="Player code not found")
    return db_player_code


@router.get("/", response_model=List[PlayerNestedOut])
async def read_players(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[PlayerNestedOut]:
    """Route pour récupérer une liste de joueur.

    Args:
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Returns:
        List[PlayerNestedOut]: liste de player.
    """
    return crud.get_players(db, skip=skip, limit=limit)


@router.get("/country/{country_id}", response_model=List[PlayerNestedOut])
async def read_players_by_country(
    country_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[PlayerNestedOut]:
    """Route pour récupérer une liste de joueur par pays.

    Args:
        country_id (int): id country.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le pays n'existe pas.

    Returns:
        List[PlayerNestedOut]: liste de player.
    """
    try:
        return crud.get_players_by_country(
            db, country_id=country_id, skip=skip, limit=limit
        )
    except AttributeError:
        raise HTTPException(status_code=404, detail="Country not found")


@router.get("/country/code/{country_code}", response_model=List[PlayerNestedOut])
async def read_players_by_country_code(
    country_code: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[PlayerNestedOut]:
    """Route pour récupérer une liste de joueur par pays par code.

    Args:
        country_code (str): code country.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le pays n'existe pas.

    Returns:
        List[PlayerNestedOut]: liste de player.
    """
    try:
        return crud.get_players_by_country_code(
            db, country_code=country_code, skip=skip, limit=limit
        )
    except AttributeError:
        raise HTTPException(status_code=404, detail="Country not found")


@router.get("/club/{club_id}", response_model=List[PlayerNestedOut])
async def read_players_by_club(
    club_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[PlayerNestedOut]:
    """Route pour récupérer une liste de joueur par club.

    Args:
        club_id (int): id club.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le club n'existe pas.

    Returns:
        List[PlayerNestedOut]: liste de player.
    """
    try:
        return crud.get_players_by_club(db, club_id=club_id, skip=skip, limit=limit)
    except AttributeError:
        raise HTTPException(status_code=404, detail="Club not found")


@router.get("/club/code/{club_code}", response_model=List[PlayerNestedOut])
async def read_players_by_club_code(
    club_code: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[PlayerNestedOut]:
    """Route pour récupérer une liste de joueur par club par code.

    Args:
        club_code (int): code club.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le club n'existe pas.

    Returns:
        List[PlayerNestedOut]: liste de player.
    """
    try:
        return crud.get_players_by_club_code(
            db, club_code=club_code, skip=skip, limit=limit
        )
    except AttributeError:
        raise HTTPException(status_code=404, detail="Club not found")


@router.get("/rarity/{rarity_id}", response_model=List[PlayerNestedOut])
async def read_players_by_rarity(
    rarity_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[PlayerNestedOut]:
    """Route pour récupérer une liste de joueur par rareté.

    Args:
        rarity_id (int): id rarity.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: la rareté n'existe pas.

    Returns:
        List[PlayerNestedOut]: liste de player.
    """
    try:
        return crud.get_players_by_rarity(
            db, rarity_id=rarity_id, skip=skip, limit=limit
        )
    except AttributeError:
        raise HTTPException(status_code=404, detail="Rarity not found")


@router.get("/rarity/code/{rarity_code}", response_model=List[PlayerNestedOut])
async def read_players_by_rarity_code(
    rarity_code: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[PlayerNestedOut]:
    """Route pour récupérer une liste de joueur par rareté par code.

    Args:
        rarity_code (int): code rarity.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: la rareté n'existe pas.

    Returns:
        List[PlayerNestedOut]: liste de player.
    """
    try:
        return crud.get_players_by_rarity_code(
            db, rarity_code=rarity_code, skip=skip, limit=limit
        )
    except AttributeError:
        raise HTTPException(status_code=404, detail="Rarity not found")


@router.get("/first-name/{first_name_id}", response_model=List[PlayerNestedOut])
async def read_players_by_first_name(
    first_name_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[PlayerNestedOut]:
    """Route pour récupérer une liste de joueur par prénom.

    Args:
        first_name_id (int): id first name.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Returns:
        List[PlayerNestedOut]: liste de player.
    """
    return crud.get_players_by_first_name(
        db, first_name_id=first_name_id, skip=skip, limit=limit
    )


@router.get("/first-name/code/{first_name_code}", response_model=List[PlayerNestedOut])
async def read_players_by_first_name_code(
    first_name_code: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[PlayerNestedOut]:
    """Route pour récupérer une liste de joueur par prénom par code.

    Args:
        first_name_code (int): code first name.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Returns:
        List[PlayerNestedOut]: liste de player.
    """
    return crud.get_players_by_first_name_code(
        db, first_name_code=first_name_code, skip=skip, limit=limit
    )


@router.get("/last-name/{last_name_id}", response_model=List[PlayerNestedOut])
async def read_players_by_last_name(
    last_name_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[PlayerNestedOut]:
    """Route pour récupérer une liste de joueur par nom de famille.

    Args:
        last_name_id (int): id last name.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Returns:
        List[PlayerNestedOut]: liste de player.
    """
    return crud.get_players_by_last_name(
        db, last_name_id=last_name_id, skip=skip, limit=limit
    )


@router.get("/last-name/code/{last_name_code}", response_model=List[PlayerNestedOut])
async def read_players_by_last_name_code(
    last_name_code: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[PlayerNestedOut]:
    """Route pour récupérer une liste de joueur par nom de famille par code.

    Args:
        last_name_code (int): code last name.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Returns:
        List[PlayerNestedOut]: liste de player.
    """
    return crud.get_players_by_last_name_code(
        db, last_name_code=last_name_code, skip=skip, limit=limit
    )


@router.get("/height/{height}", response_model=List[PlayerNestedOut])
async def read_players_by_height(
    height: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[PlayerNestedOut]:
    """Route pour récupérer une liste de joueur par taille.

    Args:
        height (int): height.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Returns:
        List[PlayerNestedOut]: liste de player.
    """
    return crud.get_players_by_height(db, height=height, skip=skip, limit=limit)


@router.get("/weight/{weight}", response_model=List[PlayerNestedOut])
async def read_players_by_weight(
    weight: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[PlayerNestedOut]:
    """Route pour récupérer une liste de joueur par poids.

    Args:
        weight (int): weight.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Returns:
        List[PlayerNestedOut]: liste de player.
    """
    return crud.get_players_by_weight(db, weight=weight, skip=skip, limit=limit)


@router.get("/age/{age}", response_model=List[PlayerNestedOut])
async def read_players_by_age(
    age: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[PlayerNestedOut]:
    """Route pour récupérer une liste de joueur par age.

    Args:
        age (int): age.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Returns:
        List[PlayerNestedOut]: liste de player.
    """
    return crud.get_players_by_age(db, age=age, skip=skip, limit=limit)


@router.post("/", response_model=PlayerNestedOut)
def create_player(
    player: PlayerCreate = Depends(),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> PlayerNestedOut:
    """Route pour crée un joueur.

    Args:
        player (PlayerCreate, optional): player. Défaut à Depends().
        file (UploadFile, optional): photo du joueur. Défaut à File(...).
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le joueur n'a pas été crée.

    Returns:
        PlayerNestedOut: player.
    """
    try:
        return crud.create_player(db=db, player=player, file=file)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{player_id}", response_model=PlayerNestedOut)
def update_player(
    player_id: int,
    player: PlayerUpdate,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> PlayerNestedOut:
    """Route pour mettre à jour un joueur.

    Args:
        player_id (int): id player.
        player (PlayerUpdate): player.
        file (UploadFile, optional): photo du joueur. Défaut à File(...).
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le joueur n'a pas été mis à jour.

    Returns:
        PlayerNestedOut: player.
    """
    try:
        return crud.update_player(db=db, player_id=player_id, player=player, file=file)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{player_id}")
def delete_player(player_id: int, db: Session = Depends(get_db)) -> Response:
    """Route pour supprimer un joueur.

    Args:
        player_id (int): id player.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le joueur n'a pas été supprimée.

    Returns:
        Response: response.
    """
    try:
        crud.delete_player(db=db, player_id=player_id)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/code/{player_code}")
def delete_player_code(player_code: int, db: Session = Depends(get_db)) -> Response:
    """Route pour supprimer un joueur par code.

    Args:
        player_code (int): code player.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le joueur n'a pas été supprimée.

    Returns:
        Response: response.
    """
    try:
        crud.delete_player_by_code(db=db, player_code=player_code)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/generate-car")
def generate_car() -> Response:
    """Route pour générer un fichier CAR.

    Raises:
        HTTPException: impossible de générer le fichier CAR.

    Returns:
        Response: response.
    """
    try:
        response = crud.generate_car()
        return Response(status_code=response.status)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/upload-car")
def upload_car() -> Response:
    """Route pour stocker le fichier CAR dans nft.storage.

    Raises:
        HTTPException: impossible de stocker le fichier CAR.

    Returns:
        Response: response.
    """
    try:
        response = crud.upload_car()
        return Response(status_code=response.status)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
