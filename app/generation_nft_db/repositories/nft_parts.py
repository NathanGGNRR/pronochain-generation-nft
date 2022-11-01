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

File: app/generation_nft_db/repositories/nft_parts.py
"""
from typing import List

from fastapi import UploadFile
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.exceptions import PronochainException
from app.generation_nft.libraries.storage.storage import Storage
from app.generation_nft_db.models import nft_parts as model_nft
from app.generation_nft_db.models import rarities as model_rarities
from app.generation_nft_db.schemas import nft_parts as schema_nft
from app.settings import settings

nft_storage = Storage()


def get_nft_part(
    db: Session, nft_part_id: int, return_one: bool = True
) -> schema_nft.NftPartNestedOut:
    """Récupère une partie d'un NFT.

    Args:
        db (Session): session de la base de donnée.
        nft_part_id (int): id nft part.
        return_one (bool, optional): retourne une seule ? Défaut à True.

    Returns:
        schema_nft.NftPartNestedOut: nft part.
    """
    nft_part_query = db.query(model_nft.NftPart).filter(
        model_nft.NftPart.id == nft_part_id
    )
    return nft_part_query.first() if return_one else nft_part_query


def get_nft_part_by_code(
    db: Session, nft_part_code: int, return_one: bool = True
) -> schema_nft.NftPartNestedOut:
    """Récupère une partie d'un NFT par code.

    Args:
        db (Session): session de la base de donnée.
        nft_part_code (int): code nft part.
        return_one (bool, optional): retourne une seule ? Défaut à True.

    Returns:
        schema_nft.NftPartNestedOut: nft part.
    """
    nft_part_code_query = db.query(model_nft.NftPart).filter(
        model_nft.NftPart.code == nft_part_code
    )
    return nft_part_code_query.first() if return_one else nft_part_code_query


def get_nft_parts(db: Session) -> List[schema_nft.NftPartNestedOut]:
    """Récupère une liste de parties de NFT.

    Args:
        db (Session): session de la base de donnée.

    Returns:
        List[schema_nft.NftPartNestedOut]: liste de nft part.
    """
    return db.query(model_nft.NftPart).all()


def create_nft_part(
    db: Session, nft_part: schema_nft.NftPartCreate
) -> schema_nft.NftPartNestedOut:
    """Crée une partie d'un NFT?

    Args:
        db (Session): session de la base de donnée.
        nft_part (schema_nft.NftPartCreate): nft part.

    Raises:
        PronochainException: la partie du NFT n'a pas été crée.

    Returns:
        schema_nft.NftPartNestedOut: nft part.
    """
    try:
        db_nft_part = model_nft.NftPart(**nft_part.dict())
        db.add(db_nft_part)
        db.commit()
        db.refresh(db_nft_part)
        return db_nft_part
    except IntegrityError as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def update_nft_part(
    db: Session, nft_part_id: int, nft_part: schema_nft.NftPartUpdate
) -> schema_nft.NftPartNestedOut:
    """Mettre à jour une partie d'un NFT.

    Args:
        db (Session): session de la base de donnée.
        nft_part_id (int): id nft part.
        nft_part (schema_nft.NftPartUpdate): nft part.

    Raises:
        PronochainException: la partie du NFT n'a pas été mise à jour.

    Returns:
        schema_nft.NftPartNestedOut: nft part.
    """
    try:
        nft_part = nft_part.dict()
        db_nft_part = get_nft_part(db, nft_part_id=nft_part_id, return_one=False)
        db_nft_part.update(nft_part, synchronize_session=False)
        db.commit()
        db.refresh(db_nft_part.first())
        return db_nft_part.first()
    except Exception as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def delete_nft_part(db: Session, nft_part_id: int):
    """Supprime une partie d'un NFT.

    Args:
        db (Session): session de la base de donnée.
        nft_part_id (int): id nft part.

    Raises:
        PronochainException: la partie du NFT n'a pas été supprimée.
    """
    db_nft_part = get_nft_part(db, nft_part_id=nft_part_id, return_one=False)
    if db_nft_part.first() is not None:
        db_nft_part.delete()
        db.commit()
    else:
        raise PronochainException("Nft part not found")


def delete_nft_part_by_code(db: Session, nft_part_code: int):
    """Supprime une partie d'un NFT par code.

    Args:
        db (Session): session de la base de donnée.
        nft_part_code (int): code nft part.

    Raises:
        PronochainException: la partie du NFT n'a pas été supprimée.
    """
    db_nft_part = get_nft_part_by_code(
        db, nft_part_code=nft_part_code, return_one=False
    )
    if db_nft_part.first() is not None:
        db_nft_part.delete()
        db.commit()
    else:
        raise PronochainException("Nft part not found")


def get_face_part(
    db: Session, face_part_id: int, return_one: bool = True
) -> schema_nft.FacePartNestedOut:
    """Récupère une partie d'un visage.

    Args:
        db (Session): session de la base de donnée.
        face_part_id (int): id face part.
        return_one (bool, optional): retourne une seule ? Défaut à True.

    Returns:
        schema_nft.FacePartNestedOut: face part.
    """
    face_part_query = (
        db.query(model_nft.FacePart)
        .options(joinedload(model_nft.FacePart.face_parts_colors))
        .filter(model_nft.FacePart.id == face_part_id)
    )
    return face_part_query.first() if return_one else face_part_query


def get_face_part_by_code(
    db: Session, face_part_code: int, return_one: bool = True
) -> schema_nft.FacePartNestedOut:
    """Récupère une partie d'un visage par code.

    Args:
        db (Session): session de la base de donnée.
        face_part_code (int): code face part.
        return_one (bool, optional): retourne une seule ? Défaut à True.

    Returns:
        schema_nft.FacePartNestedOut: face part.
    """
    face_part_code_query = (
        db.query(model_nft.FacePart)
        .options(joinedload(model_nft.FacePart.face_parts_colors))
        .filter(model_nft.FacePart.code == face_part_code)
    )
    return face_part_code_query.first() if return_one else face_part_code_query


def get_face_parts(db: Session) -> List[schema_nft.FacePartNestedOut]:
    """Récupère une liste de parties de visage.

    Args:
        db (Session): session de la base de donnée.

    Returns:
        List[schema_nft.FacePartNestedOut]: liste de face part.
    """
    return (
        db.query(model_nft.FacePart)
        .options(joinedload(model_nft.FacePart.face_parts_colors))
        .all()
    )


def create_face_part(
    db: Session, face_part: schema_nft.FacePartCreate
) -> schema_nft.FacePartNestedOut:
    """Crée une partie de visage.

    Args:
        db (Session): session de la base de donnée.
        face_part (schema_nft.FacePartCreate): face part.

    Raises:
        PronochainException: la partie de visage n'a pas été crée.

    Returns:
        schema_nft.FacePartNestedOut: face part.
    """
    try:
        face_part_dict = face_part.dict()
        face_parts_colors = face_part_dict.pop("face_parts_colors")

        db_face_part = model_nft.FacePart(**face_part_dict)
        db.add(db_face_part)
        db.commit()
        db.refresh(db_face_part)

        for face_part_color in face_parts_colors:
            face_part_color["face_part_id"] = db_face_part.id
            db_face_part_color = model_nft.FacePartColor(**face_part_color)
            db.add(db_face_part_color)
            db.commit()
            db.refresh(db_face_part_color)

        return db_face_part
    except IntegrityError as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def update_face_part(
    db: Session, face_part_id: int, face_part: schema_nft.FacePartUpdate
) -> schema_nft.FacePartNestedOut:
    """Mettre à jour une partie de visage.

    Args:
        db (Session): session de la base de donnée.
        face_part_id (int): id face part.
        face_part (schema_nft.FacePartUpdate): face part.

    Raises:
        PronochainException: la partie de visage n'a pas été mise à jour.

    Returns:
        schema_nft.FacePartNestedOut: face part.
    """
    try:
        face_part = face_part.dict()
        face_parts_colors = face_part.pop("face_parts_colors")

        db_face_part = get_face_part(db, face_part_id=face_part_id, return_one=False)
        db_face_part_first = db_face_part.first()

        face_parts_colors_ids = [
            face_part_color.id
            for face_part_color in db_face_part_first.face_parts_colors
        ]
        db.query(model_nft.FacePartColor).filter(
            model_nft.FacePartColor.id.in_(face_parts_colors_ids)
        ).delete()
        db.commit()

        db_face_part.update(face_part, synchronize_session=False)

        db.commit()
        db.refresh(db_face_part_first)

        for face_part_color in face_parts_colors:
            face_part_color["face_part_id"] = db_face_part_first.id
            db_face_part_color = model_nft.FacePartColor(**face_part_color)
            db.add(db_face_part_color)
            db.commit()
            db.refresh(db_face_part_color)

        return db_face_part.first()
    except Exception as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def delete_face_part(db: Session, face_part_id: int):
    """Supprime une partie de visage.

    Args:
        db (Session): session de la base de donnée.
        face_part_id (int): id face part.

    Raises:
        PronochainException: la partie de visage n'a pas été supprimée.
    """
    db_face_part = get_face_part(db, face_part_id=face_part_id, return_one=False)
    if db_face_part.first() is not None:
        db_face_part.delete()
        db.commit()
    else:
        raise PronochainException("Face part not found")


def delete_face_part_by_code(db: Session, face_part_code: int):
    """Supprime une partie de visage par code.

    Args:
        db (Session): session de la base de donnée.
        face_part_code (int): code face part.

    Raises:
        PronochainException: la partie de visage n'a pas été supprimée.
    """
    db_face_part = get_face_part_by_code(
        db, face_part_code=face_part_code, return_one=False
    )
    if db_face_part.first() is not None:
        db_face_part.delete()
        db.commit()
    else:
        raise PronochainException("Face part not found")


def get_element_type(
    db: Session, element_type_id: int, return_one: bool = True
) -> schema_nft.ElementTypeNestedOut:
    """Récupère un type d'élément.

    Args:
        db (Session): session de la base de donnée.
        element_type_id (int): id element type.
        return_one (bool, optional): retourne un seul ? Défaut à True.

    Returns:
        schema_nft.ElementTypeNestedOut: element type.
    """
    element_type_query = db.query(model_nft.ElementType).filter(
        model_nft.ElementType.id == element_type_id
    )
    return element_type_query.first() if return_one else element_type_query


def get_element_type_by_code(
    db: Session, element_type_code: int, return_one: bool = True
) -> schema_nft.ElementTypeNestedOut:
    """Récupère un type d'élément par code.

    Args:
        db (Session): session de la base de donnée.
        element_type_code (int): code element type.
        return_one (bool, optional): retourne un seul ? Défaut à True.

    Returns:
        schema_nft.ElementTypeNestedOut: element type.
    """
    element_type_code_query = db.query(model_nft.ElementType).filter(
        model_nft.ElementType.code == element_type_code
    )
    return element_type_code_query.first() if return_one else element_type_code_query


def get_element_types(db: Session) -> List[schema_nft.ElementTypeNestedOut]:
    """Récupère une liste de type d'élements.

    Args:
        db (Session): session de la base de donnée.

    Returns:
        List[schema_nft.ElementTypeNestedOut]: liste de element type.
    """
    return db.query(model_nft.ElementType).all()


def create_element_type(
    db: Session, element_type: schema_nft.ElementTypeCreate
) -> schema_nft.ElementTypeNestedOut:
    """Crée un type d'élément.

    Args:
        db (Session): session de la base de donnée.
        element_type (schema_nft.ElementTypeCreate): element type.

    Raises:
        PronochainException: le type d'élément n'a pas été crée.

    Returns:
        schema_nft.ElementTypeNestedOut: element type.
    """
    try:
        db_element_type = model_nft.ElementType(**element_type.dict())
        db.add(db_element_type)
        db.commit()
        db.refresh(db_element_type)
        return db_element_type
    except IntegrityError as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def update_element_type(
    db: Session, element_type_id: int, element_type: schema_nft.ElementTypeUpdate
) -> schema_nft.ElementTypeNestedOut:
    """Mettre à jour un type d'élément.

    Args:
        db (Session): session de la base de donnée.
        element_type_id (int): id element type.
        element_type (schema_nft.ElementTypeUpdate): element type.

    Raises:
        PronochainException: le type d'élément n'a pas été mis à jour.

    Returns:
        schema_nft.ElementTypeNestedOut: element type.
    """
    try:
        element_type = element_type.dict()
        db_element_type = get_element_type(
            db, element_type_id=element_type_id, return_one=False
        )
        db_element_type.update(element_type, synchronize_session=False)
        db.commit()
        db.refresh(db_element_type.first())
        return db_element_type.first()
    except Exception as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def delete_element_type(db: Session, element_type_id: int):
    """Supprime un type d'élément.

    Args:
        db (Session): session de la base de donnée.
        element_type_id (int): id element type.

    Raises:
        PronochainException: le type d'élément n'a pas été supprimé.
    """
    db_element_type = get_element_type(
        db, element_type_id=element_type_id, return_one=False
    )
    if db_element_type.first() is not None:
        db_element_type.delete()
        db.commit()
    else:
        raise PronochainException("Element type not found")


def delete_element_type_by_code(db: Session, element_type_code: int):
    """Supprime un type d'élément par code.

    Args:
        db (Session): session de la base de donnée.
        element_type_code (int): code element type.

    Raises:
        PronochainException: le type d'élément n'a pas été supprimé.
    """
    db_element_type = get_element_type_by_code(
        db, element_type_code=element_type_code, return_one=False
    )
    if db_element_type.first() is not None:
        db_element_type.delete()
        db.commit()
    else:
        raise PronochainException("Element tType not found")


def get_element(
    db: Session, element_id: int, return_one: bool = True
) -> schema_nft.ElementNestedOut:
    """Récupère un élément.

    Args:
        db (Session): session de la base de donnée.
        element_id (int): id element.
        return_one (bool, optional): retourne un seul ? Défaut à True.

    Returns:
        schema_nft.ElementNestedOut: element.
    """
    element_query = db.query(model_nft.Element).filter(
        model_nft.Element.id == element_id
    )
    return element_query.first() if return_one else element_query


def get_element_by_code(
    db: Session, element_code: int, return_one: bool = True
) -> schema_nft.ElementNestedOut:
    """Récupère un élément par code.

    Args:
        db (Session): session de la base de donnée.
        element_code (int): code element.
        return_one (bool, optional): retourne un seul ? Défaut à True.

    Returns:
        schema_nft.ElementNestedOut: element.
    """
    element_code_query = db.query(model_nft.Element).filter(
        model_nft.Element.code == element_code
    )
    return element_code_query.first() if return_one else element_code_query


def get_elements_by_rarity(
    db: Session, rarity_id: int
) -> List[schema_nft.ElementNestedOut]:
    """Récupère une liste d'éléments par rareté.

    Args:
        db (Session): session de la base de donnée.
        rarity_id (int): id rarity.

    Raises:
        AttributeError: la rareté n'existe pas.

    Returns:
        List[schema_nft.ElementNestedOut]: liste d'element.
    """
    try:
        return (
            db.query(model_rarities.Rarity)
            .filter(model_rarities.Rarity.id == rarity_id)
            .first()
            .elements
        )
    except Exception:
        raise AttributeError


def get_elements_by_rarity_code(
    db: Session, rarity_code: int
) -> List[schema_nft.ElementNestedOut]:
    """Récupère une liste d'éléments par rareté par code.

    Args:
        db (Session): session de la base de donnée.
        rarity_code (int): code rarity.

    Raises:
        AttributeError: la rareté n'existe pas.

    Returns:
        List[schema_nft.ElementNestedOut]: liste d'element.
    """
    try:
        return (
            db.query(model_rarities.Rarity)
            .filter(model_rarities.Rarity.code == rarity_code)
            .first()
            .elements
        )
    except Exception:
        raise AttributeError


def get_elements(db: Session) -> List[schema_nft.ElementNestedOut]:
    """Récupère une liste d'éléments.

    Args:
        db (Session): session de la base de donnée.

    Returns:
        List[schema_nft.ElementNestedOut]: liste d'element.
    """
    return db.query(model_nft.Element).all()


def create_element(
    db: Session,
    code: int,
    name: str,
    nft_part_id: int,
    type_id: int,
    parent_id: int,
    file: UploadFile,
) -> schema_nft.ElementNestedOut:
    """Crée un élément.

    Args:
        db (Session): session de la base de donnée.
        code (int): code de l'élément.
        name (str): nom de l'élément.
        nft_part_id (int): id nft part.
        type_id (int): id type.
        parent_id (int): id parent.
        file (UploadFile): photo de l'élément.

    Raises:
        PronochainException: l'élément n'a pas été crée.

    Returns:
        schema_nft.ElementNestedOut: element.
    """
    try:
        if settings.STORE_NFT_PART:
            response = nft_storage.add(file.file)
            db_element = model_nft.Element(
                code=code,
                name=name,
                nft_part_id=nft_part_id,
                type_id=type_id,
                parent_id=parent_id,
                cid=response.value.cid,
                filename=file.filename,
            )
        else:
            db_element = model_nft.Element(
                code=code,
                name=name,
                nft_part_id=nft_part_id,
                type_id=type_id,
                parent_id=parent_id,
                cid=None,
                filename=None,
            )
        db.add(db_element)
        db.commit()
        db.refresh(db_element)
        return db_element
    except IntegrityError as e:
        nft_storage.delete(response.value.cid)
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def update_element(
    db: Session,
    element_id: int,
    code: int,
    name: str,
    nft_part_id: int,
    type_id: int,
    parent_id: int,
    file: UploadFile,
) -> schema_nft.ElementNestedOut:
    """Mettre à jour un élément.

    Args:
        db (Session): session de la base de donnée.
        element_id (int): id element.
        code (int): code de l'élément.
        name (str): nom de l'élément.
        nft_part_id (int): id nft part.
        type_id (int): id type.
        parent_id (int): id parent.
        file (UploadFile): photo de l'élément.

    Raises:
        PronochainException: NFT n'a pas été trouvé.
        PronochainException: l'élément n'a pas été mis à jour.

    Returns:
        schema_nft.ElementNestedOut: element.
    """
    try:
        db_element = get_element(db, element_id=element_id, return_one=False)
        element = {
            "code": code,
            "name": name,
            "nft_part_id": nft_part_id,
            "type_id": type_id,
            "parent_id": parent_id,
            "cid": None,
            "filename": None,
        }

        if settings.STORE_NFT_PART:
            try:
                nft_storage.delete(db_element.first().cid)
            except Exception as e:
                if str(e) != "NFT not found":
                    raise PronochainException(str(e.orig).split("DETAIL: ")[-1])
            response = nft_storage.add(file.file)
            element["cid"] = response.value.cid
            element["filename"] = file.filename

        db_element.update(element, synchronize_session=False)
        db.commit()
        db.refresh(db_element.first())
        return db_element.first()
    except Exception as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def delete_element(db: Session, element_id: int):
    """Supprime un élément.

    Args:
        db (Session): session de la base de donnée.
        element_id (int): id element.

    Raises:
        PronochainException: l'élément n'a pas été supprimé.
    """
    db_element = get_element(db, element_id=element_id, return_one=False)
    if db_element.first() is not None:
        if settings.STORE_NFT_PART:
            nft_storage.delete(db_element.first().cid)
        db_element.delete()
        db.commit()
    else:
        raise PronochainException("Element not found")


def delete_element_by_code(db: Session, element_code: int):
    """Supprime un élément par code.

    Args:
        db (Session): session de la base de donnée.
        element_code (int): code element.

    Raises:
        PronochainException: l'élément n'a pas été supprimé.
    """
    db_element = get_element_by_code(db, element_code=element_code, return_one=False)
    if db_element.first() is not None:
        if settings.STORE_NFT_PART:
            nft_storage.delete(db_element.first().cid)
        db_element.delete()
        db.commit()
    else:
        raise PronochainException("Element not found")


def get_elements_by_type(
    db: Session, element_type_id: int
) -> list[schema_nft.ElementOut]:
    """Récupère une liste d'éléments par type.

    Args:
        db (Session): session de la base de donnée.
        element_type_id (int): id element type.

    Raises:
        AttributeError: le type d'élément n'existe pas.

    Returns:
        list[schema_nft.ElementOut]: liste d'element.
    """
    try:
        type_elements = (
            db.query(model_nft.ElementType)
            .filter(model_nft.ElementType.id == element_type_id)
            .first()
            .elements
        )
    except Exception:
        raise AttributeError
    if any(type_elements):
        return type_elements
    return []


def get_elements_by_type_code(
    db: Session, element_type_code: int
) -> list[schema_nft.ElementOut]:
    """Récupère une liste d'éléments par type par code.

    Args:
        db (Session): session de la base de donnée.
        element_type_code (int): code element type.

    Raises:
        AttributeError: le type d'élément n'existe pas.

    Returns:
        list[schema_nft.ElementOut]: liste d'element.
    """
    try:
        type_elements_code = (
            db.query(model_nft.ElementType)
            .filter(model_nft.ElementType.code == element_type_code)
            .first()
            .elements
        )
    except Exception:
        raise AttributeError
    if any(type_elements_code):
        return type_elements_code
    return []


def get_elements_by_nft_part(
    db: Session, nft_part_id: int
) -> list[schema_nft.ElementOut]:
    """Récupère une liste d'éléments par partie de NFT.

    Args:
        db (Session): session de la base de donnée.
        nft_part_id (int): id nft part.

    Raises:
        AttributeError: la partie du NFT n'existe pas.

    Returns:
        list[schema_nft.ElementOut]: liste d'element.
    """
    try:
        nft_part_elements = (
            db.query(model_nft.NftPart)
            .filter(model_nft.NftPart.id == nft_part_id)
            .first()
            .elements
        )
    except Exception:
        raise AttributeError
    if any(nft_part_elements):
        return nft_part_elements
    return []


def get_elements_by_nft_part_code(
    db: Session, nft_part_code: int
) -> list[schema_nft.ElementOut]:
    """Récupère une liste d'éléments par partie de NFT par code.

    Args:
        db (Session): session de la base de donnée.
        nft_part_code (int): code nft part.

    Raises:
        AttributeError: la partie du NFT n'existe pas.

    Returns:
        list[schema_nft.ElementOut]: liste d'element.
    """
    try:
        nft_part_elements_code = (
            db.query(model_nft.NftPart)
            .filter(model_nft.NftPart.code == nft_part_code)
            .first()
            .elements
        )
    except Exception:
        raise AttributeError
    if any(nft_part_elements_code):
        return nft_part_elements_code
    return []


def get_color(
    db: Session, color_id: int, return_one: bool = True
) -> schema_nft.ColorNestedOut:
    """Récupère une couleur.

    Args:
        db (Session): session de la base de donnée.
        color_id (int): id color.
        return_one (bool, optional): retourne une seule ? Défaut à True.

    Returns:
        schema_nft.ColorNestedOut: color.
    """
    color_query = db.query(model_nft.Color).filter(model_nft.Color.id == color_id)
    return color_query.first() if return_one else color_query


def get_colors_by_rarity(
    db: Session, rarity_id: int
) -> List[schema_nft.ColorNestedOut]:
    """Récupère une liste de couleurs par rareté.

    Args:
        db (Session): session de la base de donnée.
        rarity_id (int): id rarity.

    Raises:
        AttributeError: la rareté n'existe pas.

    Returns:
        List[schema_nft.ColorNestedOut]: liste de color.
    """
    try:
        return (
            db.query(model_rarities.Rarity)
            .filter(model_rarities.Rarity.id == rarity_id)
            .first()
            .colors
        )
    except Exception:
        raise AttributeError


def get_colors_by_rarity_code(
    db: Session, rarity_code: int
) -> List[schema_nft.ColorNestedOut]:
    """Récupère une liste de couleurs par rareté par code.

    Args:
        db (Session): session de la base de donnée.
        rarity_code (int): code rarity.

    Raises:
        AttributeError: la rareté n'existe pas.

    Returns:
        List[schema_nft.ColorNestedOut]: liste de color.
    """
    try:
        return (
            db.query(model_rarities.Rarity)
            .filter(model_rarities.Rarity.code == rarity_code)
            .first()
            .colors
        )
    except Exception:
        raise AttributeError


def get_colors(
    db: Session, skip: int = 0, limit: int = 100
) -> List[schema_nft.ColorNestedOut]:
    """Récupère une liste de couleurs.

    Args:
        db (Session): session de la base de donnée.
        skip (int, optional): skip. Défaut à 0.
        limit (int, optional): limit. Défaut à 100.

    Returns:
        List[schema_nft.ColorNestedOut]: liste de color.
    """
    return db.query(model_nft.Color).offset(skip).limit(limit).all()


def create_color(
    db: Session, color: schema_nft.ColorCreate
) -> schema_nft.ColorNestedOut:
    """Crée une couleur.

    Args:
        db (Session): session de la base de donnée.
        color (schema_nft.ColorCreate): color.

    Raises:
        PronochainException: la couleur n'a pas été crée.

    Returns:
        schema_nft.ColorNestedOut: color
    """
    try:
        db_color = model_nft.Color(**color.dict())
        db.add(db_color)
        db.commit()
        db.refresh(db_color)
        return db_color
    except IntegrityError as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def update_color(
    db: Session, color_id: int, color: schema_nft.ColorUpdate
) -> schema_nft.ColorNestedOut:
    """Mettre à jour une couleur.

    Args:
        db (Session): session de la base de donnée.
        color_id (int): id color.
        color (schema_nft.ColorUpdate): color.

    Raises:
        PronochainException: la couleur n'a pas été mise à jour.

    Returns:
        schema_nft.ColorNestedOut: color.
    """
    try:
        color = color.dict()
        db_color = get_color(db, color_id=color_id, return_one=False)
        db_color.update(color, synchronize_session=False)
        db.commit()
        db.refresh(db_color.first())
        return db_color.first()
    except Exception as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def delete_color(db: Session, color_id: int):
    """Supprime une couleur.

    Args:
        db (Session): session de la base de donnée.
        color_id (int): id color.

    Raises:
        PronochainException: la couleur n'a pas été supprimée.
    """
    db_color = get_color(db, color_id=color_id, return_one=False)
    if db_color.first() is not None:
        db_color.delete()
        db.commit()
    else:
        raise PronochainException("Color not found")


def get_colors_by_nft_part(db: Session, nft_part_id: int) -> list[schema_nft.ColorOut]:
    """Récupère une liste de couleurs par partie du NFT.

    Args:
        db (Session): session de la base de donnée.
        nft_part_id (int): id nft part.

    Raises:
        AttributeError: la partie du NFT n'existe pas.

    Returns:
        list[schema_nft.ColorOut]: liste de color.
    """
    try:
        nft_part_colors = (
            db.query(model_nft.NftPart)
            .filter(model_nft.NftPart.id == nft_part_id)
            .first()
            .colors
        )
    except Exception:
        raise AttributeError
    if any(nft_part_colors):
        return nft_part_colors
    return []


def get_colors_by_nft_part_code(
    db: Session, nft_part_code: int
) -> list[schema_nft.ColorOut]:
    """Récupère une liste de couleurs par partie du NFT par code.

    Args:
        db (Session): session de la base de donnée.
        nft_part_code (int): code nft part.

    Raises:
        AttributeError: la partie du NFT n'existe pas.

    Returns:
        list[schema_nft.ColorOut]: liste de color.
    """
    try:
        nft_part_colors_code = (
            db.query(model_nft.NftPart)
            .filter(model_nft.NftPart.code == nft_part_code)
            .first()
            .colors
        )
    except Exception:
        raise AttributeError
    if any(nft_part_colors_code):
        return nft_part_colors_code
    return []


def create_dependent_face_parts_colors(
    db: Session,
    dependent_face_parts_colors: List[schema_nft.DependentFacePartColorCreate],
):
    """Crée une dépendance entre une partie de visage et une couleur.

    Args:
        db (Session): session de la base de donnée.
        dependent_face_parts_colors (List[schema_nft.DependentFacePartColorCreate]): liste de dépendances.

    Raises:
        PronochainException: la dépendance n'a pas été crée.
    """
    try:
        for dependent_face_part_color in dependent_face_parts_colors:
            face_part_color_id = dependent_face_part_color.face_part_color_id
            depend_face_part_color_id = (
                dependent_face_part_color.depend_face_part_color_id
            )
            face_part_color = (
                db.query(model_nft.FacePartColor)
                .filter(model_nft.FacePartColor.id == face_part_color_id)
                .first()
            )
            depend_face_part_color = (
                db.query(model_nft.FacePartColor)
                .filter(model_nft.FacePartColor.id == depend_face_part_color_id)
                .first()
            )
            face_part_color.depend_face_part_colors.append(depend_face_part_color)
        db.commit()
    except IntegrityError as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])


def delete_dependent_face_parts_colors(
    db: Session,
    dependent_face_parts_colors: List[schema_nft.DependentFacePartColorDelete],
):
    """Supprime une dépendance entre une partie de visage et une couleur.

    Args:
        db (Session): session de la base de donnée.
        dependent_face_parts_colors (List[schema_nft.DependentFacePartColorDelete]): liste de dépendances.

    Raises:
        PronochainException: la dépendance n'a pas été supprimée.
    """
    try:
        for dependent_face_part_color in dependent_face_parts_colors:
            face_part_color_id = dependent_face_part_color.face_part_color_id
            depend_face_part_color_id = (
                dependent_face_part_color.depend_face_part_color_id
            )
            face_part_color = (
                db.query(model_nft.FacePartColor)
                .filter(model_nft.FacePartColor.id == face_part_color_id)
                .first()
            )
            depend_face_part_colors = face_part_color.depend_face_part_colors
            new_depend_face_part_colors = [
                depend_face_part_color
                for depend_face_part_color in depend_face_part_colors
                if depend_face_part_color.id != depend_face_part_color_id
            ]
            face_part_color.depend_face_part_colors = new_depend_face_part_colors
        db.commit()
    except IntegrityError as e:
        raise PronochainException(str(e.orig).split("DETAIL: ")[-1])
