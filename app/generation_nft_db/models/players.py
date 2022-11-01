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

File: app/generation_nft_db/models/players.py
"""
from sqlalchemy import (
    BigInteger,
    Column,
    Date,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    Table,
)
from sqlalchemy.orm import relationship

from app.generation_nft_db.models.base import Base

players_id = "players.id"

players_countries = Table(
    "players_countries",
    Base.metadata,
    Column("player_id", ForeignKey(players_id, ondelete="cascade"), primary_key=True),
    Column(
        "country_id", ForeignKey("countries.id", ondelete="cascade"), primary_key=True
    ),
)

players_positions = Table(
    "players_positions",
    Base.metadata,
    Column("player_id", ForeignKey(players_id, ondelete="cascade"), primary_key=True),
    Column(
        "position_id", ForeignKey("positions.id", ondelete="cascade"), primary_key=True
    ),
)


class Player(Base):
    """Player modèle.

    Args:
        Base (Base): modèle pydantic.

    Returns:
        str: last name et first name.
    """

    __tablename__ = "players"
    all_delete = "all,delete"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    code = Column(BigInteger, unique=True, nullable=False, index=True)
    first_name_id = Column(
        Integer, ForeignKey("names.id", ondelete="cascade"), nullable=True
    )
    last_name_id = Column(
        Integer, ForeignKey("names.id", ondelete="cascade"), nullable=False
    )
    age = Column(Integer, nullable=False)
    birth = Column(Date, nullable=False)
    height = Column(SmallInteger, nullable=False)
    weight = Column(SmallInteger, nullable=False)
    cid = Column(String(255))
    filename = Column(String(255))
    club_id = Column(Integer, ForeignKey("clubs.id", ondelete="cascade"))
    rarity_id = Column(Integer, ForeignKey("rarities.id", ondelete="cascade"))

    first_name = relationship(
        "Name",
        backref="first_names",
        foreign_keys=[first_name_id],
        cascade=all_delete,
        lazy="joined",
    )
    last_name = relationship(
        "Name",
        backref="last_names",
        foreign_keys=[last_name_id],
        cascade=all_delete,
        lazy="joined",
    )
    club = relationship("Club", back_populates="players", cascade=all_delete)
    stats = relationship("PlayerStat", back_populates="player", cascade=all_delete)
    countries = relationship(
        "Country",
        secondary=players_countries,
        back_populates="players",
        cascade=all_delete,
        lazy="joined",
    )
    positions = relationship(
        "Position",
        secondary=players_positions,
        back_populates="players",
        cascade=all_delete,
    )
    rarity = relationship("Rarity", back_populates="players", cascade=all_delete)
    combinations = relationship(
        "Combination", back_populates="player_picture", cascade=all_delete
    )

    def __repr__(self) -> str:
        """Représentation du modèle Player.

        Returns:
            str: last name et first name.
        """
        try:
            return f"{self.last_name.value} {self.first_name.value}"
        except AttributeError:
            return str(self.code)


class PlayerStat(Base):
    """PlayerStat modèle.

    Args:
        Base (Base): modèle pydantic.

    Returns:
        str: last name et first name, valeur de la stat.
    """

    __tablename__ = "players_stats"

    player_id = Column(ForeignKey(players_id, ondelete="cascade"), primary_key=True)
    stat_id = Column(ForeignKey("stats.id", ondelete="cascade"), primary_key=True)
    value = Column(SmallInteger, nullable=False)

    player = relationship("Player", back_populates="stats", cascade="all,delete")
    stat = relationship("Stat", back_populates="players", cascade="all,delete")

    def __repr__(self) -> str:
        """Représentation du modèle PlayerStat.

        Returns:
            str: last name et first name, valeur de la stat.
        """
        return f"{self.player.last_name.value} {self.player.first_name.value}, {self.stat.value}: {self.value}"
