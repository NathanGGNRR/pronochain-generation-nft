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

File: app/generation_nft/libraries/face/tilt_learning/tilt_learning_data.py
"""

import math
import warnings

import numpy as np

from app import logger
from app.generation_nft.libraries.face.face_landmarks.constants import (
    CHEEK_POINTS,
    LEFT_POINT,
    LEFT_TILT_POINTS,
    RIGHT_POINT,
    RIGHT_TILT_POINTS,
)
from app.generation_nft.libraries.face.face_styling.face_styling import FaceStyling
from app.generation_nft.utils import get_mean, get_percentage, set_positive

warnings.filterwarnings("ignore")


class TiltLearningData(object):
    """Classe avec toutes les fonctions pour récupérer les informations du visage."""

    def __init__(self):
        """Initialisation de la classe TiltLearningData."""
        pass

    def generate_datasets(
        self,
        image: np.array,
        face_styling: FaceStyling,
        landmark_points: list,
    ) -> dict:
        """Génère le datasets pour le machine learning.

        Args:
            image (np.array): image.
            face_styling (FaceStyling): face styling instance.
            landmark_points (list): liste des points du visage.

        Returns:
            dict: datasets.
        """
        # l'ordre des index de chaque point à une importance
        horizontal_cheek_points = face_styling.get_coordinates_from_points(
            landmark_points, CHEEK_POINTS, ["x"], scale=False, image=image
        )

        horizontal_side_points = face_styling.get_coordinates_from_points(
            landmark_points, [LEFT_POINT, RIGHT_POINT], ["z"]
        )

        (
            horizontal_distance_difference,
            horizontal_z_difference,
        ) = self.get_horizontal_symetric_percentage(
            horizontal_cheek_points, horizontal_side_points
        )

        # l'ordre des index de chaque point à une importance
        vertical_coordinates_left = face_styling.get_coordinates_from_points(
            landmark_points,
            LEFT_TILT_POINTS,
            ["z", "y"],
            scale=False,
            inverted_y=True,
        )

        # l'ordre des index de chaque point à une importance
        vertical_coordinates_right = face_styling.get_coordinates_from_points(
            landmark_points,
            RIGHT_TILT_POINTS,
            ["z", "y"],
            scale=False,
            inverted_y=True,
        )

        (
            vertical_distance_difference,
            percentage_distance_middlepoint_difference,
        ) = self.get_vertical_symetric_percentage(
            vertical_coordinates_left, vertical_coordinates_right
        )

        return {
            "horizontal_distance_difference": horizontal_distance_difference,
            "horizontal_z_difference": horizontal_z_difference,
            "vertical_distance_difference": vertical_distance_difference,
            "percentage_distance_middlepoint_difference": percentage_distance_middlepoint_difference,
        }

    def get_side_vertical_symetric_percentage(self, points: list) -> tuple:
        """Récupère les pourcentage entre plusieurs distance pour déterminé l'inclinaison verticale.

        Args:
            points (list): liste des points que l'on souhaite analyser.

        Returns:
            tuple: vertical_distance_difference, percentage_distance_middlepoint_difference, height_middlepoint_sidepoint_difference
        """
        z_distances = []

        for index in range(len(points)):
            next_index = 0 if index + 1 > len(points) - 1 else index + 1
            first_point, second_point = points[index], points[next_index]
            z_distances.append(set_positive(second_point[0] - first_point[0]))

        differences = []

        for i in range(0, len(z_distances), 2):
            try:
                first_distance, second_distance = z_distances[i], z_distances[i + 1]
                differences.append(get_percentage(first_distance, second_distance))
            except IndexError:
                logger.error(
                    "Les distances des calculs verticales doit avoir un nombre pair."
                )
                continue

        return differences[1] - differences[0], get_percentage(
            differences[0], differences[1]
        )

    def get_vertical_symetric_percentage(
        self, vertical_left_points: list, vertical_right_points: list
    ) -> tuple:
        """Récupère les valeurs permettant de déterminer si la tête est inclinée en haut ou en bas.

        Args:
            vertical_left_points (list): liste des points de la partie gauche du visage.
            vertical_right_points (list): liste des points de la partie droit du visage.

        Returns:
            tuple: pourcentage de différence entre deux valeurs pour la distance et la moyenne des différence
        """
        (
            left_distance_difference,
            left_distance_difference_percentage,
        ) = self.get_side_vertical_symetric_percentage(vertical_left_points)

        (
            right_distance_difference,
            right_distance_difference_percentage,
        ) = self.get_side_vertical_symetric_percentage(vertical_right_points)

        return math.ceil(
            get_percentage(left_distance_difference, right_distance_difference)
        ), math.ceil(
            get_mean(
                [
                    left_distance_difference_percentage,
                    right_distance_difference_percentage,
                ]
            )
        )

    def get_horizontal_symetric_percentage(
        self, horizontal_cheek_points: list, horizontal_side_points: list
    ) -> tuple:
        """Récupère les valeurs permettant de déterminer si la tête est inclinée à droite ou a gauche.

        Args:
            horizontal_cheek_points (list): différents points permettant de calculer l'inclinaison horizontale.
            horizontal_side_points (list): différents points permettant de calculer la profondeur du visage.

        Returns:
            tuple: pourcentage de différence entre deux valeurs pour connaître l'inclinaison de la tête horizontale.
        """
        distances = []

        # récupère la différence de distance entre deux point à gauche du visage et deux points à droite du visage
        for i in range(0, len(horizontal_cheek_points), 2):
            try:
                first_distance, second_distance = (
                    horizontal_cheek_points[i][0],
                    horizontal_cheek_points[i + 1][0],
                )
            except IndexError:
                logger.error(
                    "Le nombre de point pour les calculs horizontales doit être pair."
                )
                continue
            distances.append(second_distance - first_distance)

        first_distance, second_distance = distances[0], distances[1]

        horizontal_distance_difference = math.ceil(
            get_percentage(distances[0], distances[1])
        )

        # récupère la différence en pourcentage du point z gauche du visage et du point z droit du visage
        horizontal_z_difference = math.ceil(
            get_percentage(horizontal_side_points[0][0], horizontal_side_points[1][0])
        )

        return (
            horizontal_distance_difference,
            horizontal_z_difference,
        )
