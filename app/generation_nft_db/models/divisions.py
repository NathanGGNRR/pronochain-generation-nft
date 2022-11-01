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

File: app/generation_nft_db/models/divisions.py
"""
from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.generation_nft_db.models.base import Base


class Division(Base):
    """Division modèle.

    Args:
        Base (Base): modèle pydantic.

    Returns:
        str: name.
    """

    __tablename__ = "divisions"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    code = Column(BigInteger, unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id", ondelete="cascade"))

    country = relationship("Country", back_populates="divisions", cascade="all,delete")
    clubs = relationship("Club", back_populates="division", cascade="all,delete")

    def __repr__(self) -> str:
        """Représentation du modèle Division.

        Returns:
            str: name.
        """
        return self.name
