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

File: app/generation_nft/libraries/shirt/shirt.py
"""
import cv2 as open_cv
import numpy as np
from coloraide import Color
from PIL import Image

from app.generation_nft.libraries.face.face_styling.mixins import DrawingMixin
from app.generation_nft.libraries.shirt.constants import (
    DARK_PEC,
    DARKER_PEC,
    DEFAULT_NECK_HEIGHT,
    LEFT_UP_POINT,
)
from app.generation_nft.utils import draw_contours, replace_color, rgb_to_hex, where


class ShirtStyling(DrawingMixin):
    """Classe permettant de styliser le maillot."""

    def __init__(self):
        """Initialise la classe pour styliser le maillot."""
        self.dark_pec = DARK_PEC
        self.darker_pec = DARKER_PEC
        self.default_neck_height = DEFAULT_NECK_HEIGHT

        self.base_template_shirt, _ = draw_contours(
            self.shirt_picture, self.shirt_picture, (0, 0, 0), 1
        )
        _, self.neck_template_shirt_contours = draw_contours(
            self.shirt_picture,
            open_cv.cvtColor(self.shirt_picture, open_cv.COLOR_BGR2HSV),
            (0, 255, 255),
            1,
        )

        self.neck_color = None

        self.white_color_lighter = np.array([204, 204, 204])
        self.white_color_darker = np.array([179, 179, 179])

    def draw_shirt(self) -> np.array:
        """Dessine le maillot du joueur.

        Returns:
            np.array: maillot.
        """
        self.neck_color = self.neck_params.get("neck_color")

        center_crest_indices = np.where(
            np.all(
                [
                    self.crest_shape[:, :, 0] == 0,
                    self.crest_shape[:, :, 1] == 0,
                    self.crest_shape[:, :, 2] == 255,
                ],
                axis=0,
            )
        )
        self.center_crest_points = list(
            zip(center_crest_indices[0], center_crest_indices[1])
        )[0]

        self.base_template_crest, template_crest_contours = draw_contours(
            self.crest_shape, self.crest_shape, (0, 0, 0), open_cv.FILLED
        )
        open_cv.drawContours(
            self.base_template_crest,
            template_crest_contours,
            -1,
            (254, 254, 254),
            open_cv.FILLED,
        )
        open_cv.drawContours(
            self.base_template_crest, template_crest_contours, -1, (0, 0, 0), 2
        )

        self.base_template_emblem, self.emblem_template_contours = draw_contours(
            self.crest_pattern, self.crest_pattern, (0, 0, 0), open_cv.FILLED
        )

        _, base_contours = draw_contours(
            self.base_template_shirt, self.base_template_shirt, (0, 0, 0), 1
        )

        _, first_color_contours = draw_contours(
            self.shirt_pattern,
            open_cv.cvtColor(self.shirt_pattern, open_cv.COLOR_BGR2HSV),
            (0, 255, 255),
            1,
        )
        _, second_color_contours = draw_contours(
            self.shirt_pattern,
            open_cv.cvtColor(self.shirt_pattern, open_cv.COLOR_BGR2HSV),
            (120, 255, 255),
            1,
        )

        open_cv.drawContours(
            self.base_template_shirt, base_contours, -1, (254, 254, 254), open_cv.FILLED
        )
        open_cv.drawContours(
            self.base_template_shirt,
            first_color_contours,
            -1,
            (
                int(self.first_color[0]),
                int(self.first_color[1]),
                int(self.first_color[2]),
            ),
            open_cv.FILLED,
        )
        open_cv.drawContours(
            self.base_template_shirt,
            second_color_contours,
            -1,
            (
                int(self.second_color[0]),
                int(self.second_color[1]),
                int(self.second_color[2]),
            ),
            open_cv.FILLED,
        )

        shirt_emblem_indices = np.where(
            np.all(
                [
                    self.shirt_picture[:, :, 0] == 0,
                    self.shirt_picture[:, :, 1] == 255,
                    self.shirt_picture[:, :, 2] == 0,
                ],
                axis=0,
            )
        )
        shirt_emblem_points = list(
            zip(shirt_emblem_indices[0], shirt_emblem_indices[1])
        )[0]
        template_crest, crest_height, crest_width = self.draw_crest()

        crest_y, crest_x = (
            shirt_emblem_points[0] - crest_height,
            shirt_emblem_points[1] - crest_width,
        )

        base_template_shirt_pil = self.convert_to_pil_with_transparent_background(
            self.base_template_shirt
        )
        template_crest_pil = self.convert_to_pil_with_transparent_background(
            template_crest
        )
        base_template_shirt_pil.paste(
            template_crest_pil, (crest_x, crest_y), template_crest_pil
        )
        self.base_template_shirt = open_cv.cvtColor(
            np.array(base_template_shirt_pil), open_cv.COLOR_RGBA2BGR
        )

        self.set_pec(self.base_template_shirt)

        open_cv.drawContours(self.base_template_shirt, base_contours, -1, (0, 0, 0), 2)
        open_cv.drawContours(
            self.base_template_shirt,
            self.neck_template_shirt_contours,
            -1,
            (int(self.neck_color[0]), int(self.neck_color[1]), int(self.neck_color[2])),
            open_cv.FILLED,
        )

        height = self.base_template_shirt.shape[0] + self.face_bottom_y
        face_x = LEFT_UP_POINT[1] - self.get_x_min_neck()

        virgin_shirt_part = np.full(
            (height, self.base_template_shirt.shape[1], 3),
            255,
            dtype=np.uint8,
        )

        face_pil = self.convert_to_pil_with_transparent_background(self.drawing_face)
        base_template_shirt_pil = self.convert_to_pil_with_transparent_background(
            self.base_template_shirt
        )

        shirt_part_pil = Image.fromarray(
            open_cv.cvtColor(virgin_shirt_part, open_cv.COLOR_BGR2RGBA).astype("uint8"),
            "RGBA",
        )
        shirt_part_pil.paste(face_pil, (face_x, 0), face_pil)
        shirt_part_pil.paste(
            base_template_shirt_pil, (0, self.face_bottom_y), base_template_shirt_pil
        )

        shirt_part_mask = open_cv.cvtColor(
            np.array(shirt_part_pil), open_cv.COLOR_RGBA2BGR
        )

        _, skin_coordinates_y, _ = where(shirt_part_mask, self.skin_color)
        _, neck_coordinates_y, _ = where(shirt_part_mask, self.neck_color)
        neck_height = self.default_neck_height - (
            max(neck_coordinates_y) - max(skin_coordinates_y)
        )
        if neck_height > 0:
            new_height_mask_part = np.full(
                (
                    self.drawing_face.shape[0] + neck_height,
                    self.drawing_face.shape[1],
                    3,
                ),
                255,
                dtype=np.uint8,
            )
            new_height_mask_part_pil = Image.fromarray(
                open_cv.cvtColor(new_height_mask_part, open_cv.COLOR_BGR2RGBA).astype(
                    "uint8"
                ),
                "RGBA",
            )
            new_first_point, new_second_point = self.neck_params.get(
                "second_point"
            ), self.neck_params.get("third_point")
            new_third_point, new_fourth_point = (
                new_first_point[0],
                new_first_point[1] + neck_height - 1,
            ), (new_second_point[0], new_second_point[1] + neck_height - 1)
            new_neck_points = [
                new_first_point,
                new_third_point,
                new_fourth_point,
                new_second_point,
            ]
            new_neck_coordinates = np.unique(
                np.array(new_neck_points).reshape(
                    -1, np.array(new_neck_points).shape[1]
                ),
                axis=0,
            ).reshape((-1, 1, 2))
            new_neck_coordinates = np.array(
                [
                    new_neck_coordinates[0],
                    new_neck_coordinates[1],
                    new_neck_coordinates[3],
                    new_neck_coordinates[2],
                ]
            )

            open_cv.polylines(
                new_height_mask_part, [new_neck_coordinates], True, (0, 0, 0), 2
            )
            _, new_neck_contours = draw_contours(
                new_height_mask_part, new_height_mask_part, (0, 0, 0), open_cv.FILLED
            )

            open_cv.drawContours(
                new_height_mask_part,
                new_neck_contours,
                -1,
                (
                    int(self.neck_color[0]),
                    int(self.neck_color[1]),
                    int(self.neck_color[2]),
                ),
                open_cv.FILLED,
            )
            open_cv.line(
                new_height_mask_part, new_first_point, new_third_point, (0, 0, 0), 2
            )
            open_cv.line(
                new_height_mask_part, new_second_point, new_fourth_point, (0, 0, 0), 2
            )

            new_height_mask_part_pil = Image.fromarray(
                open_cv.cvtColor(new_height_mask_part, open_cv.COLOR_BGR2RGBA).astype(
                    "uint8"
                ),
                "RGBA",
            )
            new_height_mask_part_pil.paste(face_pil, (0, 0), face_pil)
            face_pil = self.convert_to_pil_with_transparent_background(
                open_cv.cvtColor(
                    np.array(new_height_mask_part_pil), open_cv.COLOR_RGBA2BGR
                )
            )

        final_shirt_part_pil = Image.fromarray(
            open_cv.cvtColor(virgin_shirt_part, open_cv.COLOR_BGR2RGBA).astype("uint8"),
            "RGBA",
        )
        final_shirt_part_pil.paste(face_pil, (face_x, 0), face_pil)
        if self.drawing_beard is not None:
            beard_pil = self.convert_to_pil_with_transparent_background(
                self.drawing_beard
            )
            final_shirt_part_pil.paste(beard_pil, (face_x, 0), beard_pil)
        final_shirt_part_pil.paste(
            base_template_shirt_pil,
            (0, self.face_bottom_y + neck_height),
            base_template_shirt_pil,
        )
        hair_pil = self.convert_to_pil_with_transparent_background(self.drawing_hair)
        final_shirt_part_pil.paste(hair_pil, (face_x, 0), hair_pil)

        virgin_face_contours = np.full(
            (final_shirt_part_pil.size[1], final_shirt_part_pil.size[0], 3),
            255,
            dtype=np.uint8,
        )
        virgin_face_contours_pil = Image.fromarray(
            open_cv.cvtColor(virgin_face_contours, open_cv.COLOR_BGR2RGBA).astype(
                "uint8"
            ),
            "RGBA",
        )
        face_contours_pil = self.convert_to_pil_with_transparent_background(
            self.face_contours
        )
        virgin_face_contours_pil.paste(
            face_contours_pil, (face_x, 0), face_contours_pil
        )
        face_contours_mask = open_cv.cvtColor(
            np.array(virgin_face_contours_pil), open_cv.COLOR_RGBA2BGR
        )
        face_contours_mask, _ = draw_contours(
            face_contours_mask,
            face_contours_mask,
            (0, 0, 0),
            open_cv.FILLED,
            as_mask=True,
        )

        shirt_part_mask = open_cv.cvtColor(
            np.array(final_shirt_part_pil), open_cv.COLOR_RGBA2BGR
        )

        only_face_mask = open_cv.bitwise_and(
            shirt_part_mask, shirt_part_mask, mask=face_contours_mask
        )
        replace_color(only_face_mask, (0, 0, 0), (255, 255, 255))
        _, coordinates_y, coordinates_x = where(only_face_mask, self.neck_color)
        shirt_part_mask[coordinates_y, coordinates_x, :] = self.skin_color

        final_shirt_part_pil = Image.fromarray(
            open_cv.cvtColor(shirt_part_mask, open_cv.COLOR_BGR2RGBA).astype("uint8"),
            "RGBA",
        )
        face_contours_pil = self.convert_to_pil_with_transparent_background(
            self.face_contours
        )
        final_shirt_part_pil.paste(face_contours_pil, (face_x, 0), face_contours_pil)

        shirt_part_mask = np.array(final_shirt_part_pil)

        replace_color(
            shirt_part_mask,
            np.array([255, 255, 255, 255]),
            np.array([255, 255, 255, 0]),
            channel=4,
        )
        shirt_part_mask = shirt_part_mask[: shirt_part_mask.shape[0] + neck_height, :]

        crest_transparent = np.full(
            (self.crest_shape.shape[0], self.crest_shape.shape[1], 4),
            np.array([255, 255, 255, 0]),
            dtype=np.uint8,
        )
        crest_transparent_pil = Image.fromarray(
            open_cv.cvtColor(crest_transparent, open_cv.COLOR_BGRA2RGBA).astype(
                "uint8"
            ),
            "RGBA",
        )
        drawing_crest_pil = self.convert_to_pil_with_transparent_background(
            template_crest
        )
        crest_transparent_pil.paste(drawing_crest_pil, (0, 0), drawing_crest_pil)
        drawing_crest = open_cv.cvtColor(
            np.array(crest_transparent_pil), open_cv.COLOR_RGB2RGBA
        )
        replace_color(
            drawing_crest,
            np.array([255, 255, 255, 255]),
            np.array([255, 255, 255, 0]),
            channel=4,
        )
        return shirt_part_mask, drawing_crest

    def get_x_min_neck(self) -> int:
        """Récupère la coordonnée minimum de x.

        Returns:
            int: minimum x.
        """
        _, _, coordinates_x = where(self.drawing_face, self.neck_color)
        return min(coordinates_x)

    def set_pec(self, template_shirt: np.array):
        """Applique le relief des pectoraux.

        Args:
            template_shirt (np.array): template du maillot.
        """
        first_color_hex, second_color_hex = rgb_to_hex(
            self.first_color, convert_bgr_to_rgb=True
        ), rgb_to_hex(self.second_color, convert_bgr_to_rgb=True)
        first_color_hsl, second_color_hsl = Color(first_color_hex).convert(
            "hsl"
        ).to_string(precision=0).replace("hsl(", "").replace(")", "").split(" "), Color(
            second_color_hex
        ).convert(
            "hsl"
        ).to_string(
            precision=0
        ).replace(
            "hsl(", ""
        ).replace(
            ")", ""
        ).split(
            " "
        )

        new_lighter_first_percent, new_darker_first_percent = (
            last_lighter_value
            if (
                last_lighter_value := int(first_color_hsl[2].replace("%", ""))
                - self.dark_pec
            )
            > 0
            else 0,
            last_darker_value
            if (
                last_darker_value := int(first_color_hsl[2].replace("%", ""))
                - self.darker_pec
            )
            > 0
            else 0,
        )
        lighter_first_color_hsl, darker_first_color_hsl = " ".join(
            [first_color_hsl[0], first_color_hsl[1], f"{new_lighter_first_percent}%"]
        ), " ".join(
            [first_color_hsl[0], first_color_hsl[1], f"{new_darker_first_percent}%"]
        )

        new_lighter_second_percent, new_darker_second_percent = (
            last_lighter_value
            if (
                last_lighter_value := int(second_color_hsl[2].replace("%", ""))
                - self.dark_pec
            )
            > 0
            else 0,
            last_darker_value
            if (
                last_darker_value := int(second_color_hsl[2].replace("%", ""))
                - self.darker_pec
            )
            > 0
            else 0,
        )
        lighter_second_color_hsl, darker_second_color_hsl = " ".join(
            [second_color_hsl[0], second_color_hsl[1], f"{new_lighter_second_percent}%"]
        ), " ".join(
            [second_color_hsl[0], second_color_hsl[1], f"{new_darker_second_percent}%"]
        )

        first_color_lighter, first_color_darker = Color(
            f"hsl({lighter_first_color_hsl})"
        ).convert("srgb").to_string(precision=0).replace("rgb(", "").replace(
            ")", ""
        ).split(
            " "
        ), Color(
            f"hsl({darker_first_color_hsl})"
        ).convert(
            "srgb"
        ).to_string(
            precision=0
        ).replace(
            "rgb(", ""
        ).replace(
            ")", ""
        ).split(
            " "
        )
        first_color_lighter, first_color_darker = np.array(
            [
                int(first_color_lighter[2]),
                int(first_color_lighter[1]),
                int(first_color_lighter[0]),
            ]
        ), np.array(
            [
                int(first_color_darker[2]),
                int(first_color_darker[1]),
                int(first_color_darker[0]),
            ]
        )

        second_color_lighter, second_color_darker = Color(
            f"hsl({lighter_second_color_hsl})"
        ).convert("srgb").to_string(precision=0).replace("rgb(", "").replace(
            ")", ""
        ).split(
            " "
        ), Color(
            f"hsl({darker_second_color_hsl})"
        ).convert(
            "srgb"
        ).to_string(
            precision=0
        ).replace(
            "rgb(", ""
        ).replace(
            ")", ""
        ).split(
            " "
        )
        second_color_lighter, second_color_darker = np.array(
            [
                int(second_color_lighter[2]),
                int(second_color_lighter[1]),
                int(second_color_lighter[0]),
            ]
        ), np.array(
            [
                int(second_color_darker[2]),
                int(second_color_darker[1]),
                int(second_color_darker[0]),
            ]
        )

        lighter_pec_indices = np.where(
            np.all(
                [
                    self.pec_picture[:, :, 0] == 255,
                    self.pec_picture[:, :, 1] == 0,
                    self.pec_picture[:, :, 2] == 0,
                ],
                axis=0,
            )
        )
        for lighter_pec in list(zip(lighter_pec_indices[0], lighter_pec_indices[1])):
            template_shirt_point = template_shirt[lighter_pec[0], lighter_pec[1]]
            if (
                template_shirt_point[0] == int(self.first_color[0])
                and template_shirt_point[1] == int(self.first_color[1])
                and template_shirt_point[2] == int(self.first_color[2])
            ):
                template_shirt[lighter_pec[0], lighter_pec[1]] = first_color_lighter
            elif (
                template_shirt_point[0] == int(self.second_color[0])
                and template_shirt_point[1] == int(self.second_color[1])
                and template_shirt_point[2] == int(self.second_color[2])
            ):
                template_shirt[lighter_pec[0], lighter_pec[1]] = second_color_lighter
            elif (
                template_shirt_point[0] != 0
                and template_shirt_point[1] != 0
                and template_shirt_point[2] != 0
            ):
                template_shirt[
                    lighter_pec[0], lighter_pec[1]
                ] = self.white_color_lighter

        darker_pec_indices = np.where(
            np.all(
                [
                    self.pec_picture[:, :, 0] == 0,
                    self.pec_picture[:, :, 1] == 0,
                    self.pec_picture[:, :, 2] == 255,
                ],
                axis=0,
            )
        )
        for darker_pec in list(zip(darker_pec_indices[0], darker_pec_indices[1])):
            template_shirt_point = template_shirt[darker_pec[0], darker_pec[1]]
            if (
                template_shirt_point[0] == int(self.first_color[0])
                and template_shirt_point[1] == int(self.first_color[1])
                and template_shirt_point[2] == int(self.first_color[2])
            ):
                template_shirt[darker_pec[0], darker_pec[1]] = first_color_darker
            elif (
                template_shirt_point[0] == int(self.second_color[0])
                and template_shirt_point[1] == int(self.second_color[1])
                and template_shirt_point[2] == int(self.second_color[2])
            ):
                template_shirt[darker_pec[0], darker_pec[1]] = second_color_darker
            elif (
                template_shirt_point[0] != 0
                and template_shirt_point[1] != 0
                and template_shirt_point[2] != 0
            ):
                template_shirt[darker_pec[0], darker_pec[1]] = self.white_color_darker

    def draw_crest(self) -> tuple:
        """Dessine l'écusson.

        Returns:
            tuple: l'écusson, la coordonnée x et y de la position de l'écusson.
        """
        center_emblem_indices = np.where(
            np.all(
                [
                    self.crest_pattern[:, :, 0] == 0,
                    self.crest_pattern[:, :, 1] == 0,
                    self.crest_pattern[:, :, 2] == 255,
                ],
                axis=0,
            )
        )
        center_emblem_points = list(
            zip(center_emblem_indices[0], center_emblem_indices[1])
        )[0]

        emblem_y, emblem_x = center_emblem_points[0], center_emblem_points[1]
        crest_y, crest_x = self.center_crest_points[0], self.center_crest_points[1]
        emblem_y, emblem_x = crest_y - emblem_y, crest_x - emblem_x

        replace_color(
            self.crest_content,
            np.array([0, 0, 255]),
            (self.first_color[-1], self.first_color[1], self.first_color[0]),
        )
        replace_color(
            self.crest_content,
            np.array([255, 0, 0]),
            (self.second_color[-1], self.second_color[1], self.second_color[0]),
        )
        _, emblem_contours = draw_contours(
            self.base_template_emblem, self.base_template_emblem, (0, 0, 0), 1
        )
        replace_color(self.base_template_emblem, np.array([0, 0, 0]), self.first_color)
        open_cv.drawContours(
            self.base_template_emblem, emblem_contours, -1, (0, 0, 0), 1
        )

        crest_content = self.convert_to_pil_with_transparent_background(
            self.crest_content
        )
        emblem = self.convert_to_pil_with_transparent_background(
            self.base_template_emblem, convert=False
        )

        crest_template_pil = Image.fromarray(
            open_cv.cvtColor(self.base_template_crest, open_cv.COLOR_RGB2RGBA).astype(
                "uint8"
            ),
            "RGBA",
        )
        crest_template_pil.paste(crest_content, (0, 0), crest_content)
        crest_template_pil.paste(emblem, (emblem_x, emblem_y), emblem)

        return (
            open_cv.cvtColor(np.array(crest_template_pil), open_cv.COLOR_RGBA2RGB),
            crest_y,
            crest_x,
        )
