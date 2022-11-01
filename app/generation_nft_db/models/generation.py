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

File: app/generation_nft_db/models/generation.py
"""
from sqlalchemy import BigInteger, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.generation_nft_db.models.base import Base


class Combination(Base):
    """Combination modèle.

    Args:
        Base (Base): modèle pydantic.
    """

    __tablename__ = "combinations"
    colors_id = "colors.id"
    elements_id = "elements.id"
    names_id = "names.id"
    all_delete = "all,delete"

    card_shape_id = Column(
        Integer, ForeignKey(elements_id, ondelete="cascade"), primary_key=True
    )
    card_pattern_id = Column(
        Integer, ForeignKey(elements_id, ondelete="cascade"), primary_key=True
    )
    card_color_id = Column(
        Integer, ForeignKey(colors_id, ondelete="cascade"), primary_key=True
    )
    shirt_pattern_id = Column(
        Integer, ForeignKey(elements_id, ondelete="cascade"), primary_key=True
    )
    crest_shape_id = Column(
        Integer, ForeignKey(elements_id, ondelete="cascade"), primary_key=True
    )
    crest_pattern_id = Column(
        Integer, ForeignKey(elements_id, ondelete="cascade"), primary_key=True
    )
    crest_content_id = Column(
        Integer, ForeignKey(elements_id, ondelete="cascade"), primary_key=True
    )
    player_picture_id = Column(
        Integer, ForeignKey("players.id", ondelete="cascade"), primary_key=True
    )
    first_name_id = Column(
        Integer, ForeignKey(names_id, ondelete="cascade"), primary_key=True
    )
    last_name_id = Column(
        Integer, ForeignKey(names_id, ondelete="cascade"), primary_key=True
    )
    country_flag_id = Column(
        Integer, ForeignKey("countries.id", ondelete="cascade"), primary_key=True
    )
    hair_color_id = Column(
        Integer, ForeignKey(colors_id, ondelete="cascade"), primary_key=True
    )
    eyes_color_id = Column(
        Integer, ForeignKey(colors_id, ondelete="cascade"), primary_key=True
    )
    skin_color_id = Column(
        Integer, ForeignKey(colors_id, ondelete="cascade"), primary_key=True
    )
    mouth_color_id = Column(
        Integer, ForeignKey(colors_id, ondelete="cascade"), primary_key=True
    )
    count = Column(BigInteger, nullable=False, index=True)

    card_shape = relationship(
        "Element",
        backref="card_shape_combinations",
        foreign_keys=[card_shape_id],
        cascade=all_delete,
    )
    card_pattern = relationship(
        "Element",
        backref="card_pattern_combinations",
        foreign_keys=[card_pattern_id],
        cascade=all_delete,
    )
    card_color = relationship(
        "Color",
        backref="card_color_combinations",
        foreign_keys=[card_color_id],
        cascade=all_delete,
    )
    shirt_pattern = relationship(
        "Element",
        backref="shirt_pattern_combinations",
        foreign_keys=[shirt_pattern_id],
        cascade=all_delete,
    )
    crest_shape = relationship(
        "Element",
        backref="crest_shape_combinations",
        foreign_keys=[crest_shape_id],
        cascade=all_delete,
    )
    crest_pattern = relationship(
        "Element",
        backref="crest_pattern_combinations",
        foreign_keys=[crest_pattern_id],
        cascade=all_delete,
    )
    crest_content = relationship(
        "Element",
        backref="crest_content_combinations",
        foreign_keys=[crest_content_id],
        cascade=all_delete,
    )
    player_picture = relationship(
        "Player", back_populates="combinations", cascade=all_delete
    )
    first_name = relationship(
        "Name",
        backref="first_name_combinations",
        foreign_keys=[first_name_id],
        cascade=all_delete,
    )
    last_name = relationship(
        "Name",
        backref="last_name_combinations",
        foreign_keys=[last_name_id],
        cascade=all_delete,
    )
    country_flag = relationship(
        "Country", back_populates="combinations", cascade=all_delete
    )
    hair_color = relationship(
        "Color",
        backref="hair_color_combinations",
        foreign_keys=[hair_color_id],
        cascade=all_delete,
    )
    eyes_color = relationship(
        "Color",
        backref="eyes_color_combinations",
        foreign_keys=[eyes_color_id],
        cascade=all_delete,
    )
    skin_color = relationship(
        "Color",
        backref="skin_color_combinations",
        foreign_keys=[skin_color_id],
        cascade=all_delete,
    )
    mouth_color = relationship(
        "Color",
        backref="mouth_color_combinations",
        foreign_keys=[mouth_color_id],
        cascade=all_delete,
    )
