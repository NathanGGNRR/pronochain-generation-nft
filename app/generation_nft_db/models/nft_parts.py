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

File: app/generation_nft_db/models/nft_parts.py
"""
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Sequence,
    SmallInteger,
    String,
    Table,
)
from sqlalchemy.orm import backref, relationship

from app.generation_nft_db.models.base import Base


class ElementType(Base):
    """ElementType modèle.

    Args:
        Base (Base): modèle pydantic.

    Returns:
        str: name.
    """

    __tablename__ = "element_types"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    code = Column(SmallInteger, unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)

    elements = relationship("Element", back_populates="type", cascade="all,delete")

    def __repr__(self) -> str:
        """Représentation du modèle ElementType.

        Returns:
            str: name.
        """
        return self.name


class Element(Base):
    """Element modèle.

    Args:
        Base (Base): modèle pydantic.

    Returns:
        str: name.
    """

    __tablename__ = "elements"
    all_delete = "all,delete"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    code = Column(SmallInteger, unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    nft_part_id = Column(Integer, ForeignKey("nft_parts.id", ondelete="cascade"))
    type_id = Column(Integer, ForeignKey("element_types.id", ondelete="cascade"))
    parent_id = Column(
        Integer, ForeignKey("elements.id", ondelete="cascade"), index=True
    )
    cid = Column(String(255))
    filename = Column(String(255))
    rarity_id = Column(Integer, ForeignKey("rarities.id", ondelete="cascade"))

    nft_part = relationship("NftPart", back_populates="elements", cascade=all_delete)
    type = relationship("ElementType", back_populates="elements", cascade=all_delete)
    children = relationship(lambda: Element, backref=backref("parent", remote_side=id))
    position_types = relationship(
        "PositionType", back_populates="element", cascade=all_delete
    )
    rarity = relationship("Rarity", back_populates="elements", cascade=all_delete)

    def __repr__(self) -> str:
        """Représentation du modèle Element.

        Returns:
            str: name.
        """
        return self.name


class Color(Base):
    """Color modèle.

    Args:
        Base (Base): modèle pydantic.

    Returns:
        str: hex.
    """

    __tablename__ = "colors"
    all_delete = "all,delete"

    id = Column(
        Integer,
        Sequence("colors_id_seq", start=40, increment=1),
        autoincrement=True,
        primary_key=True,
        index=True,
    )
    hex = Column(String(7), unique=True, nullable=False)
    nft_part_id = Column(Integer, ForeignKey("nft_parts.id", ondelete="cascade"))
    rarity_id = Column(Integer, ForeignKey("rarities.id", ondelete="cascade"))

    nft_part = relationship("NftPart", back_populates="colors", cascade=all_delete)
    face_parts_colors = relationship(
        "FacePartColor", back_populates="color", cascade=all_delete
    )
    rarity = relationship("Rarity", back_populates="colors", cascade=all_delete)

    def __repr__(self) -> str:
        """Représentation du modèle Color.

        Returns:
            str: hex.
        """
        return self.hex


class NftPart(Base):
    """NftPart modèle.

    Args:
        Base (Base): modèle pydantic.

    Returns:
        str: name.
    """

    __tablename__ = "nft_parts"
    all_delete = "all,delete"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    code = Column(SmallInteger, unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)

    elements = relationship("Element", back_populates="nft_part", cascade=all_delete)
    colors = relationship("Color", back_populates="nft_part", cascade=all_delete)

    def __repr__(self) -> str:
        """Représentation du modèle NftPart.

        Returns:
            str: name.
        """
        return self.name


class FacePart(Base):
    """FacePart modèle.

    Args:
        Base (Base): modèle pydantic.

    Returns:
        str: name.
    """

    __tablename__ = "face_parts"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    code = Column(SmallInteger, unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)

    face_parts_colors = relationship(
        "FacePartColor", back_populates="face_part", cascade="all,delete"
    )

    def __repr__(self) -> str:
        """Représentation du modèle FacePart.

        Returns:
            str: name.
        """
        return self.name


dependent_face_parts_colors = Table(
    "dependent_face_parts_colors",
    Base.metadata,
    Column(
        "face_part_color_id",
        Integer,
        ForeignKey("face_parts_colors.id", ondelete="cascade"),
        primary_key=True,
    ),
    Column(
        "depend_face_part_color_id",
        Integer,
        ForeignKey("face_parts_colors.id", ondelete="cascade"),
        primary_key=True,
    ),
)


class FacePartColor(Base):
    """FacePartColor modèle.

    Args:
        Base (Base): modèle pydantic.

    Returns:
        str: face part et color.
    """

    __tablename__ = "face_parts_colors"
    all_delete = "all,delete"

    id = Column(
        Integer,
        Sequence("face_parts_colors_id_seq", start=36, increment=1),
        autoincrement=True,
        primary_key=True,
        index=True,
    )
    face_part_id = Column(ForeignKey("face_parts.id", ondelete="cascade"))
    color_id = Column(ForeignKey("colors.id", ondelete="cascade"))

    face_part = relationship(
        "FacePart",
        back_populates="face_parts_colors",
        cascade=all_delete,
        lazy="joined",
    )
    color = relationship(
        "Color", back_populates="face_parts_colors", cascade=all_delete, lazy="joined"
    )
    depend_face_part_colors = relationship(
        "FacePartColor",
        secondary=dependent_face_parts_colors,
        primaryjoin=id == dependent_face_parts_colors.c.face_part_color_id,
        secondaryjoin=id == dependent_face_parts_colors.c.depend_face_part_color_id,
        backref="depended_face_parts_colors",
        cascade=all_delete,
        lazy="joined",
        join_depth=2,
    )

    def __repr__(self) -> str:
        """Représentation du modèle FacePartColor.

        Returns:
            str: face part et color.
        """
        return f"Part: {self.face_part} - Color: ({self.color})"
