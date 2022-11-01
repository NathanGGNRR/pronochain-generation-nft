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

File: app/generation_nft/libraries/face/face_landmarks/face_landmarks.py
"""
from typing import Union

import cv2 as open_cv
import numpy as np
from mediapipe.python.solutions import face_mesh as mediapipe_fm

from app import logger
from app.generation_nft.libraries.face.face_landmarks.constants import ADD_POINT_LIST
from app.generation_nft.utils import normalize_values


class FaceLandmarks(object):
    """Classe permettant d'intéragir avec les landmarks."""

    def __init__(self, min_detection_confidence: float = None):
        """Initialise la classe d'intéraction des landamarks.

        Args:
            min_detection_confidence (float, optional): la valeur minimum de confiance de la détection d'un visage. Par défaut à 0.8 (80%).
        """
        if min_detection_confidence is not None:
            self.min_detection_confidence = min_detection_confidence

    def face_landmark(
        self, face: np.array, check: bool = True
    ) -> Union[tuple, list, None]:
        """Récupère les différents points de la détection des landmarks.

        Args:
            face (np.array): face.
            check (bool, optional): correspond à l'étape de vérification, si la valeur est False, les parties sont retournées. Défaut à True.

        Raises:
            mesh_error: erreur lors de la détection du masque.
            landmark_detect_error: aucune détection de masque.

        Returns:
            Union[tuple, list, None]: liste de coordonnées x, y et z de chaque point des landmarks.
        """
        with mediapipe_fm.FaceMesh(
            static_image_mode=True,
            refine_landmarks=True,
            max_num_faces=1,
            min_detection_confidence=self.min_detection_confidence,
        ) as face_mesh:
            try:
                results = face_mesh.process(
                    open_cv.cvtColor(face, open_cv.COLOR_BGR2RGB)
                )

            except Exception as mesh_error:
                logger.error(
                    f"La détection des landmarks sur le visage du joueur {self.player.code} a rencontrée une erreur.",
                    mesh_error,
                )
                raise mesh_error

            try:
                face_landmark = results.multi_face_landmarks[0]
                if not check:
                    normalized_landmark_points = normalize_values(
                        face, face_landmark.landmark
                    )
                    normalized_landmark_points = self.add_points(
                        normalized_landmark_points, ADD_POINT_LIST
                    )

                    return face_landmark, normalized_landmark_points
                return face_landmark
            except TypeError as landmark_detect_error:
                logger.error(
                    f"Aucune détection de visage sur l'image du joueur {self.player.code} pour les landmarks.",
                    landmark_detect_error,
                )
                return None

    def add_points(self, landmarks: list, point_list: list) -> list:
        """Ajoute une liste de points dans les coordonnées des parties du visage.

        Args:
            landmarks (list): coordonnées des parties du visage.
            point_list (list): liste de points à ajouter.

        Returns:
            list: coordonnées des parties du visage avec les nouveaux points.
        """
        for points in point_list:
            new_point = self.add_point(landmarks, points[0], points[1])
            landmarks.append(new_point)
        return landmarks

    def add_point(self, landmarks: list, first_point: int, second_point: int) -> dict:
        """Ajoute un point dans les coordonnées des parties du visage.

        Args:
            landmarks (list): coordonnées des parties du visage.
            first_point (int): index du premier point.
            second_point (int): index du deuxième point.

        Returns:
            dict: nouveau point qui se situe entre les deux points.
        """
        first_landmark_point, second_landmark_point = (
            landmarks[first_point],
            landmarks[second_point],
        )
        first_landmark_point_x, first_landmark_point_y, first_landmark_point_z = (
            first_landmark_point.get("x"),
            first_landmark_point.get("y"),
            first_landmark_point.get("z"),
        )
        second_landmark_point_x, second_landmark_point_y, second_landmark_point_z = (
            second_landmark_point.get("x"),
            second_landmark_point.get("y"),
            second_landmark_point.get("z"),
        )
        width, height, new_z = (
            int(round(abs(first_landmark_point_x - second_landmark_point_x) / 2)),
            int(round(abs(first_landmark_point_y - second_landmark_point_y) / 2)),
            round((first_landmark_point_z + second_landmark_point_z) / 2, 2),
        )
        new_x = (
            first_landmark_point_x + width
            if first_landmark_point_x < second_landmark_point_x
            else first_landmark_point_x - width
        )
        new_y = (
            first_landmark_point_y + height
            if first_landmark_point_y < second_landmark_point_y
            else first_landmark_point_y - height
        )

        return {"x": new_x, "y": new_y, "z": new_z}
