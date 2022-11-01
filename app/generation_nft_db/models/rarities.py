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

File: app/generation_nft_db/models/rarities.py
"""
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from app.generation_nft_db.models.base import Base


class Rarity(Base):
    """Rarity modèle.

    Args:
        Base (Base): modèle pydantic.

    Returns:
        str: name.
    """

    __tablename__ = "rarities"
    all_delete = "all,delete"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    code = Column(Integer, unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    percentage = Column(Float(3), nullable=False)

    elements = relationship("Element", back_populates="rarity", cascade=all_delete)
    colors = relationship("Color", back_populates="rarity", cascade=all_delete)
    players = relationship("Player", back_populates="rarity", cascade=all_delete)

    def __repr__(self) -> str:
        """Représentation du modèle Rarity.

        Returns:
            str: name.
        """
        return self.name
