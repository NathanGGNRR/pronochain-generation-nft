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

File: app/generation_nft/libraries/face/face_resizing/face_resizing.py
"""
import warnings

import cv2 as open_cv
import numpy as np
from PIL import Image

from app import logger
from app.exceptions import PronochainException
from app.generation_nft.libraries.face.face_landmarks.constants import (
    LEFT_NECK,
    RIGHT_NECK,
)
from app.generation_nft.libraries.face.face_resizing.constants import (
    WIDTH_LANDMARK_REFERENCE,
    WIDTH_PARSING_REFERENCE,
)
from app.generation_nft.utils import get_dimension_to_append, resize_parsing

warnings.filterwarnings("ignore")


class FaceResizing(object):
    """Classe pour uniformiser le visage."""

    def __init__(self):
        """Initialise la classe pour uniformiser le visage."""
        pass

    def face_parsing_resizing(self, face: np.array) -> np.array:
        """Redimensionne la prédiction des parties du visage.

        Args:
            face (np.array): prédiction visage.

        Returns:
            np.array: prédiction visage redimensionné.
        """
        cropped_face = self.face_parsing(face, to_resize=True)
        face_pil = Image.fromarray(
            open_cv.cvtColor(cropped_face, open_cv.COLOR_BGR2RGB).astype("uint8"), "RGB"
        )

        (height, width, _) = cropped_face.shape
        new_width = WIDTH_PARSING_REFERENCE
        new_height = int(new_width * height / width)

        if width != new_width:
            face_pil = face_pil.resize(
                (WIDTH_PARSING_REFERENCE, new_height), Image.ANTIALIAS
            )

        dimension_to_substract = None
        if WIDTH_PARSING_REFERENCE != new_height:
            (dimension_to_substract, less_width, less_height) = get_dimension_to_append(
                new_height, WIDTH_PARSING_REFERENCE
            )

            if less_width:
                face_pil = face_pil.crop(
                    (0, 0, WIDTH_PARSING_REFERENCE - 1, new_height)
                )

            if less_height:
                face_pil = face_pil.crop(
                    (0, 0, WIDTH_PARSING_REFERENCE, new_height - 1)
                )

        new_face = open_cv.cvtColor(
            np.array(face_pil.convert("RGB")), open_cv.COLOR_BGR2RGB
        )
        if dimension_to_substract is not None:
            new_face = resize_parsing(new_face, dimension_to_substract)
        return new_face

    def face_landmark_resizing(self, face_resized: np.array) -> tuple:
        """Redimensionne le visage avec les coordonnées de différentes parties.

        Args:
            face_resized (np.array): visage à redimensionner.

        Raises:
            PronochainException: aucunes coordonnées détectées.
            PronochainException: aucunes coordonnées détectées.

        Returns:
            tuple: visage redimensionné, coordonnées et coordonnées normalisées.
        """
        result_landmark_points, normalized_landmark_points = self.face_landmark(
            face_resized, check=False
        )

        if result_landmark_points is None:
            logger.info(
                f"Aucun landmarks detecte pour l'image du joueur {self.player.code}, arret du processus pour ce visage."
            )
            raise PronochainException

        while (
            normalized_landmark_points[RIGHT_NECK].get("x")
            - normalized_landmark_points[LEFT_NECK].get("x")
        ) < WIDTH_LANDMARK_REFERENCE - 2 or (
            normalized_landmark_points[RIGHT_NECK].get("x")
            - normalized_landmark_points[LEFT_NECK].get("x")
        ) > WIDTH_LANDMARK_REFERENCE + 2:
            face_pil = Image.fromarray(
                open_cv.cvtColor(face_resized, open_cv.COLOR_BGR2RGB).astype("uint8"),
                "RGB",
            )

            width_difference = WIDTH_LANDMARK_REFERENCE - (
                normalized_landmark_points[RIGHT_NECK].get("x")
                - normalized_landmark_points[LEFT_NECK].get("x")
            )
            (height, width, _) = face_resized.shape
            new_width = face_resized.shape[1] + width_difference
            new_height = int(new_width * height / width)

            if width_difference != 0:
                face_pil = face_pil.resize((new_width, new_height), Image.ANTIALIAS)

            dimension_to_substract = None
            if new_width != new_height:
                (
                    dimension_to_substract,
                    less_width,
                    less_height,
                ) = get_dimension_to_append(new_height, new_width)

                if less_width:
                    face_pil = face_pil.crop((0, 0, new_width - 1, new_height))

                if less_height:
                    face_pil = face_pil.crop((0, 0, new_width, new_height - 1))

            face_resized = open_cv.cvtColor(
                np.array(face_pil.convert("RGB")), open_cv.COLOR_BGR2RGB
            )
            if dimension_to_substract is not None:
                face_resized = resize_parsing(face_resized, dimension_to_substract)

            result_landmark_points, normalized_landmark_points = self.face_landmark(
                face_resized, check=False
            )

            if result_landmark_points is None:
                logger.info(
                    f"Aucun landmarks detecte pour l'image du joueur {self.player.code}, arret du processus pour ce visage."
                )
                raise PronochainException

        return face_resized, result_landmark_points, normalized_landmark_points
