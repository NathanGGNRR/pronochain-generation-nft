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

File: app/generation_nft_db/models/positions.py
"""
from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, String
from sqlalchemy.orm import relationship

from app.generation_nft_db.models.base import Base
from app.generation_nft_db.models.players import players_positions
from app.generation_nft_db.models.stats import stats_positions


class PositionType(Base):
    """PositionType modèle.

    Args:
        Base (Base): modèle pydantic.

    Returns:
        str: value.
    """

    __tablename__ = "position_types"
    all_delete = "all,delete"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    code = Column(SmallInteger, unique=True, nullable=False, index=True)
    abbreviation = Column(String(10), nullable=False)
    value = Column(String(255), nullable=False)
    element_id = Column(Integer, ForeignKey("elements.id", ondelete="cascade"))

    element = relationship(
        "Element", back_populates="position_types", cascade=all_delete, lazy="joined"
    )
    positions = relationship(
        "Position", back_populates="type", cascade=all_delete, lazy="joined"
    )

    def __repr__(self) -> str:
        """Représentation du modèle PositionType.

        Returns:
            str: value.
        """
        return self.value


class Position(Base):
    """Position modèle.

    Args:
        Base (Base): modèle pydantic.

    Returns:
        str: value.
    """

    __tablename__ = "positions"
    all_delete = "all,delete"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    code = Column(SmallInteger, unique=True, nullable=False, index=True)
    abbreviation = Column(String(10), nullable=False)
    value = Column(String(255), nullable=False)
    type_id = Column(Integer, ForeignKey("position_types.id", ondelete="cascade"))

    type = relationship(
        "PositionType", back_populates="positions", cascade=all_delete, lazy="joined"
    )
    players = relationship(
        "Player",
        secondary=players_positions,
        back_populates="positions",
        cascade=all_delete,
        lazy="joined",
    )
    stats = relationship(
        "Stat",
        secondary=stats_positions,
        back_populates="positions",
        cascade=all_delete,
        lazy="joined",
    )

    def __repr__(self) -> str:
        """Représentation du modèle Position.

        Returns:
            str: value.
        """
        return self.value
