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

File: app/generation_nft/libraries/card/card.py
"""
from typing import Union

import cv2 as open_cv
import imutils
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from app.generation_nft.libraries.card.constants import (
    COORDINATES_PARTS,
    FONT_SIZE_NOTE,
    MARGIN,
    STAR_COLOR,
    Anchor,
    Content,
    Direction,
    OrientationResize,
    PictureName,
    Type,
)
from app.generation_nft.utils import (
    draw_contours,
    get_coordinates,
    replace_color,
    replace_color_not_equal,
)
from app.generation_nft_db.constants import FixtureEnum
from app.settings import settings


class CardStyling(object):
    """Classe permettant de styliser la carte."""

    def __init__(self):
        """Initialise la classe pour dessiner le carte."""
        self.font_path = (
            f"{settings.FIXTURE_FILES_PATH}/fonts/{FixtureEnum.CARD_FONT.value}.ttf"
        )

        self.margin = MARGIN
        self.font_size_note = FONT_SIZE_NOTE

        self.age_note = str(self.player.age)
        self.height_note = str(self.player.height)
        self.weight_note = str(self.player.weight)

    def draw_card(self) -> np.array:
        """Dessine la carte du NFT.

        Returns:
            np.array: carte du NFT.
        """
        virgin_card_part = np.full(
            (self.card_shape.shape[0], self.card_shape.shape[1], 4),
            np.array([255, 255, 255, 0]),
            dtype=np.uint8,
        )
        height_to_remove = int(
            (self.card_pattern.shape[0] - self.card_shape.shape[0]) / 2
        )
        self.card_pattern = self.card_pattern[
            height_to_remove : (self.card_shape.shape[0] + height_to_remove),
            : self.card_shape.shape[1],
        ]
        visual_card_shape, card_shape_contours = draw_contours(
            self.card_shape,
            open_cv.cvtColor(self.card_shape, open_cv.COLOR_BGR2HSV),
            (0, 0, 0),
            open_cv.FILLED,
            as_mask=True,
        )
        card_pattern = open_cv.bitwise_and(
            self.card_pattern, self.card_pattern, mask=visual_card_shape
        )
        replace_color(
            card_pattern, np.array([0, 0, 0, 0]), np.array([255, 255, 255, 0])
        )
        open_cv.drawContours(
            virgin_card_part,
            card_shape_contours,
            -1,
            (
                int(self.card_color[0]),
                int(self.card_color[1]),
                int(self.card_color[2]),
                255,
            ),
            open_cv.FILLED,
        )

        card_pil = Image.fromarray(virgin_card_part.astype("uint8"), "RGBA")
        card_pattern_pil = Image.fromarray(card_pattern.astype("uint8"), "RGBA")
        card_pil.paste(card_pattern_pil, (0, 0), card_pattern_pil)
        self.add_parts(card_pil)
        card_part = np.array(card_pil)

        _, card_bytes = open_cv.imencode(".png", card_part)
        return card_bytes.tobytes()

    def add_parts(self, card_pil: Image):
        """Ajoute les parties constituant la carte du NFT.

        Args:
            card_pil (Image): carte du NFT.
        """
        for coordinates_part in COORDINATES_PARTS:
            color = coordinates_part.get("color")
            if color is not None:
                coordinates = get_coordinates(self.card_shape, color)

            card_type = coordinates_part.get("type")

            content = coordinates_part.get("content")
            value = coordinates_part.get("value")
            if content == Content.ATTRIBUTE.value:
                value = getattr(self, value)

            size = coordinates_part.get("size")
            if size is None and card_type == Type.PICTURE.value:
                size = value.shape

            position = (coordinates[1], coordinates[0])

            margin = (
                coordinates_part.get("margin")
                if coordinates_part.get("margin") is not None
                else self.margin
            )

            if card_type == Type.FONT.value:
                self.draw_text(
                    card_pil,
                    value,
                    position,
                    size,
                    coordinates,
                    coordinates_part,
                )
            elif card_type in [Type.PICTURE.value, Type.PICTURES.value]:
                self.draw_picture(
                    card_pil,
                    value,
                    position,
                    size,
                    coordinates,
                    coordinates_part,
                    margin,
                )

    def draw_text(
        self,
        card_pil: Image,
        value: str,
        position: tuple,
        size: int,
        coordinates: tuple,
        coordinates_part: dict,
    ):
        """Dessine du texte.

        Args:
            card_pil (Image): carte.
            value (str): valeur.
            position (tuple): position.
            size (int): taille.
            coordinates (tuple): coordonnées.
            coordinates_part (dict): coordonnées de la partie.
        """
        fill = coordinates_part.get("fill")
        depending = coordinates_part.get("depending")
        anchor = coordinates_part.get("anchor")
        opacity = coordinates_part.get("opacity")
        uppercase = coordinates_part.get("uppercase")

        if depending is not None:
            last_x = coordinates_part.get("last_x")
            last_y = coordinates_part.get("last_y")

            position = get_coordinates(
                np.array(card_pil), [254, 254, 254, 255], last_x=last_x, last_y=last_y
            )
            if last_x:
                position = (position[1] + 25, position[0])
            if last_y:
                position = (coordinates[1], position[0] + 100)

        draw_card = ImageDraw.Draw(card_pil)
        font = ImageFont.truetype(self.font_path, size)
        draw_card.text(
            position,
            value.upper() if uppercase else value,
            font=font,
            fill=(fill[0], fill[1], fill[2], opacity),
            spacing=0,
            anchor=anchor,
        )

    def draw_picture(
        self,
        card_pil: Image,
        value: np.array,
        position: tuple,
        size: Union[int, tuple],
        coordinates: tuple,
        coordinates_part: dict,
        margin: int,
    ):
        """Dessine une image sur la carte NFT.

        Args:
            card_pil (Image): carte.
            value (np.array): valeur.
            position (tuple): position.
            size (Union[int, tuple]): taille.
            coordinates (tuple): coordonnées.
            coordinates_part (dict): coordonnées de la partie.
            margin (int): margin.
        """
        if value is not None:
            value = open_cv.cvtColor(value, open_cv.COLOR_BGRA2RGBA)
        name = coordinates_part.get("name")
        depending = coordinates_part.get("depending")
        anchor = coordinates_part.get("anchor")
        opacity = coordinates_part.get("opacity")
        value_to_add = coordinates_part.get("value_to_add")
        resize = coordinates_part.get("resize")
        if resize is not None:
            value = self.resize(
                value, resize, coordinates_part.get("resize_orientation")
            )
            height, width = value.shape[0], value.shape[1]
        elif size is not None:
            height, width = size[0], size[1]
        else:
            (width, height) = card_pil.size

        if anchor == Anchor.TOP_MIDDLE.value:
            position = (coordinates[1] - int(width / 2), coordinates[0])
            if depending is not None:
                depending_position = get_coordinates(
                    np.array(card_pil), [254, 254, 254, 255], last_x=False, last_y=True
                )
                position = (position[0], depending_position[0] + margin)

        elif anchor == Anchor.BOTTOM_MIDDLE.value:
            position = (coordinates[1] - int(width / 2), coordinates[0] - height)

        elif anchor == Anchor.TOP_RIGHT.value:
            position = (coordinates[1] - width, coordinates[0])
            if depending is not None:
                depending_position = get_coordinates(
                    np.array(card_pil), [254, 254, 254, 255], last_x=False, last_y=True
                )
                if value_to_add is not None:
                    position = (
                        position[0] + value_to_add,
                        depending_position[0] + margin,
                    )
                else:
                    position = (position[0], depending_position[0] + margin)
        else:
            if depending is not None:
                depending_position = get_coordinates(
                    np.array(card_pil), [254, 254, 254, 255], last_x=False, last_y=True
                )
                if value_to_add is not None:
                    position = (
                        position[0] + value_to_add,
                        depending_position[0] + margin,
                    )
                else:
                    position = (position[0], depending_position[0] + margin)

        if name == PictureName.SHIRT_FACE.value:
            value_pil = Image.fromarray(value.astype("uint8"), "RGBA")
            card_pil.paste(value_pil, position, value_pil)

        elif name == PictureName.STAR.value:
            number_filled_star = int(int(self.global_note) / 20)
            percent_stay_star = int(((int(self.global_note) % 20) * 100) / 20) / 100

            loop = coordinates_part.get("loop")
            direction = coordinates_part.get("direction")

            width_shift = (
                -(width + 25) if direction == Direction.LEFT.value else (width + 25)
            )
            for i in range(1, loop + 1):
                percent_star_pil = None

                if i > number_filled_star:
                    replace_color_not_equal(
                        value,
                        np.array([255, 255, 255, 0]),
                        np.array(
                            [STAR_COLOR[2], STAR_COLOR[1], STAR_COLOR[0], opacity]
                        ),
                    )
                if i == number_filled_star + 1 and percent_stay_star != 0:
                    percent_star = value.copy()
                    replace_color_not_equal(
                        percent_star,
                        np.array([255, 255, 255, 0]),
                        np.array([STAR_COLOR[0], STAR_COLOR[1], STAR_COLOR[2], 255]),
                    )
                    right_x = percent_star.shape[1] - int(
                        percent_star.shape[1] * percent_stay_star
                    )
                    percent_star[:, 0:right_x] = np.array([255, 255, 255, 0])
                    percent_star_pil = Image.fromarray(
                        percent_star.astype("uint8"), "RGBA"
                    )

                value_pil = Image.fromarray(
                    open_cv.cvtColor(value.astype("uint8"), open_cv.COLOR_RGBA2BGRA),
                    "RGBA",
                )

                card_pil.paste(value_pil, position, value_pil)
                if percent_star_pil is not None:
                    card_pil.paste(percent_star_pil, position, percent_star_pil)
                position = (position[0] + width_shift, position[1])

        elif name == PictureName.FLAG_AND_CREST.value:

            childs = coordinates_part.get("childs")
            flag = childs[0]
            crest = childs[-1]

            flag_and_crest_part = np.full(
                (card_pil.size[1], card_pil.size[0], 4),
                np.array([255, 255, 255, 0]),
                dtype=np.uint8,
            )
            flag_and_crest_part_pil = Image.fromarray(
                flag_and_crest_part.astype("uint8")
            )

            flag_picture = getattr(self, flag.get("value"))
            flag_picture = self.resize(
                flag_picture, flag.get("resize"), flag.get("resize_orientation")
            )
            flag_picture_pil = Image.fromarray(flag_picture, "RGBA")
            flag_margin = flag.get("margin")
            flag_and_crest_part_pil.paste(
                flag_picture_pil,
                (position[0] - int(flag_picture.shape[1]) - flag_margin, 0),
                flag_picture_pil,
            )

            with_text = crest.get("with_text")
            club_part = np.full(
                (card_pil.size[1], card_pil.size[0], 4),
                np.array([255, 255, 255, 0]),
                dtype=np.uint8,
            )
            club_part_pil = Image.fromarray(club_part.astype("uint8"))

            crest_picture = getattr(self, crest.get("value"))
            crest_picture = self.resize(
                crest_picture, crest.get("resize"), crest.get("resize_orientation")
            )
            crest_pil = Image.fromarray(crest_picture)
            club_part_pil.paste(
                crest_pil, (position[0] - int(crest_picture.shape[1] / 2), 0), crest_pil
            )
            text = getattr(self, with_text)
            draw_crest = ImageDraw.Draw(club_part_pil)
            font = ImageFont.truetype(self.font_path, 96)
            draw_crest.text(
                (position[0], crest_picture.shape[0] + 50),
                text,
                font=font,
                fill=(254, 254, 254, 255),
                spacing=0,
                anchor=Anchor.TOP_MIDDLE.value,
            )
            club_part = np.array(club_part_pil)
            replace_color(
                club_part,
                np.array([255, 255, 255, 255]),
                np.array([255, 255, 255, 0]),
                channel=4,
            )
            crest_margin = flag.get("margin")
            position_crest = (0 + int(crest_picture.shape[1]) + crest_margin, 0)

            club_part_pil = Image.fromarray(
                open_cv.cvtColor(club_part, open_cv.COLOR_RGBA2BGRA).astype("uint8")
            )
            flag_and_crest_part_pil.paste(club_part_pil, position_crest, club_part_pil)

            card_pil.paste(
                flag_and_crest_part_pil, (0, position[1]), flag_and_crest_part_pil
            )
        else:
            value_pil = Image.fromarray(value.astype("uint8"), "RGBA")
            card_pil.paste(value_pil, position, value_pil)
            with_text = coordinates_part.get("with_text")
            if with_text is not None:
                text = getattr(self, with_text)
                draw_note = ImageDraw.Draw(card_pil)
                font = ImageFont.truetype(self.font_path, self.font_size_note)
                draw_note.text(
                    (coordinates[1], position[1] + value.shape[0] + 50),
                    text,
                    font=font,
                    fill=(254, 254, 254, 255),
                    spacing=0,
                    anchor=Anchor.TOP_MIDDLE.value,
                )

    def resize(self, value: np.array, resize: int, orientation: int) -> np.array:
        """Redimensionne la carte.

        Args:
            value (np.array): valeur.
            resize (int): valeur de redimension.
            orientation (int): orientation.

        Returns:
            np.array: carte redimensionnée.
        """
        if orientation == OrientationResize.WIDTH.value:
            value = imutils.resize(value, width=resize, inter=open_cv.INTER_AREA)
        elif orientation == OrientationResize.HEIGHT.value:
            value = imutils.resize(value, height=resize, inter=open_cv.INTER_AREA)
        return value
