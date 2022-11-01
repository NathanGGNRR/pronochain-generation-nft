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

File: app/generation_nft_db/models/clubs.py
"""
from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.generation_nft_db.models.base import Base


class Club(Base):
    """Club modèle.

    Args:
        Base (Base): modèle pydantic.

    Returns:
        str: name.
    """

    __tablename__ = "clubs"
    all_delete = "all,delete"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    code = Column(BigInteger, unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id", ondelete="cascade"))
    division_id = Column(Integer, ForeignKey("divisions.id", ondelete="cascade"))
    first_color_id = Column(ForeignKey("colors.id", ondelete="cascade"))
    second_color_id = Column(ForeignKey("colors.id", ondelete="cascade"))

    country = relationship("Country", back_populates="clubs", cascade=all_delete)
    division = relationship("Division", back_populates="clubs", cascade=all_delete)
    players = relationship("Player", back_populates="club", cascade=all_delete)
    first_color = relationship(
        "Color",
        backref="first_clubs",
        foreign_keys=[first_color_id],
        cascade=all_delete,
        lazy="joined",
    )
    second_color = relationship(
        "Color",
        backref="second_clubs",
        foreign_keys=[second_color_id],
        cascade=all_delete,
        lazy="joined",
    )

    def __repr__(self) -> str:
        """Représentation du modèle Club.

        Returns:
            str: name.
        """
        return self.name
