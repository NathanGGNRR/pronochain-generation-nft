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

File: app/generation_nft_db/schemas/nft_parts.py
"""
from typing import List, Optional

from pydantic import BaseModel, constr

from app.generation_nft_db.schemas.rarities import RarityOut


class CodeNameModel(BaseModel):
    """CodeNameModel schéma.

    Args:
        BaseModel (BaseModel): modèle pydantic.
    """

    code: int
    name: constr(max_length=255)


class NftPart(CodeNameModel):
    """NftPart schéma.

    Args:
        CodeNameModel (CodeNameModel): modèle CodeNameModel.
    """

    pass


class FacePart(CodeNameModel):
    """FacePart schéma.

    Args:
        CodeNameModel (CodeNameModel): modèle CodeNameModel.
    """

    pass


class ElementType(CodeNameModel):
    """ElementType schéma.

    Args:
        CodeNameModel (CodeNameModel): modèle CodeNameModel.
    """

    pass


class Element(CodeNameModel):
    """Element schéma.

    Args:
        CodeNameModel (CodeNameModel): modèle CodeNameModel.
    """

    cid: Optional[str]
    filename: Optional[str]


class Color(BaseModel):
    """Color schéma.

    Args:
        BaseModel (BaseModel): modèle pydantic.
    """

    hex: constr(max_length=7)


class FacePartColor(BaseModel):
    """FacePartColor schéma.

    Args:
        BaseModel (BaseModel): modèle pydantic.
    """

    id: int

    class Config:
        """Classe config d'un modèle pydantic."""

        orm_mode = True


class NftPartOut(NftPart):
    """NftPartOut schéma.

    Args:
        NftPart (NftPart): modèle NftPart.
    """

    id: int

    class Config:
        """Classe config d'un modèle pydantic."""

        orm_mode = True


class FacePartOut(FacePart):
    """FacePartOut schéma.

    Args:
        FacePart (FacePart): modèle FacePart.
    """

    id: int

    class Config:
        """Classe config d'un modèle pydantic."""

        orm_mode = True


class ElementTypeOut(ElementType):
    """ElementTypeOut schéma.

    Args:
        ElementType (ElementType): modèle ElementType.
    """

    id: int

    class Config:
        """Classe config d'un modèle pydantic."""

        orm_mode = True


class ElementOut(Element):
    """ElementOut schéma.

    Args:
        Element (Element): modèle Element.
    """

    id: int

    class Config:
        """Classe config d'un modèle pydantic."""

        orm_mode = True


class ColorOut(Color):
    """ColorOut schéma.

    Args:
        Color (Color): modèle Color.
    """

    id: int

    class Config:
        """Classe config d'un modèle pydantic."""

        orm_mode = True


class FacePartColorOut(FacePartColor):
    """FacePartColorOut schéma.

    Args:
        FacePartColor (FacePartColor): modèle FacePartColor.
    """

    color: ColorOut


class FacePartColorNestedOut(FacePartColor):
    """FacePartColorNestedOut schéma.

    Args:
        FacePartColor (FacePartColor): modèle FacePartColor.
    """

    face_part: FacePartOut
    color: ColorOut


class FacePartColorWithoutFacePartOut(FacePartColor):
    """FacePartColorWithoutFacePartOut schéma.

    Args:
        FacePartColor (FacePartColor): modèle FacePartColor.
    """

    color: ColorOut
    depend_face_part_colors: Optional[List[FacePartColorOut]]


class NftPartNestedOut(NftPartOut):
    """NftPartNestedOut schéma.

    Args:
        NftPartOut (NftPartOut): modèle NftPartOut.
    """

    elements: Optional[List[ElementOut]]
    colors: Optional[List[ColorOut]]


class FacePartNestedOut(FacePartOut):
    """FacePartNestedOut schéma.

    Args:
        FacePartOut (FacePartOut): modèle FacePartOut.
    """

    face_parts_colors: Optional[List[FacePartColorWithoutFacePartOut]]


class ElementTypeNestedOut(ElementTypeOut):
    """ElementTypeNestedOut schéma.

    Args:
        ElementTypeOut (ElementTypeOut): modèle ElementTypeOut.
    """

    elements: Optional[List[ElementOut]]


class ElementNestedOut(ElementOut):
    """ElementNestedOut schéma.

    Args:
        ElementOut (ElementOut): modèle ElementOut.
    """

    nft_part: Optional[NftPartOut]
    type: Optional[ElementTypeOut]
    parent: Optional[ElementOut]
    rarity: Optional[RarityOut]


class ColorNestedOut(ColorOut):
    """ColorNestedOut schéma.

    Args:
        ColorOut (ColorOut): modèle ColorOut.
    """

    nft_part: Optional[NftPartOut]
    rarity: Optional[RarityOut]


class FacePartColorCreate(BaseModel):
    """FacePartColorCreate schéma.

    Args:
        BaseModel (BaseModel): modèle pydantic.
    """

    color_id: int


class NftPartCreate(NftPart):
    """NftPartCreate schéma.

    Args:
        NftPart (NftPart): modèle NftPart.
    """

    pass


class NftPartUpdate(NftPartCreate):
    """NftPartUpdate schéma.

    Args:
        NftPartCreate (NftPartCreate): modèle NftPartCreate.
    """

    pass


class ElementTypeCreate(ElementType):
    """ElementTypeCreate schéma.

    Args:
        ElementType (ElementType): modèle ElementType.
    """

    pass


class ElementTypeUpdate(ElementTypeCreate):
    """ElementTypeUpdate schéma.

    Args:
        ElementTypeCreate (ElementTypeCreate): modèle ElementTypeCreate.
    """

    pass


class ElementCreate(Element):
    """ElementCreate schéma.

    Args:
        Element (Element): modèle Element.
    """

    nft_part_id: Optional[int]
    type_id: Optional[int]
    parent_id: Optional[int]
    rarity_id: Optional[int]


class ElementUpdate(ElementCreate):
    """ElementUpdate schéma.

    Args:
        ElementCreate (ElementCreate): modèle ElementCreate.
    """

    pass


class ColorCreate(Color):
    """ColorCreate schéma.

    Args:
        Color (Color): modèle Color.
    """

    nft_part_id: Optional[int]
    rarity_id: Optional[int]


class ColorUpdate(ColorCreate):
    """ColorUpdate schéma.

    Args:
        ColorCreate (ColorCreate): modèle ColorCreate.
    """

    pass


class FacePartCreate(FacePart):
    """FacePartCreate schéma.

    Args:
        FacePart (FacePart): modèle FacePart.
    """

    face_parts_colors: Optional[List[FacePartColorCreate]]


class FacePartUpdate(FacePartCreate):
    """FacePartUpdate schéma.

    Args:
        FacePartCreate (FacePartCreate): modèle FacePartCreate.
    """

    pass


class DependentFacePartColorCreate(BaseModel):
    """DependentFacePartColorCreate schéma.

    Args:
        BaseModel (BaseModel): modèle pydantic.
    """

    face_part_color_id: int
    depend_face_part_color_id: int


class DependentFacePartColorDelete(DependentFacePartColorCreate):
    """DependentFacePartColorDelete schéma.

    Args:
        DependentFacePartColorCreate (DependentFacePartColorCreate): modèle DependentFacePartColorCreate.
    """

    face_part_color_id: int
    depend_face_part_color_id: int
