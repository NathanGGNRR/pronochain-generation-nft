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

File: app/generation_nft/libraries/face/face_styling/parts/brow.py
"""
import warnings

import cv2 as open_cv
import numpy as np
from PIL import Image

from app.generation_nft.utils import replace_color

warnings.filterwarnings("ignore")


class BrowDrawing(object):
    """Classe pour styliser les sourcils."""

    def __init__(self):
        """Initialise la classe du style pour les sourcils."""
        pass

    def draw_brow(
        self,
        face: np.array,
        new_face_minimize: np.array,
        contour: list,
        mask_part: np.array,
        **_
    ) -> np.array:
        """Dessine les sourcils.

        Args:
            face (np.array): visage.
            new_face_minimize (np.array): visage dupliqué minimisé.
            contour (list): contour.
            mask_part (np.array): mask des parties.

        Returns:
            np.array: visage avec les sourcils dessinés.
        """
        face_copy = face.copy()
        face_minimize_copy = new_face_minimize.copy()

        open_cv.drawContours(
            face_minimize_copy,
            contour,
            -1,
            (int(self.hair_color[0]), int(self.hair_color[1]), int(self.hair_color[2])),
            open_cv.FILLED,
        )

        mask_pil = self.convert_to_pil_with_transparent_background(face_minimize_copy)
        mask_part_pil = Image.fromarray(
            open_cv.cvtColor(new_face_minimize, open_cv.COLOR_BGR2RGBA).astype("uint8"),
            "RGBA",
        )
        mask_part_pil.paste(mask_pil, (0, 0), mask_pil)

        new_face_minimize = open_cv.cvtColor(
            np.array(mask_part_pil), open_cv.COLOR_RGBA2BGR
        )
        open_cv.drawContours(new_face_minimize, contour, -1, self.real_black_color, 2)

        self.real_brow_mask = open_cv.bitwise_and(face_copy, face_copy, mask=mask_part)
        replace_color(self.real_brow_mask, self.real_black_color, self.white_color)

        return new_face_minimize
