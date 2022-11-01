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

File: app/generation_nft/libraries/face/face_styling/parts/mouth.py
"""
import warnings

import cv2 as open_cv
import numpy as np
from mediapipe.python.solutions import face_mesh as mediapipe_fm
from mediapipe.python.solutions.drawing_utils import DrawingSpec

from app.generation_nft.utils import draw_landmarks, replace_color

warnings.filterwarnings("ignore")


class MouthDrawing(object):
    """Classe pour styliser la bouche."""

    def __init__(self):
        """Initialise la classe du style pour la bouche."""
        pass

    def draw_mouth(
        self,
        name: str,
        new_face_minimize: np.array,
        contour_depend_mask: np.array,
        contour_depend_on: list,
        landmarks: list,
        parts: list,
        face_shape: tuple,
        coordinates: tuple,
        **_
    ) -> np.array:
        """Dessine la bouche du visage.

        Args:
            name (str): nom.
            new_face_minimize (np.array): visage.
            contour_depend_mask (np.array): mask de la partie dont dépend la bouche.
            contour_depend_on (list): contour de la partie dont dépend la bouche.
            landmarks (list): coordonnées du visage.
            parts (list): parties du visage.
            face_shape (tuple): forme du visage.
            coordinates (tuple): coordonnées.

        Returns:
            np.array: visage avec la bouche dessinée.
        """
        new_contour_depend_mask = contour_depend_mask.copy()
        copy_face_minimize = new_face_minimize.copy()

        (
            y_top,
            y_bottom,
            x_left,
            x_right,
        ) = coordinates
        copy_face_minimize = self.resize_natif(
            copy_face_minimize, face_shape, x_left, y_top
        )
        new_contour_depend_mask = self.resize_natif(
            new_contour_depend_mask, face_shape, x_left, y_top
        )

        mouth_landmarks = list(landmarks).copy()

        virgin_mask_part = np.full(
            (face_shape[0], face_shape[1], 3),
            255,
            dtype=np.uint8,
        )
        virgin_intern_mouth_mask = np.full(
            (face_shape[0], face_shape[1], 1),
            0,
            dtype=np.uint8,
        )
        open_cv.drawContours(
            virgin_intern_mouth_mask, contour_depend_on, -1, 1, open_cv.FILLED
        )
        _, inter_mouth_contours = self.draw_line_contours(
            name, virgin_mask_part, parts[-1], mouth_landmarks
        )
        open_cv.drawContours(
            virgin_intern_mouth_mask, inter_mouth_contours, -1, 0, open_cv.FILLED
        )

        new_contour_depend_mask = open_cv.bitwise_and(
            new_contour_depend_mask,
            new_contour_depend_mask,
            mask=virgin_intern_mouth_mask,
        )
        replace_color(new_contour_depend_mask, self.real_black_color, self.white_color)

        open_cv.drawContours(
            copy_face_minimize,
            contour_depend_on,
            -1,
            (int(self.skin_color[0]), int(self.skin_color[1]), int(self.skin_color[2])),
            10,
            open_cv.LINE_AA,
        )
        open_cv.drawContours(
            copy_face_minimize,
            contour_depend_on,
            -1,
            (
                int(self.mouth_color[0]),
                int(self.mouth_color[1]),
                int(self.mouth_color[2]),
            ),
            open_cv.FILLED,
        )
        open_cv.drawContours(
            copy_face_minimize,
            inter_mouth_contours,
            -1,
            (254, 254, 254),
            open_cv.FILLED,
        )

        draw_landmarks(
            image=copy_face_minimize,
            landmark_list=mouth_landmarks,
            connection_drawing_spec=DrawingSpec(
                color=self.real_black_color, thickness=1
            ),
            connections=mediapipe_fm.FACEMESH_LIPS,
        )

        return copy_face_minimize[y_top:y_bottom, x_left:x_right]
