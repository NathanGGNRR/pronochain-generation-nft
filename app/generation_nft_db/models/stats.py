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

File: app/generation_nft_db/models/stats.py
"""
from sqlalchemy import Column, ForeignKey, Integer, SmallInteger, String, Table
from sqlalchemy.orm import relationship

from app.generation_nft_db.models.base import Base

stats_stat_types = Table(
    "stats_stat_types",
    Base.metadata,
    Column("stat_id", ForeignKey("stats.id", ondelete="cascade"), primary_key=True),
    Column(
        "type_id", ForeignKey("stat_types.id", ondelete="cascade"), primary_key=True
    ),
)

stats_positions = Table(
    "stats_positions",
    Base.metadata,
    Column("stat_id", ForeignKey("stats.id", ondelete="cascade"), primary_key=True),
    Column(
        "position_id", ForeignKey("positions.id", ondelete="cascade"), primary_key=True
    ),
)


class StatType(Base):
    """Stat type modèle.

    Args:
        Base (Base): modèle pydantic.

    Returns:
        str: value.
    """

    __tablename__ = "stat_types"
    all_delete = "all,delete"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    code = Column(SmallInteger, unique=True, nullable=False, index=True)
    value = Column(String(255), nullable=False)

    stats = relationship(
        "Stat", secondary=stats_stat_types, back_populates="types", cascade=all_delete
    )

    def __repr__(self) -> str:
        """Représentation du modèle StatType.

        Returns:
            str: value.
        """
        return self.value


class Stat(Base):
    """Stat modèle.

    Args:
        Base (Base): modèle pydantic.

    Returns:
        str: value.
    """

    __tablename__ = "stats"
    all_delete = "all,delete"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    code = Column(SmallInteger, unique=True, nullable=False, index=True)
    value = Column(String(255), nullable=False)

    types = relationship(
        "StatType",
        secondary=stats_stat_types,
        back_populates="stats",
        cascade=all_delete,
        lazy="joined",
    )
    players = relationship("PlayerStat", back_populates="stat", cascade=all_delete)
    positions = relationship(
        "Position",
        secondary=stats_positions,
        back_populates="stats",
        cascade=all_delete,
        lazy="joined",
    )

    def __repr__(self) -> str:
        """Représentation du modèle Stat.

        Returns:
            str: value.
        """
        return self.value
