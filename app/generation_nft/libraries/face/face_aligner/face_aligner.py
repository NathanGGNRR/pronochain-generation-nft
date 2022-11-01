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

File: app/generation_nft/libraries/face/face_aligner/face_aligner.py
"""
import cv2 as open_cv
import numpy as np

from app import logger


class FaceAligner(object):
    """Classe permettant d'aligner le visage de manière a ce qu'elle soit la plus droite possible."""

    def __init__(self):
        """Initialise la classe pour aligner les yeux horizontalement."""
        pass

    def face_align(
        self, face: np.array, left_eye_points: np.array, right_eye_points: np.array
    ) -> np.array:
        """Aligne le visage horizontalement.

        Args:
            face (np.array): face.
            left_eye_points (np.array): coordonnées de l'oeil gauche.
            right_eye_points (np.array): coordonnées de l'oeil droit.

        Raises:
            mass_error: erreur lors de la reprise du centre.
            type_rotation_error: le type des coordonnées doit être en float.
            rotation_error: erreur lors de la rotation.

        Returns:
            np.array: image alignée.
        """
        try:
            # récupère le centre de chaque oeil
            left_eye_center = self.get_mass_center(left_eye_points)
            right_eye_center = self.get_mass_center(right_eye_points)
        except AttributeError as mass_error:
            logger.error(
                f"Le format des coordonnées d'un des yeux n'est pas correcte pour l'image du joueur {self.player.code}.",
                mass_error,
            )
            raise mass_error

        left_eye_center_x, left_eye_center_y, right_eye_center_x, right_eye_center_y = (
            left_eye_center[0],
            left_eye_center[1],
            right_eye_center[0],
            right_eye_center[1],
        )

        # récupère la différence entre chaque coordonnées
        angle_x = right_eye_center_x - left_eye_center_x
        angle_y = right_eye_center_y - left_eye_center_y
        angle = np.degrees(np.arctan2(angle_y, angle_x))

        # récupère la centre des deux eyes
        eyes_center = (
            (left_eye_center_x + right_eye_center_x) // 2,
            (left_eye_center_y + right_eye_center_y) // 2,
        )

        # rotation de l'image
        try:
            transformation_matrix = open_cv.getRotationMatrix2D(eyes_center, angle, 1.0)
        except UnboundLocalError as type_rotation_error:
            logger.error(
                f"Le type des coordonnées du centre des deux yeux est incorrect (float attendu) pour l'image du joueur {self.player.code}.",
                type_rotation_error,
            )
            raise type_rotation_error

        except Exception as rotation_error:
            logger.error(
                f"La rotation a rencontrée une erreur pour l'image du joueur {self.player.code}.",
                rotation_error,
            )
            raise rotation_error

        face_aligned = open_cv.warpAffine(
            face,
            transformation_matrix,
            (face.shape[1], face.shape[0]),
            flags=open_cv.INTER_CUBIC,
        )

        return face_aligned

    def get_mass_center(self, point_list: np.array) -> tuple:
        """Récupère le point centrale par rapport à la liste des points en paramètres.

        Args:
            point_list (np.array): liste des coordonnées d'une partie.

        Returns:
            tuple: le point centrale de tous les autres points.
        """
        return point_list.mean(axis=0).astype(np.float16)
