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

File: app/generation_nft_api/routers/nft_parts.py
"""
from typing import List

from fastapi import APIRouter, Depends, File, Form, HTTPException, Response, UploadFile
from sqlalchemy.orm import Session

from app.generation_nft_api.dependencies import get_current_active_superuser, get_db
from app.generation_nft_db.repositories import nft_parts as crud
from app.generation_nft_db.schemas.nft_parts import (
    ColorCreate,
    ColorNestedOut,
    ColorOut,
    ColorUpdate,
    DependentFacePartColorCreate,
    DependentFacePartColorDelete,
    ElementNestedOut,
    ElementOut,
    ElementTypeCreate,
    ElementTypeNestedOut,
    ElementTypeUpdate,
    FacePartCreate,
    FacePartNestedOut,
    FacePartUpdate,
    NftPartCreate,
    NftPartNestedOut,
    NftPartUpdate,
)
from app.settings import settings

router = APIRouter(
    prefix="/nft",
    tags=["nft"],
    responses={404: {"description": "Not found"}},
    dependencies=[]
    if settings.AUTH_DISABLED
    else [Depends(get_current_active_superuser)],
)

nft_part_not_found = "Nft part not found"
element_part_not_found = "Element type not found"
rarity_part_not_found = "Rarity not found"


@router.get("/nft-parts", response_model=List[NftPartNestedOut])
async def read_nft_parts(db: Session = Depends(get_db)) -> List[NftPartNestedOut]:
    """Route pour r??cup??rer une liste de partie de NFT.

    Args:
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Returns:
        List[NftPartNestedOut]: liste de nft part.
    """
    return crud.get_nft_parts(db)


@router.get("/nft-parts/{nft_part_id}", response_model=NftPartNestedOut)
async def read_nft_part(
    nft_part_id: int, db: Session = Depends(get_db)
) -> NftPartNestedOut:
    """Route pour r??cup??rer une partie de NFT.

    Args:
        nft_part_id (int): id nft part.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: la partie du NFT n'existe pas.

    Returns:
        NftPartNestedOut: nft part.
    """
    db_nft_part = crud.get_nft_part(db, nft_part_id=nft_part_id)
    if db_nft_part is None:
        raise HTTPException(status_code=404, detail=nft_part_not_found)
    return db_nft_part


@router.get("/nft-parts/code/{nft_part_code}", response_model=NftPartNestedOut)
async def read_nft_part_code(
    nft_part_code: int, db: Session = Depends(get_db)
) -> NftPartNestedOut:
    """Route pour r??cup??rer une partie de NFT par code.

    Args:
        nft_part_code (int): code nft part.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: la partie du NFT n'existe pas.

    Returns:
        NftPartNestedOut: nft part.
    """
    db_nft_part_code = crud.get_nft_part_by_code(db, nft_part_code=nft_part_code)
    if db_nft_part_code is None:
        raise HTTPException(status_code=404, detail=nft_part_not_found)
    return db_nft_part_code


@router.post("/nft-parts", response_model=NftPartNestedOut)
def create_nft_part(
    nft_part: NftPartCreate, db: Session = Depends(get_db)
) -> NftPartNestedOut:
    """Route pour cr??er une partie de NFT.

    Args:
        nft_part (NftPartCreate): nft part.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: la partie du NFT n'a pas ??t?? cr??e.

    Returns:
        NftPartNestedOut: nft part.
    """
    try:
        return crud.create_nft_part(db=db, nft_part=nft_part)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/nft-parts/{nft_part_id}", response_model=NftPartNestedOut)
def update_nft_part(
    nft_part_id: int, nft_part: NftPartUpdate, db: Session = Depends(get_db)
) -> NftPartNestedOut:
    """Route pour mettre ?? jour une partie de NFT.

    Args:
        nft_part_id (int): id nft part.
        nft_part (NftPartUpdate): nft part.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: la partie du NFT n'a pas ??t?? mise ?? jour.

    Returns:
        NftPartNestedOut: nft part.
    """
    try:
        return crud.update_nft_part(db=db, nft_part_id=nft_part_id, nft_part=nft_part)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/nft-parts/{nft_part_id}")
def delete_nft_part(nft_part_id: int, db: Session = Depends(get_db)) -> Response:
    """Route pour supprimer une partie de NFT.

    Args:
        nft_part_id (int): id nft part.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: la partie du NFT n'a pas ??t?? supprim??e.

    Returns:
        Response: response.
    """
    try:
        crud.delete_nft_part(db=db, nft_part_id=nft_part_id)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/nft-parts/code/{nft_part_code}")
def delete_nft_part_code(nft_part_code: int, db: Session = Depends(get_db)) -> Response:
    """Route pour supprimer une partie de NFT par code.

    Args:
        nft_part_code (int): code nft part.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: la partie du NFT n'a pas ??t?? supprim??e.

    Returns:
        Response: response.
    """
    try:
        crud.delete_nft_part_by_code(db=db, nft_part_code=nft_part_code)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/face-parts", response_model=List[FacePartNestedOut])
async def read_face_parts(db: Session = Depends(get_db)) -> List[FacePartNestedOut]:
    """Route pour r??cup??rer une liste de partie de visage.

    Args:
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Returns:
        List[FacePartNestedOut]: liste de partie de visage.
    """
    return crud.get_face_parts(db)


@router.get("/face-parts/{face_part_id}", response_model=FacePartNestedOut)
async def read_face_part(
    face_part_id: int, db: Session = Depends(get_db)
) -> FacePartNestedOut:
    """Route pour r??cup??rer une partie de visage.

    Args:
        face_part_id (int): id face part.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: la partie du visage n'existe pas.

    Returns:
        FacePartNestedOut: face part.
    """
    db_face_part = crud.get_face_part(db, face_part_id=face_part_id)
    if db_face_part is None:
        raise HTTPException(status_code=404, detail="Face part not found")
    return db_face_part


@router.get("/face-parts/code/{face_part_code}", response_model=FacePartNestedOut)
async def read_face_part_code(
    face_part_code: int, db: Session = Depends(get_db)
) -> FacePartNestedOut:
    """Route pour r??cup??rer une partie de visage par code.

    Args:
        face_part_code (int): code face part.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: la partie du visage n'existe pas.

    Returns:
        FacePartNestedOut: face part.
    """
    db_face_part_code = crud.get_face_part_by_code(db, face_part_code=face_part_code)
    if db_face_part_code is None:
        raise HTTPException(status_code=404, detail="Face part not found")
    return db_face_part_code


@router.post("/face-parts", response_model=FacePartNestedOut)
def create_face_part(
    face_part: FacePartCreate, db: Session = Depends(get_db)
) -> FacePartNestedOut:
    """Route pour cr??er une partie de visage.

    Args:
        face_part (FacePartCreate): face part.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: la partie du visage n'a pas ??t?? cr??e.

    Returns:
        FacePartNestedOut: face part.
    """
    try:
        return crud.create_face_part(db=db, face_part=face_part)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/face-parts/{face_part_id}", response_model=FacePartNestedOut)
def update_face_part(
    face_part_id: int, face_part: FacePartUpdate, db: Session = Depends(get_db)
) -> FacePartNestedOut:
    """Route pour mettre ?? jour une partie de visage.

    Args:
        face_part_id (int): id face part.
        face_part (FacePartUpdate): face part.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: la partie du visage n'a pas ??t?? mis ?? jour.

    Returns:
        FacePartNestedOut: face part.
    """
    try:
        return crud.update_face_part(
            db=db, face_part_id=face_part_id, face_part=face_part
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/face-parts/{face_part_id}")
def delete_face_part(face_part_id: int, db: Session = Depends(get_db)) -> Response:
    """Route pour supprimer une partie de visage.

    Args:
        face_part_id (int): id face part.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: la partie du visage n'a pas ??t?? supprim??e.

    Returns:
        Response: response.
    """
    try:
        crud.delete_face_part(db=db, face_part_id=face_part_id)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/face-parts/code/{face_part_code}")
def delete_face_part_code(
    face_part_code: int, db: Session = Depends(get_db)
) -> Response:
    """Route pour supprimer une partie de visage par code.

    Args:
        face_part_code (int): code face part.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: la partie du visage n'a pas ??t?? supprim??e.

    Returns:
        Response: response.
    """
    try:
        crud.delete_face_part_by_code(db=db, face_part_code=face_part_code)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/element-types", response_model=List[ElementTypeNestedOut])
async def read_element_types(
    db: Session = Depends(get_db),
) -> List[ElementTypeNestedOut]:
    """Route pour r??cup??rer une liste de types d'??l??ment.

    Args:
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Returns:
        List[ElementTypeNestedOut]: liste de element type.
    """
    return crud.get_element_types(db)


@router.get("/element-types/{element_type_id}", response_model=ElementTypeNestedOut)
async def read_element_type(
    element_type_id: int, db: Session = Depends(get_db)
) -> ElementTypeNestedOut:
    """Route pour r??cup??rer un type d'??l??ment.

    Args:
        element_type_id (int): id element type.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: le type d'??l??ment n'existe pas.

    Returns:
        ElementTypeNestedOut: element type.
    """
    db_element_type = crud.get_element_type(db, element_type_id=element_type_id)
    if db_element_type is None:
        raise HTTPException(status_code=404, detail=element_part_not_found)
    return db_element_type


@router.get(
    "/element-types/code/{element_type_code}", response_model=ElementTypeNestedOut
)
async def read_element_type_code(
    element_type_code: int, db: Session = Depends(get_db)
) -> ElementTypeNestedOut:
    """Route pour r??cup??rer un type d'??l??ment par code.

    Args:
        element_type_code (int): code element type.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: le type d'??l??ment n'existe pas.

    Returns:
        ElementTypeNestedOut: element type.
    """
    db_element_type_code = crud.get_element_type_by_code(
        db, element_type_code=element_type_code
    )
    if db_element_type_code is None:
        raise HTTPException(status_code=404, detail=element_part_not_found)
    return db_element_type_code


@router.post("/element-types", response_model=ElementTypeNestedOut)
def create_element_type(
    element_type: ElementTypeCreate, db: Session = Depends(get_db)
) -> ElementTypeNestedOut:
    """Route pour cr??er un type d'??l??ment.

    Args:
        element_type (ElementTypeCreate): element type.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: le type d'??l??ment n'a pas ??t?? cr??e.

    Returns:
        ElementTypeNestedOut: element type.
    """
    try:
        return crud.create_element_type(db=db, element_type=element_type)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/element-types/{element_type_id}", response_model=ElementTypeNestedOut)
def update_element_type(
    element_type_id: int, element_type: ElementTypeUpdate, db: Session = Depends(get_db)
) -> ElementTypeNestedOut:
    """Route pour mettre ?? jour un type d'??l??ment.

    Args:
        element_type_id (int): id element type.
        element_type (ElementTypeUpdate): element type.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: le type d'??l??ment n'a pas ??t?? cr??e.

    Returns:
        ElementTypeNestedOut: element type.
    """
    try:
        return crud.update_element_type(
            db=db, element_type_id=element_type_id, element_type=element_type
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/element-types/{element_type_id}")
def delete_element_type(
    element_type_id: int, db: Session = Depends(get_db)
) -> Response:
    """Route pour supprimer un type d'??l??ment.

    Args:
        element_type_id (int): id element type.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: le type d'??l??ment n'a pas ??t?? supprim??.

    Returns:
        Response: response.
    """
    try:
        crud.delete_element_type(db=db, element_type_id=element_type_id)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/element-types/code/{element_type_code}")
def delete_element_type_code(
    element_type_code: int, db: Session = Depends(get_db)
) -> Response:
    """Route pour supprimer un type d'??l??ment par code.

    Args:
        element_type_code (int): code element type.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: le type d'??l??ment n'a pas ??t?? supprim??.

    Returns:
        Response: response.
    """
    try:
        crud.delete_element_type_by_code(db=db, element_type_code=element_type_code)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/elements", response_model=List[ElementNestedOut])
async def read_elements(db: Session = Depends(get_db)) -> List[ElementNestedOut]:
    """Route pour r??cup??rer une liste d'??l??ments.

    Args:
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Returns:
        List[ElementNestedOut]: liste d'element.
    """
    return crud.get_elements(db)


@router.get("/elements/{element_id}", response_model=ElementNestedOut)
async def read_element(
    element_id: int, db: Session = Depends(get_db)
) -> ElementNestedOut:
    """Route pour r??cup??rer un ??l??ment.

    Args:
        element_id (int): id element.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: l'??l??ment n'existe pas.

    Returns:
        ElementNestedOut: element.
    """
    db_element = crud.get_element(db, element_id=element_id)
    if db_element is None:
        raise HTTPException(status_code=404, detail="Element not found")
    return db_element


@router.get("/elements/code/{element_code}", response_model=ElementNestedOut)
async def read_element_code(
    element_code: int, db: Session = Depends(get_db)
) -> ElementNestedOut:
    """Route pour r??cup??rer un ??l??ment par code.

    Args:
        element_code (int): code element.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: l'??l??ment n'existe pas.

    Returns:
        ElementNestedOut: element.
    """
    db_element_code = crud.get_element_by_code(db, element_code=element_code)
    if db_element_code is None:
        raise HTTPException(status_code=404, detail="Element not found")
    return db_element_code


@router.get("/elements/rarity/{rarity_id}", response_model=List[ElementNestedOut])
async def read_elements_by_rarity(
    rarity_id: int, db: Session = Depends(get_db)
) -> List[ElementNestedOut]:
    """Route pour r??cup??rer une liste d'??l??ment par raret??.

    Args:
        rarity_id (int): id rarity.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: la raret?? n'existe pas.

    Returns:
        List[ElementNestedOut]: liste d'element.
    """
    try:
        return crud.get_elements_by_rarity(db, rarity_id=rarity_id)
    except AttributeError:
        raise HTTPException(status_code=404, detail=rarity_part_not_found)


@router.get(
    "/elements/rarity/code/{rarity_code}", response_model=List[ElementNestedOut]
)
async def read_elements_by_rarity_code(
    rarity_code: int, db: Session = Depends(get_db)
) -> List[ElementNestedOut]:
    """Route pour r??cup??rer une liste d'??l??ment par raret?? par code.

    Args:
        rarity_code (int): code rarity.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: la raret?? n'existe pas.

    Returns:
        List[ElementNestedOut]: liste d'element.
    """
    try:
        return crud.get_elements_by_rarity_code(db, rarity_code=rarity_code)
    except AttributeError:
        raise HTTPException(status_code=404, detail=rarity_part_not_found)


@router.post("/elements", response_model=ElementNestedOut)
def create_element(
    code: int = Form(...),
    name: str = Form(...),
    nft_part_id: int = Form(...),
    type_id: int = Form(...),
    parent_id: int = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> ElementNestedOut:
    """Route pour cr??er un ??l??ment.

    Args:
        code (int, optional): code de l'??l??ment. D??faut ?? Form(...).
        name (str, optional): nom de l'??l??ment. D??faut ?? Form(...).
        nft_part_id (int, optional): id nft part. D??faut ?? Form(...).
        type_id (int, optional): id type. D??faut ?? Form(...).
        parent_id (int, optional): id parent. D??faut ?? Form(None).
        file (UploadFile, optional): image de l'??l??ment. D??faut ?? File(...).
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: l'??l??ment n'a pas ??t?? cr??e.

    Returns:
        ElementNestedOut: element.
    """
    try:
        return crud.create_element(
            db=db,
            code=code,
            name=name,
            nft_part_id=nft_part_id,
            type_id=type_id,
            parent_id=parent_id,
            file=file,
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/elements/{element_id}", response_model=ElementNestedOut)
def update_element(
    element_id: int,
    code: int = Form(...),
    name: str = Form(...),
    nft_part_id: int = Form(...),
    type_id: int = Form(...),
    parent_id: int = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> ElementNestedOut:
    """Route pour mettre ?? jour un ??l??ment.

    Args:
        element_id (int): id element.
        code (int, optional): code de l'??l??ment. D??faut ?? Form(...).
        name (str, optional): nom de l'??l??ment. D??faut ?? Form(...).
        nft_part_id (int, optional): id nft part. D??faut ?? Form(...).
        type_id (int, optional): id type. D??faut ?? Form(...).
        parent_id (int, optional): id parent. D??faut ?? Form(None).
        file (UploadFile, optional): image de l'??l??ment. D??faut ?? File(...).
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: l'??l??ment n'a pas ??t?? mis ?? jour.

    Returns:
        ElementNestedOut: element.
    """
    try:
        return crud.update_element(
            db=db,
            element_id=element_id,
            code=code,
            name=name,
            nft_part_id=nft_part_id,
            type_id=type_id,
            parent_id=parent_id,
            file=file,
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/elements/{element_id}")
def delete_element(element_id: int, db: Session = Depends(get_db)) -> Response:
    """Route pour supprimer un ??l??ment.

    Args:
        element_id (int): id element.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: l'??l??ment n'a pas ??t?? supprim??.

    Returns:
        Response: response.
    """
    try:
        crud.delete_element(db=db, element_id=element_id)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/elements/code/{element_code}")
def delete_element_code(element_code: int, db: Session = Depends(get_db)) -> Response:
    """Route pour supprimer un ??l??ment par code.

    Args:
        element_code (int): code element.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: l'??l??ment n'a pas ??t?? supprim??.

    Returns:
        Response: response.
    """
    try:
        crud.delete_element_by_code(db=db, element_code=element_code)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/elements/type/{element_type_id}", response_model=List[ElementOut])
async def read_elements_by_type(
    element_type_id: int, db: Session = Depends(get_db)
) -> List[ElementOut]:
    """Route pour r??cup??rer une liste d'??l??ments par type.

    Args:
        element_type_id (int): id element type.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: le type d'??l??ment n'existe pas.

    Returns:
        List[ElementOut]: liste d'element.
    """
    try:
        return crud.get_elements_by_type(db, element_type_id=element_type_id)
    except AttributeError:
        raise HTTPException(status_code=404, detail=element_part_not_found)


@router.get("/elements/type/code/{element_type_code}", response_model=List[ElementOut])
async def read_elements_by_type_code(
    element_type_code: int, db: Session = Depends(get_db)
) -> List[ElementOut]:
    """Route pour r??cup??rer une liste d'??l??ments par type par code.

    Args:
        element_type_code (int): code element type.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: le type d'??l??ment n'existe pas.


    Returns:
        List[ElementOut]: liste d'element.
    """
    try:
        return crud.get_elements_by_type_code(db, element_type_code=element_type_code)
    except AttributeError:
        raise HTTPException(status_code=404, detail=element_part_not_found)


@router.get("/elements/nft-part/{nft_part_id}", response_model=List[ElementOut])
async def read_elements_by_nft_part(
    nft_part_id: int, db: Session = Depends(get_db)
) -> List[ElementOut]:
    """Route pour r??cup??rer une liste d'??l??ments par partie du NFT.

    Args:
        nft_part_id (int): id nft part.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: la partie du NFT n'existe pas.

    Returns:
        List[ElementOut]: liste d'element.
    """
    try:
        return crud.get_elements_by_nft_part(db, nft_part_id=nft_part_id)
    except AttributeError:
        raise HTTPException(status_code=404, detail=nft_part_not_found)


@router.get("/elements/nft-part/code/{nft_part_code}", response_model=List[ElementOut])
async def read_elements_by_nft_part_code(
    nft_part_code: int, db: Session = Depends(get_db)
) -> List[ElementOut]:
    """Route pour r??cup??rer une liste d'??l??ments par partie du NFT par code.

    Args:
        nft_part_code (int): code nft part.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: la partie du NFT n'existe pas.

    Returns:
        List[ElementOut]: liste d'element.
    """
    try:
        return crud.get_elements_by_nft_part_code(db, nft_part_code=nft_part_code)
    except AttributeError:
        raise HTTPException(status_code=404, detail=nft_part_not_found)


@router.get("/colors", response_model=List[ColorNestedOut])
async def read_colors(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[ColorNestedOut]:
    """Route pour r??cup??rer une liste de couleurs.

    Args:
        skip (int, optional): skip. D??faut ?? 0.
        limit (int, optional): limit. D??faut ?? 100.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Returns:
        List[ColorNestedOut]: liste de color.
    """
    return crud.get_colors(db, skip=skip, limit=limit)


@router.get("/colors/{color_id}", response_model=ColorNestedOut)
async def read_color(color_id: int, db: Session = Depends(get_db)) -> ColorNestedOut:
    """Route pour r??cup??rer une couleur.

    Args:
        color_id (int): id color.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: la couleur n'existe pas.

    Returns:
        ColorNestedOut: color.
    """
    db_color = crud.get_color(db, color_id=color_id)
    if db_color is None:
        raise HTTPException(status_code=404, detail="Color not found")
    return db_color


@router.get("/colors/rarity/{rarity_id}", response_model=List[ColorNestedOut])
async def read_colors_by_rarity(
    rarity_id: int, db: Session = Depends(get_db)
) -> List[ColorNestedOut]:
    """Route pour r??cup??rer une liste de couleur par raret??.

    Args:
        rarity_id (int): id rarity.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: la raret?? n'existe pas.

    Returns:
        List[ColorNestedOut]: liste de color.
    """
    try:
        return crud.get_colors_by_rarity(db, rarity_id=rarity_id)
    except AttributeError:
        raise HTTPException(status_code=404, detail=rarity_part_not_found)


@router.get("/colors/rarity/code/{rarity_code}", response_model=List[ColorNestedOut])
async def read_colors_by_rarity_code(
    rarity_code: int, db: Session = Depends(get_db)
) -> List[ColorNestedOut]:
    """Route pour r??cup??rer une liste de couleur par raret?? par code.

    Args:
        rarity_code (int): code rarity.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: la raret?? n'existe pas.

    Returns:
        List[ColorNestedOut]: liste de color.
    """
    try:
        return crud.get_colors_by_rarity_code(db, rarity_code=rarity_code)
    except AttributeError:
        raise HTTPException(status_code=404, detail=rarity_part_not_found)


@router.post("/colors", response_model=ColorNestedOut)
def create_color(color: ColorCreate, db: Session = Depends(get_db)) -> ColorNestedOut:
    """Route pour cr??er une couleur.

    Args:
        color (ColorCreate): color.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: la couleur n'a pas ??t?? cr??e.

    Returns:
        ColorNestedOut: color.
    """
    try:
        return crud.create_color(db=db, color=color)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/colors/{color_id}", response_model=ColorNestedOut)
def update_color(
    color_id: int, color: ColorUpdate, db: Session = Depends(get_db)
) -> ColorNestedOut:
    """Route pour mettre ?? jour une couleur.

    Args:
        color_id (int): id color.
        color (ColorUpdate): color.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: la couleur n'a pas ??t?? mise ?? jour.

    Returns:
        ColorNestedOut: color.
    """
    try:
        return crud.update_color(db=db, color_id=color_id, color=color)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/colors/{color_id}")
def delete_color(color_id: int, db: Session = Depends(get_db)) -> Response:
    """Route pour supprimer une couleur.

    Args:
        color_id (int): _description_
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: _description_

    Returns:
        Response: response.
    """
    try:
        crud.delete_color(db=db, color_id=color_id)
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/colors/nft-part/{nft_part_id}", response_model=List[ColorOut])
async def read_colors_by_nft_part(
    nft_part_id: int, db: Session = Depends(get_db)
) -> List[ColorOut]:
    """Route pour r??cup??rer une liste de couleur par partie de NFT.

    Args:
        nft_part_id (int): id nft part.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: la partie du NFT n'existe pas.

    Returns:
        List[ColorOut]: liste de color.
    """
    try:
        return crud.get_colors_by_nft_part(db, nft_part_id=nft_part_id)
    except AttributeError:
        raise HTTPException(status_code=404, detail=nft_part_not_found)


@router.get("/colors/nft-part/code/{nft_part_code}", response_model=List[ColorOut])
async def read_colors_by_nft_part_code(
    nft_part_code: int, db: Session = Depends(get_db)
) -> List[ColorOut]:
    """Route pour r??cup??rer une liste de couleur par partie de NFT par code.

    Args:
        nft_part_code (int): code nft part.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: la partie du NFT n'existe pas.

    Returns:
        List[ColorOut]: liste de color.
    """
    try:
        return crud.get_colors_by_nft_part_code(db, nft_part_code=nft_part_code)
    except AttributeError:
        raise HTTPException(status_code=404, detail=nft_part_not_found)


@router.post("/dependent-face-parts-colors")
def create_dependent_face_parts_colors(
    dependent_face_parts_colors: List[DependentFacePartColorCreate],
    db: Session = Depends(get_db),
) -> Response:
    """Route pour cr??er les d??pendances entre une partie d'un visage et une couleur.

    Args:
        dependent_face_parts_colors (List[DependentFacePartColorCreate]): d??pendances.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: les d??pendances n'ont pas ??t?? cr??es.

    Returns:
        Response: response.
    """
    try:
        crud.create_dependent_face_parts_colors(
            db=db, dependent_face_parts_colors=dependent_face_parts_colors
        )
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/dependent-face-parts-colors")
def delete_dependent_face_parts_colors(
    dependent_face_parts_colors: List[DependentFacePartColorDelete],
    db: Session = Depends(get_db),
) -> Response:
    """Route pour supprimer les d??pendances entre une partie d'un visage et une couleur.

    Args:
        dependent_face_parts_colors (List[DependentFacePartColorDelete]): d??pendances.
        db (Session, optional): session de la base de donn??e. D??faut ?? Depends(get_db).

    Raises:
        HTTPException: les d??pendances n'ont pas ??t?? supprim??es.

    Returns:
        Response: response.
    """
    try:
        crud.delete_dependent_face_parts_colors(
            db=db, dependent_face_parts_colors=dependent_face_parts_colors
        )
        return Response(status_code=204)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
