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

File: app/generation_nft_api/routers/clubs.py
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.generation_nft_api.dependencies import get_current_active_superuser, get_db
from app.generation_nft_db.repositories import clubs as crud
from app.generation_nft_db.schemas.clubs import ClubCreate, ClubNestedOut, ClubUpdate
from app.settings import settings

router = APIRouter(
    prefix="/clubs",
    tags=["clubs"],
    responses={404: {"description": "Not found"}},
    dependencies=[]
    if settings.AUTH_DISABLED
    else [Depends(get_current_active_superuser)],
)


@router.get("/", response_model=List[ClubNestedOut])
async def read_clubs(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[ClubNestedOut]:
    """Route pour récupérer une liste de clubs.

    Args:
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Returns:
        List[ClubNestedOut]: liste de club.
    """
    return crud.get_clubs(db, skip=skip, limit=limit)


@router.get("/division/{division_id}", response_model=List[ClubNestedOut])
async def read_clubs_by_division(
    division_id: int, db: Session = Depends(get_db)
) -> List[ClubNestedOut]:
    """Route pour récupérer une liste de clubs par division.

    Args:
        division_id (int): _description_
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: la division n'existe pas.

    Returns:
        List[ClubNestedOut]: liste de club.
    """
    try:
        return crud.get_clubs_by_division(db, division_id=division_id)
    except AttributeError:
        raise HTTPException(status_code=404, detail="Division not found")


@router.get("/division/code/{division_code}", response_model=List[ClubNestedOut])
async def read_clubs_by_division_code(
    division_code: int, db: Session = Depends(get_db)
) -> List[ClubNestedOut]:
    """Route pour récupérer une liste de clubs par division par code.

    Args:
        division_code (int): code division.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: la division n'existe pas.

    Returns:
        List[ClubNestedOut]: liste de club.
    """
    try:
        return crud.get_clubs_by_division_code(db, division_code=division_code)
    except AttributeError:
        raise HTTPException(status_code=404, detail="Division not found")


@router.get("/country/{country_id}", response_model=List[ClubNestedOut])
async def read_clubs_by_country(
    country_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[ClubNestedOut]:
    """Route pour récupérer une liste de clubs par pays.

    Args:
        country_id (int): id country.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le pays n'existe pas.

    Returns:
        List[ClubNestedOut]: liste de club.
    """
    try:
        return crud.get_clubs_by_country(
            db, country_id=country_id, skip=skip, limit=limit
        )
    except AttributeError:
        raise HTTPException(status_code=404, detail="Country not found")


@router.get("/country/code/{country_code}", response_model=List[ClubNestedOut])
async def read_clubs_by_country_code(
    country_code: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[ClubNestedOut]:
    """Route pour récupérer une liste de clubs par pays par code.

    Args:
        country_code (str): code country.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le pays n'existe pas.

    Returns:
        List[ClubNestedOut]: liste de club.
    """
    try:
        return crud.get_clubs_by_country_code(
            db, country_code=country_code, skip=skip, limit=limit
        )
    except AttributeError:
        raise HTTPException(status_code=404, detail="Country not found")


@router.get("/{club_id}", response_model=ClubNestedOut)
async def read_club(club_id: int, db: Session = Depends(get_db)) -> ClubNestedOut:
    """Route pour récupérer un club.

    Args:
        club_id (int): id club.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le club n'existe pas.

    Returns:
        ClubNestedOut: club.
    """
    db_club = crud.get_club(db, club_id=club_id)
    if db_club is None:
        raise HTTPException(status_code=404, detail="Club not found")
    return db_club


@router.get("/code/{club_code}", response_model=ClubNestedOut)
async def read_club_code(
    club_code: int, db: Session = Depends(get_db)
) -> ClubNestedOut:
    """Route pour récupérer un club par code.

    Args:
        club_code (int): code club.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le club n'existe pas.

    Returns:
        ClubNestedOut: club.
    """
    db_club_code = crud.get_club_by_code(db, club_code=club_code)
    if db_club_code is None:
        raise HTTPException(status_code=404, detail="Club not found")
    return db_club_code


@router.get("/player/{player_id}", response_model=ClubNestedOut)
async def read_club_by_player(
    player_id: int, db: Session = Depends(get_db)
) -> ClubNestedOut:
    """Route pour récupérer un club par joueur.

    Args:
        player_id (int): id player.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le joueur n'existe pas.

    Returns:
        ClubNestedOut: club.
    """
    db_player_club = crud.get_club_by_player(db, player_id=player_id)
    if db_player_club is None:
        raise HTTPException(status_code=404, detail="Player club not found")
    return db_player_club


@router.get("/player/code/{player_code}", response_model=ClubNestedOut)
async def read_club_by_player_code(
    player_code: int, db: Session = Depends(get_db)
) -> ClubNestedOut:
    """Route pour récupérer un club par joueur par code.

    Args:
        player_code (int): code player.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le joueur n'existe pas.

    Returns:
        ClubNestedOut: club.
    """
    db_player_club_code = crud.get_club_by_player_code(db, player_code=player_code)
    if db_player_club_code is None:
        raise HTTPException(status_code=404, detail="Player club not found")
    return db_player_club_code


@router.post("/", response_model=ClubNestedOut)
def create_club(club: ClubCreate, db: Session = Depends(get_db)) -> ClubNestedOut:
    """Route pour créer un club.

    Args:
        club (ClubCreate): club.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le club n'a pas été crée.

    Returns:
        ClubNestedOut: club.
    """
    try:
        return crud.create_club(db=db, club=club)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{club_id}", response_model=ClubNestedOut)
def update_club(
    club_id: int, club: ClubUpdate, db: Session = Depends(get_db)
) -> ClubNestedOut:
    """Route pour mettre à jour un club.

    Args:
        club_id (int): id club.
        club (ClubUpdate): club.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le club n'a pas été mis à jour.

    Returns:
        ClubNestedOut: club.
    """
    try:
        return crud.update_club(db=db, club_id=club_id, club=club)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{club_id}")
def delete_club(club_id: int, db: Session = Depends(get_db)) -> Response:
    """Route pour supprimer un club.

    Args:
        club_id (int): id club.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le club n'a pas été supprimé.

    Returns:
        Response: response.
    """
    try:
        crud.delete_club(db=db, club_id=club_id)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/code/{club_code}")
def delete_club_code(club_code: int, db: Session = Depends(get_db)) -> Response:
    """Route pour supprimer un club par code.

    Args:
        club_code (int): code club.
        db (Session, optional): session de la base de donnée. Défaut à Depends(get_db).

    Raises:
        HTTPException: le club n'a pas été supprimé.

    Returns:
        Response: response.
    """
    try:
        crud.delete_club_by_code(db=db, club_code=club_code)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
