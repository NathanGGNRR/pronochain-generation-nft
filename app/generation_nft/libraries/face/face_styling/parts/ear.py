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

File: app/generation_nft/libraries/face/face_styling/parts/ear.py
"""
import warnings

import cv2 as open_cv
import numpy as np
from PIL import Image

warnings.filterwarnings("ignore")


class EarDrawing(object):
    """Classe pour styliser les oreilles."""

    def __init__(self):
        """Initialise la classe du style pour les oreilles."""
        pass

    def draw_ear(self, new_face_minimize: np.array, contour: list, **_) -> np.array:
        """Dessine les oreilles du visage.

        Args:
            new_face_minimize (np.array): visage.
            contour (list): contour.

        Returns:
            np.array: visage avec les oreilles dessinées.
        """
        copy_face_minimize = new_face_minimize.copy()

        open_cv.drawContours(
            copy_face_minimize,
            contour,
            -1,
            (int(self.skin_color[0]), int(self.skin_color[1]), int(self.skin_color[2])),
            open_cv.FILLED,
        )

        mask_pil = self.convert_to_pil_with_transparent_background(copy_face_minimize)
        mask_part_pil = Image.fromarray(
            open_cv.cvtColor(new_face_minimize, open_cv.COLOR_BGR2RGBA).astype("uint8"),
            "RGBA",
        )
        mask_part_pil.paste(mask_pil, (0, 0), mask_pil)

        new_face_minimize = open_cv.cvtColor(
            np.array(mask_part_pil), open_cv.COLOR_RGBA2BGR
        )
        open_cv.drawContours(new_face_minimize, contour, -1, self.real_black_color, 2)
        return new_face_minimize
