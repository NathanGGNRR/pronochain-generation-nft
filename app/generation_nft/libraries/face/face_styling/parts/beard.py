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

File: app/generation_nft/libraries/face/face_styling/parts/beard.py
"""
import warnings
from typing import Optional

import cv2 as open_cv
import numpy as np
from coloraide import Color
from PIL import Image

from app.generation_nft.utils import (
    draw_contours,
    get_unique_colors,
    replace_color,
    rgb_to_hex,
    where,
)

warnings.filterwarnings("ignore")


class BeardDrawing(object):
    """Classe pour styliser la barbe."""

    def __init__(self):
        """Initialise la classe du style pour la barbe."""
        pass

    def draw_beard(
        self,
        face: np.array,
        new_face_minimize: np.array,
        cleaned_face: np.array,
        contour_depend_visual_mask: np.array,
        **_
    ) -> np.array:
        """Dessine la barbe du visage.

        Args:
            face (np.array): visage.
            new_face_minimize (np.array): visage dupliqué minimisé.
            cleaned_face (np.array): visage nettoyé.
            contour_depend_visual_mask (np.array): mask de la partie dont dépend la bouche.

        Returns:
            np.array: visage avec la barbe dessinée.
        """
        face_copy = face.copy()
        cleaned_face_copy = cleaned_face.copy()
        _, coordinates_y, _ = where(contour_depend_visual_mask, self.real_black_color)
        max_y = min(coordinates_y) + int((max(coordinates_y) - min(coordinates_y)) / 2)

        _, before_ear_coordinates_y, before_ear_coordinates_x = where(
            cleaned_face_copy[: min(coordinates_y), :], self.real_black_color
        )
        cleaned_face_copy[
            before_ear_coordinates_y, before_ear_coordinates_x, :
        ] = np.array([255, 255, 255])

        _, white_contours = draw_contours(
            cleaned_face_copy, cleaned_face_copy, self.temp_white_color, open_cv.FILLED
        )
        black_face_mask, _ = draw_contours(
            cleaned_face_copy,
            cleaned_face_copy,
            self.real_black_color,
            open_cv.FILLED,
            as_mask=True,
        )
        open_cv.drawContours(black_face_mask, white_contours, -1, 0, open_cv.FILLED)

        face_cleaned_mask = open_cv.bitwise_and(
            face_copy, face_copy, mask=black_face_mask
        )
        replace_color(face_cleaned_mask, self.real_black_color, self.white_color)
        face_cleaned_check_beard = face_cleaned_mask.copy()

        if self.no_hair:
            pilosity_color = get_unique_colors(
                self.real_brow_mask, with_frequency_count=True
            )[0]
        else:
            pilosity_color = get_unique_colors(
                self.real_hair_mask, with_frequency_count=True
            )[0]

        rgb_pilosity_hex_color = rgb_to_hex(
            pilosity_color.get("color"), convert_bgr_to_rgb=True
        )

        face_cleaned_check_beard_pil = Image.fromarray(
            open_cv.cvtColor(face_cleaned_check_beard, open_cv.COLOR_BGR2RGB).astype(
                "uint8"
            ),
            "RGB",
        )
        face_cleaned_check_beard_pil = face_cleaned_check_beard_pil.convert(
            "P", palette=Image.ADAPTIVE, colors=200
        )
        face_cleaned_check_beard = open_cv.cvtColor(
            np.array(face_cleaned_check_beard_pil.convert("RGB")), open_cv.COLOR_BGR2RGB
        )

        bottom_face_colors = get_unique_colors(face_cleaned_check_beard)
        color_distances = []
        for bottom_face_color in bottom_face_colors:
            color = bottom_face_color.get("color")
            hex_color = rgb_to_hex(color, convert_bgr_to_rgb=True)
            color_distances.append(
                int(Color(hex_color).delta_e(rgb_pilosity_hex_color))
            )

        average_distance = int(np.mean(color_distances))
        min_pilosity_distance = min(color_distances)

        if (
            average_distance >= 20
            and (min_pilosity_distance * 100 / average_distance) < 5.0
        ):
            beard_cleaned_pil = Image.fromarray(
                open_cv.cvtColor(face_cleaned_mask, open_cv.COLOR_BGR2RGB).astype(
                    "uint8"
                ),
                "RGB",
            )
            beard_cleaned_pil = beard_cleaned_pil.convert(
                "P", palette=Image.ADAPTIVE, colors=3
            )
            beard_cleaned = open_cv.cvtColor(
                np.array(beard_cleaned_pil.convert("RGB")), open_cv.COLOR_BGR2RGB
            )

            beard_colors = get_unique_colors(beard_cleaned)
            beard_colors.pop()
            beard_color = beard_colors[0].get("color")
            skin_color = beard_colors[-1].get("color")

            self.remove_contours(beard_cleaned, skin_color, self.real_black_color, 50)
            replace_color(beard_cleaned, skin_color, self.white_color)
            self.remove_contours(
                beard_cleaned, beard_color, self.white_color, 50, max_y
            )
            replace_color(beard_cleaned, beard_color, self.real_black_color)

            indices = np.where(
                np.all(
                    [
                        cleaned_face_copy[min(coordinates_y), :] == 0,
                        cleaned_face_copy[min(coordinates_y), :] == 0,
                        cleaned_face_copy[min(coordinates_y), :] == 0,
                    ],
                    axis=0,
                )
            )
            min_x, max_x = min(indices[0]), max(indices[0])

            left_first_point = (min_x, min(coordinates_y))
            left_second_point, left_third_second_point = (
                min_x + 100,
                min(coordinates_y),
            ), (min_x + 150, min(coordinates_y) + 150)
            left_points = np.array(
                [left_first_point, left_second_point, left_third_second_point]
            )
            open_cv.polylines(beard_cleaned, [left_points], True, self.black_color, 1)
            _, new_left_points_contours = draw_contours(
                beard_cleaned, beard_cleaned, self.black_color, open_cv.FILLED
            )
            open_cv.drawContours(
                beard_cleaned,
                new_left_points_contours,
                -1,
                self.white_color,
                open_cv.FILLED,
            )

            right_first_point = (max_x, min(coordinates_y))
            right_second_point, right_third_second_point = (
                max_x - 100,
                min(coordinates_y),
            ), (max_x - 150, min(coordinates_y) + 150)
            right_points = np.array(
                [right_first_point, right_second_point, right_third_second_point]
            )
            open_cv.polylines(beard_cleaned, [right_points], True, self.black_color, 1)
            _, new_right_points_contours = draw_contours(
                beard_cleaned, beard_cleaned, self.black_color, open_cv.FILLED
            )
            open_cv.drawContours(
                beard_cleaned,
                new_right_points_contours,
                -1,
                self.white_color,
                open_cv.FILLED,
            )

            _, beard_contours = draw_contours(
                beard_cleaned, beard_cleaned, self.real_black_color, open_cv.FILLED
            )
            replace_color(
                beard_cleaned,
                self.real_black_color,
                (
                    int(self.hair_color[0]),
                    int(self.hair_color[1]),
                    int(self.hair_color[2]),
                ),
            )
            open_cv.drawContours(
                beard_cleaned, beard_contours, -1, self.real_black_color, 1
            )

            final_contours = self.remove_contours(
                beard_cleaned,
                self.white_color,
                None,
                None,
                get_all_without_biggest=True,
            )
            final_contours = [
                final_contour.get("contour") for final_contour in final_contours[1:]
            ]
            open_cv.drawContours(
                beard_cleaned, np.array(final_contours), -1, self.real_black_color, 1
            )

            self.drawing_beard = beard_cleaned

        return new_face_minimize

    def remove_contours(
        self,
        mask: np.array,
        color_to_remove: tuple,
        color_to_replace: Optional[tuple],
        under: int,
        max_y: int = None,
        get_all_without_biggest: bool = False,
    ) -> Optional[list]:
        """Supprime les contours en trop.

        Args:
            mask (np.array): mask.
            color_to_remove (tuple): couleur à supprimée.
            color_to_replace (tuple): couleur qui remplace la couleur supprimée.
            under (int): seuil sous lequel est supprimé le contour.
            max_y (int, optional): y maximum. Défaut à None.
            get_all_without_biggest (bool, optional): récupère tout sans le plus grand contour ? Défaut à False.

        Returns:
            Optional[list]: _description_
        """
        _, contours = draw_contours(mask, mask, color_to_remove, 1)
        final_contours = []
        for contour in contours:
            virgin_mask_contour = np.full(
                (mask.shape[0], mask.shape[1], 3),
                255,
                dtype=np.uint8,
            )
            open_cv.drawContours(
                virgin_mask_contour,
                np.array(contour),
                -1,
                (self.real_black_color),
                open_cv.FILLED,
            )
            contour_size, _, _ = where(
                virgin_mask_contour, self.real_black_color, count=True
            )
            if get_all_without_biggest:
                final_contours.append({"count": contour_size, "contour": contour})
            else:
                if contour_size < under:
                    final_contours.append(contour)
                elif max_y is not None:
                    y_values = list(map(lambda x: x[0][1], contour))
                    if max_y > max(y_values):
                        final_contours.append(contour)

        if get_all_without_biggest:
            return sorted(final_contours, key=lambda item: item["count"], reverse=True)
        else:
            if len(final_contours) > 0:
                open_cv.drawContours(
                    mask,
                    np.array(final_contours),
                    -1,
                    (color_to_replace),
                    open_cv.FILLED,
                )
