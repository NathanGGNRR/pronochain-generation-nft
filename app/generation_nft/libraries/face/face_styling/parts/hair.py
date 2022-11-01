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

File: app/generation_nft/libraries/face/face_styling/parts/hair.py
"""
import warnings

import cv2 as open_cv
import numpy as np
from PIL import Image

from app.generation_nft.utils import replace_color, where

warnings.filterwarnings("ignore")


class HairDrawing(object):
    """Classe pour styliser les cheveux."""

    def __init__(self):
        """Initialise la classe du style pour les cheveux."""
        pass

    def draw_hair(
        self,
        face: np.array,
        new_face_minimize: np.array,
        mask_part: np.array,
        contour: list,
        **_
    ) -> np.array:
        """Dessine les cheveux du visage.

        Args:
            face (np.array): visage.
            new_face_minimize (np.array): visage dupliqué minimisé.
            mask_part (np.array): mask du visage.
            contour (list): contour des cheveux.

        Returns:
            np.array: visage avec les cheveux dessinés.
        """
        face_copy = face.copy()
        face_minimize_copy = new_face_minimize.copy()
        virgin_mask_part = np.full(
            (face_minimize_copy.shape[0], face_minimize_copy.shape[1], 3),
            255,
            dtype=np.uint8,
        )

        open_cv.drawContours(
            face_minimize_copy,
            contour,
            -1,
            (int(self.hair_color[0]), int(self.hair_color[1]), int(self.hair_color[2])),
            open_cv.FILLED,
        )
        open_cv.drawContours(
            virgin_mask_part,
            contour,
            -1,
            (int(self.hair_color[0]), int(self.hair_color[1]), int(self.hair_color[2])),
            open_cv.FILLED,
        )
        open_cv.drawContours(virgin_mask_part, contour, -1, self.real_black_color, 1)

        hair_count, _, _ = where(face_minimize_copy, self.hair_color, count=True)
        if hair_count < 15000:
            replace_color(face_minimize_copy, self.hair_color, self.white_color)
            replace_color(virgin_mask_part, self.hair_color, self.white_color)
            replace_color(virgin_mask_part, self.real_black_color, self.white_color)
            self.no_hair = True

        hair_mask_pil = self.convert_to_pil_with_transparent_background(
            face_minimize_copy
        )
        mask_part_pil = Image.fromarray(
            open_cv.cvtColor(new_face_minimize, open_cv.COLOR_BGR2RGBA).astype("uint8"),
            "RGBA",
        )
        mask_part_pil.paste(hair_mask_pil, (0, 0), hair_mask_pil)

        new_face_minimize = open_cv.cvtColor(
            np.array(mask_part_pil), open_cv.COLOR_RGBA2BGR
        )
        open_cv.drawContours(new_face_minimize, contour, -1, self.real_black_color, 2)

        real_hair_mask = open_cv.bitwise_and(face_copy, face_copy, mask=mask_part)
        replace_color(real_hair_mask, self.real_black_color, self.white_color)
        return new_face_minimize, virgin_mask_part, real_hair_mask
