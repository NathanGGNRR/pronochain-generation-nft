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

File: app/generation_nft/tests/test_tilt_learning.py
"""

import warnings
from pathlib import Path
from typing import Union

import cv2 as open_cv
import numpy as np
import pytest

from app.generation_nft.libraries.face.face_landmarks.constants import (
    CHEEK_POINTS,
    LEFT_POINT,
    LEFT_TILT_POINTS,
    RIGHT_POINT,
    RIGHT_TILT_POINTS,
)
from app.generation_nft.libraries.face.face_landmarks.face_landmarks import (
    FaceLandmarks,
)
from app.generation_nft.libraries.face.face_styling.face_styling import FaceStyling
from app.generation_nft.libraries.face.tilt_learning.tilt_learning import TiltLearning
from app.settings import settings

warnings.filterwarnings("ignore")


@pytest.fixture
def image_path() -> Path:
    """Récupérer le chemin d'une image.

    Returns:
        Path: chemin de l'image.
    """
    return Path(f"{settings.GENERATION_NFT_PATH}/tests/pictures/tilt.jpg")


@pytest.fixture
def face_styling() -> FaceStyling:
    """Face styling instance.

    Returns:
        FaceStyling: face styling instance.
    """
    return FaceStyling()


@pytest.fixture
def face_landmarks() -> FaceLandmarks:
    """Face landmarks instance.

    Returns:
        FaceLandmarks: face landmarks instance.
    """
    return FaceLandmarks(min_detection_confidence=0.8)


@pytest.fixture
def image(image_path: Path) -> np.array:
    """Image.

    Args:
        image_path (Path): image path.

    Returns:
        np.array: image.
    """
    file_path = f"{image_path.parent}/{image_path.name}"
    return open_cv.imread(file_path)


@pytest.fixture
def landmarks(face_landmarks: FaceLandmarks, image: np.array) -> Union[list, None]:
    """Landmarks array.

    Args:
        face_landmarks (FaceLandmarks): face landmarks instance.
        image (np.array): image.

    Returns:
        Union[list, None]: landmarks array.
    """
    return face_landmarks.face_landmark(image).landmark


@pytest.fixture
def tilt_learning() -> TiltLearning:
    """Tilt learning instance.

    Returns:
        TiltLearning: tilt learning instance.
    """
    return TiltLearning()


def test_image_path(image_path: Path):
    """Test le chemin de l'image.

    Args:
        image_path (Path): chemin de l'image.

    Raises:
        AssertionError: L'image est introuvable.
        AssertionError: Le nom de l'image n'est pas correcte.
    """
    if not image_path.is_file():
        raise AssertionError("L'image est introuvable.")

    if str(image_path.name) != "tilt.jpg":
        raise AssertionError("Le nom de l'image n'est pas correcte.")


def test_image(image: np.array):
    """Test la fonction imread d'open_cv.

    Args:
        image (np.array): image.

    Raises:
        AssertionError: L'image est introuvable.
        AssertionError: L'image n'est pas de la bonne taille.
    """
    if image is None:
        raise AssertionError("L'image est introuvable.")

    if image.shape[0] != 225 or image.shape[1] != 225:
        raise AssertionError("L'image n'est pas de la bonne taille.")


def test_get_side_vertical_symetric_percentage(
    face_styling: FaceStyling,
    landmarks: Union[list, None],
    tilt_learning: TiltLearning,
):
    """Test la récupération des valeurs d'un côté du visage.

    Args:
        face_styling (FaceStyling): face styling instance.
        landmarks (Union[list, None]):  face landmarks array.
        tilt_learning (TiltLearning): tilt learning instance.

    Raises:
        AssertionError: La différence de distance à gauche est incorrecte.
        AssertionError: La différence de distance à gauche en pourcentage est incorrecte.
    """
    vertical_coordinates_left = face_styling.get_coordinates_from_points(
        landmarks,
        LEFT_TILT_POINTS,
        ["z", "y"],
        scale=False,
        inverted_y=True,
    )
    (
        left_distance_difference,
        left_distance_difference_percentage,
    ) = tilt_learning.get_side_vertical_symetric_percentage(vertical_coordinates_left)

    if int(left_distance_difference) != 31:
        raise AssertionError("La différence de distance à gauche est incorrecte.")
    if int(left_distance_difference_percentage) != 17:
        raise AssertionError(
            "La différence de distance à gauche en pourcentage est incorrecte."
        )


def test_get_horizontal_symetric_percentage(
    face_styling: FaceStyling,
    image: np.array,
    landmarks: Union[list, None],
    tilt_learning: TiltLearning,
):
    """Test la récupération des informations horizontales.

    Args:
        face_styling (FaceStyling): face styling instance.
        image (np.array): image.
        landmarks (Union[list, None]):  face landmarks array.
        tilt_learning (TiltLearning): tilt learning instance.

    Raises:
        AssertionError: La différence de distance horizontale est incorrecte.
        AssertionError: La différence de profondeur horizontale est incorrecte.
    """
    horizontal_cheek_points = face_styling.get_coordinates_from_points(
        landmarks, CHEEK_POINTS, ["x"], scale=False, image=image
    )

    horizontal_side_points = face_styling.get_coordinates_from_points(
        landmarks, [LEFT_POINT, RIGHT_POINT], ["z"]
    )

    (
        horizontal_distance_difference,
        horizontal_z_difference,
    ) = tilt_learning.get_horizontal_symetric_percentage(
        horizontal_cheek_points, horizontal_side_points
    )

    if horizontal_distance_difference != 93:
        raise AssertionError("La différence de distance horizontale est incorrecte.")
    if horizontal_z_difference != 94:
        raise AssertionError("La différence de profondeur horizontale est incorrecte.")


def test_get_vertical_symetric_percentage(
    face_styling: FaceStyling,
    landmarks: Union[list, None],
    tilt_learning: TiltLearning,
):
    """Test la récupération des informations verticales.

    Args:
        face_styling (FaceStyling): face styling instance.
        landmarks (Union[list, None]):  face landmarks array.
        tilt_learning (TiltLearning): tilt learning instance.

    Raises:
        AssertionError: La différence de distance verticale est incorrecte.
        AssertionError: La différence de distance du point centrale est incorrecte.
    """
    vertical_coordinates_left = face_styling.get_coordinates_from_points(
        landmarks,
        LEFT_TILT_POINTS,
        ["z", "y"],
        scale=False,
        inverted_y=True,
    )

    vertical_coordinates_right = face_styling.get_coordinates_from_points(
        landmarks,
        RIGHT_TILT_POINTS,
        ["z", "y"],
        scale=False,
        inverted_y=True,
    )

    (
        vertical_distance_difference,
        percentage_distance_middlepoint_difference,
    ) = tilt_learning.get_vertical_symetric_percentage(
        vertical_coordinates_left, vertical_coordinates_right
    )

    if vertical_distance_difference != 92:
        raise AssertionError("La différence de distance verticale est incorrecte.")
    if percentage_distance_middlepoint_difference != 18:
        raise AssertionError(
            "La différence de distance du point centrale est incorrecte."
        )


def test_is_looking_front(
    face_styling: FaceStyling,
    image: np.array,
    landmarks: Union[list, None],
    tilt_learning: TiltLearning,
):
    """Test les modèles de machine learning pour savoir si le visage regarde en face.

    Args:
        face_styling (FaceStyling): face styling instance.
        image (np.array): image.
        landmarks (Union[list, None]):  face landmarks array.
        tilt_learning (TiltLearning): tilt learning instance.

    Raises:
        AssertionError: Le visage ne regarde pas en face.
    """
    datasets = tilt_learning.generate_datasets(image, face_styling, landmarks)

    if tilt_learning.is_looking_front(datasets):
        raise AssertionError("Le visage ne regarde pas en face.")
