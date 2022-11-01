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

File: app/generation_nft_db/models/names.py
"""
from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, String
from sqlalchemy.orm import relationship

from app.generation_nft_db.models.base import Base


class NameType(Base):
    """NameType modèle.

    Args:
        Base (Base): modèle pydantic.

    Returns:
        str: value.
    """

    __tablename__ = "name_types"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    code = Column(SmallInteger, unique=True, nullable=False, index=True)
    value = Column(String(100), nullable=False)

    names = relationship("Name", back_populates="type", cascade="all,delete")

    def __repr__(self) -> str:
        """Représentation du modèle NameType.

        Returns:
            str: value.
        """
        return self.value


class Name(Base):
    """Name modèle.

    Args:
        Base (Base): modèle pydantic.

    Returns:
        str: value.
    """

    __tablename__ = "names"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    value = Column(String(255), nullable=False)
    type_id = Column(Integer, ForeignKey("name_types.id", ondelete="cascade"))

    type = relationship("NameType", back_populates="names", cascade="all,delete")

    def __repr__(self) -> str:
        """Représentation du modèle Name.

        Returns:
            str: value.
        """
        return self.value
