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

File: app/generation_nft/libraries/face/face_styling/parts/nose.py
"""
import warnings

import cv2 as open_cv
import numpy as np

from app.generation_nft.libraries.face.face_landmarks.constants import DRAWING_NOSE
from app.generation_nft.utils import draw_contours

warnings.filterwarnings("ignore")


class NoseDrawing(object):
    """Classe pour styliser le nez."""

    def __init__(self):
        """Initialise la classe du style pour le nez."""
        pass

    def draw_nose(
        self,
        new_face_minimize: np.array,
        landmarks: list,
        coordinates: tuple,
        face_shape: tuple,
        parts: list,
        **_
    ) -> np.array:
        """Dessine le nez du visage.

        Args:
            new_face_minimize (np.array): visage.
            landmarks (list): coordonnées des parties du visage.
            coordinates (tuple): coordonnées.
            face_shape (tuple): forme du visage.
            parts (list): parties du visages.

        Returns:
            np.array: visage avec le nez dessiné.
        """
        copy_face_minimize = new_face_minimize.copy()
        nose_landmarks = list(landmarks).copy()

        (
            y_top,
            y_bottom,
            x_left,
            x_right,
        ) = coordinates
        mask_part = self.resize_natif(copy_face_minimize, face_shape, x_left, y_top)

        virgin_down_nose_part = np.full(
            (face_shape[0], face_shape[1], 3),
            255,
            dtype=np.uint8,
        )
        down_nose_points_length = len(parts[0])
        for i in range(down_nose_points_length):
            next_i = i + 1
            if next_i > down_nose_points_length - 1:
                break
            first_point_x, first_point_y = nose_landmarks[parts[0][i]].get(
                "x"
            ), nose_landmarks[parts[0][i]].get("y")
            second_point_x, second_point_y = nose_landmarks[parts[0][next_i]].get(
                "x"
            ), nose_landmarks[parts[0][next_i]].get("y")
            open_cv.line(
                virgin_down_nose_part,
                (first_point_x, first_point_y),
                (second_point_x, second_point_y),
                self.black_color,
                1,
            )

        _, down_nose_contours = draw_contours(
            virgin_down_nose_part,
            virgin_down_nose_part,
            [self.black_color[0], self.black_color[1], self.black_color[2]],
            open_cv.FILLED,
        )
        open_cv.drawContours(
            mask_part,
            down_nose_contours,
            -1,
            (int(self.skin_color[0]), int(self.skin_color[1]), int(self.skin_color[2])),
            15,
            open_cv.LINE_AA,
            offset=(0, 5),
        )

        for index, nose_point in enumerate(DRAWING_NOSE[0].get("parts")):
            last = index + 1 > len(DRAWING_NOSE[0].get("parts")) - 1
            if last:
                break
            next_index = index + 1
            next_point = DRAWING_NOSE[0].get("parts")[next_index]
            first_point_x, first_point_y = landmarks[nose_point].get("x"), landmarks[
                nose_point
            ].get("y")
            second_point_x, second_point_y = landmarks[next_point].get("x"), landmarks[
                next_point
            ].get("y")
            open_cv.line(
                mask_part,
                (first_point_x, first_point_y),
                (second_point_x, second_point_y),
                self.black_color,
                1,
                open_cv.LINE_AA,
            )

        nose_mask_parts = self.draw_nose_contour(
            mask_part, DRAWING_NOSE[1:], nose_landmarks
        )
        open_cv.drawContours(
            mask_part,
            nose_mask_parts[0].get("contour"),
            -1,
            self.real_black_color,
            open_cv.FILLED,
        )
        open_cv.drawContours(
            mask_part,
            nose_mask_parts[1].get("contour"),
            -1,
            self.real_black_color,
            open_cv.FILLED,
        )

        return mask_part[y_top:y_bottom, x_left:x_right]

    def draw_nose_contour(
        self, mask_part: np.array, nose_parts: list, nose_landmarks: list
    ) -> list:
        """Dessine les contours du nez.

        Args:
            mask_part (np.array): visage.
            nose_parts (list): parties du nez.
            nose_landmarks (list): coordonnées des parties du nez.

        Returns:
            list: contours du nez.
        """
        nose_mask_parts = []
        for nose in nose_parts:
            name = nose.get("name")
            parts = nose.get("parts")
            close = nose.get("close")
            points = nose.get("points")
            depend_mask_name = nose.get("depend_mask_name")

            nose_mask_part, drawing_contours = self.draw_line_contours(
                name, mask_part, parts, nose_landmarks, close
            )

            contour = []
            for drawing_contour in drawing_contours:
                if len(drawing_contour) == 1:
                    x, y = drawing_contour[0][0][0], drawing_contour[0][0][1]
                    nose_mask_part[y, x] = np.array([255, 255, 255])
                else:
                    contour.append(drawing_contour)

            nose_mask_parts.append(
                {
                    "name": name,
                    "points": points,
                    "mask_part": nose_mask_part,
                    "contour": contour,
                    "depend_mask_name": depend_mask_name,
                }
            )
        return nose_mask_parts
