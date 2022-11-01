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

File: app/generation_nft_db/models/country.py
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.generation_nft_db.models.base import Base
from app.generation_nft_db.models.players import players_countries


class Country(Base):
    """Country modèle.

    Args:
        Base (Base): modèle pydantic.

    Returns:
        str: value.
    """

    __tablename__ = "countries"
    all_delete = "all,delete"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    code = Column(String(2), unique=True, nullable=False, index=True)
    value = Column(String(255), nullable=False)
    cid = Column(String(255))
    filename = Column(String(255))

    divisions = relationship("Division", back_populates="country", cascade=all_delete)
    clubs = relationship("Club", back_populates="country", cascade=all_delete)
    players = relationship(
        "Player",
        secondary=players_countries,
        back_populates="countries",
        cascade=all_delete,
    )
    combinations = relationship(
        "Combination", back_populates="country_flag", cascade=all_delete
    )

    def __repr__(self) -> str:
        """Représentation du modèle Country.

        Returns:
            str: value.
        """
        return self.value
