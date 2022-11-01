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

File: app/generation_nft/libraries/face/face_styling/parts/neck.py
"""
import warnings

import cv2 as open_cv
import numpy as np
from PIL import Image

from app.generation_nft.utils import draw_contours, get_shade_color

warnings.filterwarnings("ignore")


class NeckDrawing(object):
    """Classe pour styliser le cou."""

    def __init__(self):
        """Initialise la classe du style pour le cou."""
        pass

    def draw_neck(
        self,
        name: str,
        new_face_minimize: np.array,
        landmarks: list,
        parts: list,
        face_shape: tuple,
        coordinates: tuple,
        **_
    ) -> np.array:
        """Dessine le cou.

        Args:
            name (str): nom.
            new_face_minimize (np.array): visage.
            landmarks (list): coordonnées du visage.
            parts (list): parties du visage.
            face_shape (tuple): forme du visage.
            coordinates (tuple): coordonnées.

        Returns:
            np.array: visage avec le cou dessiné.
        """
        copy_face_minimize = new_face_minimize.copy()

        (
            y_top,
            _,
            x_left,
            x_right,
        ) = coordinates
        copy_face_minimize = self.resize_natif(
            copy_face_minimize, face_shape, x_left, y_top
        )

        neck_landmarks = list(landmarks).copy()

        neck_points = [
            [neck_landmarks[point].get("x"), neck_landmarks[point].get("y")]
            for point in parts
        ]

        first_point_max_y, second_point_max_y = max(
            np.where(
                np.all(
                    [
                        copy_face_minimize[:, neck_points[0][0]][:, 0]
                        == int(self.skin_color[0]),
                        copy_face_minimize[:, neck_points[0][0]][:, 1]
                        == int(self.skin_color[1]),
                        copy_face_minimize[:, neck_points[0][0]][:, 2]
                        == int(self.skin_color[2]),
                    ],
                    axis=0,
                )
            )[0]
        ), max(
            np.where(
                np.all(
                    [
                        copy_face_minimize[:, neck_points[1][0]][:, 0]
                        == int(self.skin_color[0]),
                        copy_face_minimize[:, neck_points[1][0]][:, 1]
                        == int(self.skin_color[1]),
                        copy_face_minimize[:, neck_points[1][0]][:, 2]
                        == int(self.skin_color[2]),
                    ],
                    axis=0,
                )
            )[0]
        )

        neck_points[0][1] = (
            first_point_max_y
            if first_point_max_y < second_point_max_y
            else second_point_max_y
        )
        neck_points[-1][1] = (
            first_point_max_y
            if first_point_max_y < second_point_max_y
            else second_point_max_y
        )

        new_bottom_y = (
            max(np.where(copy_face_minimize[:, :] == self.skin_color)[0]) + 75
        )
        neck_points.insert(1, [neck_points[0][0], new_bottom_y])
        neck_points.insert(2, [neck_points[-1][0], new_bottom_y])
        neck_points.append([neck_points[-1][0], neck_points[0][1]])
        neck_points.append(neck_points[0])

        first_point, second_point, third_point, fourth_point = (
            neck_points[0],
            neck_points[1],
            neck_points[2],
            neck_points[3],
        )

        neck_coordinates = np.unique(
            np.array(neck_points).reshape(-1, np.array(neck_points).shape[1]), axis=0
        ).reshape((-1, 1, 2))
        neck_coordinates = np.array(
            [
                neck_coordinates[0],
                neck_coordinates[1],
                neck_coordinates[3],
                neck_coordinates[2],
            ]
        )

        virgin_neck_part = np.full(
            (
                face_shape[0] if new_bottom_y < face_shape[0] else new_bottom_y + 1,
                face_shape[1],
                3,
            ),
            255,
            dtype=np.uint8,
        )

        open_cv.polylines(
            virgin_neck_part, [neck_coordinates], True, self.real_black_color, 1
        )

        _, neck_contours = draw_contours(
            virgin_neck_part, virgin_neck_part, self.real_black_color, open_cv.FILLED
        )

        self.neck_color = get_shade_color(self.skin_color, 4)

        open_cv.drawContours(
            virgin_neck_part,
            neck_contours,
            -1,
            (int(self.neck_color[0]), int(self.neck_color[1]), int(self.neck_color[2])),
            open_cv.FILLED,
        )
        open_cv.line(
            virgin_neck_part, first_point, second_point, self.real_black_color, 2
        )
        open_cv.line(
            virgin_neck_part, third_point, fourth_point, self.real_black_color, 2
        )

        copy_face_minimize_pil = self.convert_to_pil_with_transparent_background(
            copy_face_minimize
        )
        neck_mask_part_pil = Image.fromarray(
            open_cv.cvtColor(virgin_neck_part, open_cv.COLOR_BGR2RGBA).astype("uint8"),
            "RGBA",
        )
        neck_mask_part_pil.paste(copy_face_minimize_pil, (0, 0), copy_face_minimize_pil)

        neck_params = {
            "second_point": (second_point[0] - x_left, second_point[1]),
            "third_point": (third_point[0] - x_left, third_point[1]),
            "neck_color": self.neck_color,
        }

        return (
            open_cv.cvtColor(np.array(neck_mask_part_pil), open_cv.COLOR_RGBA2BGR)[
                y_top:new_bottom_y, x_left:x_right
            ],
            neck_params,
        )
