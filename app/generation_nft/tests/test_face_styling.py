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

File: app/generation_nft/tests/test_face_styling.py
"""

from pathlib import Path
from typing import Union

import cv2 as open_cv
import numpy as np
import pytest

from app.generation_nft.libraries.face.face_landmarks.constants import (
    LEFT_EYE,
    LEFT_POINT,
    LEFT_TILT_POINTS,
)
from app.generation_nft.libraries.face.face_landmarks.face_landmarks import (
    FaceLandmarks,
)
from app.generation_nft.libraries.face.face_styling.face_styling import FaceStyling
from app.settings import settings


@pytest.fixture
def image_path() -> Path:
    """Récupérer le chemin d'une image.

    Returns:
        Path: chemin de l'image.
    """
    return Path(f"{settings.GENERATION_NFT_PATH}/tests/pictures/1.jpg")


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


def test_get_coordinates_from_list(
    face_styling: FaceStyling,
    image: np.array,
    landmarks: Union[list, None],
):
    """Test la création des landmarks.

    Args:
        face_styling (FaceStyling):  face styling instance.
        image (np.array): image.
        landmarks (Union[list, None]):  face landmarks array.

    Raises:
        AssertionError: La récupération des coordonées d'un point n'a pas fonctionnée.
    """
    left_eye_coordinates = face_styling.get_coordinates_from_list(
        image, landmarks, LEFT_EYE
    )
    if len(left_eye_coordinates) != 16:
        raise AssertionError(
            "La récupération de plusieurs coordonnées n'a pas fonctionnée."
        )


def test_get_coordinate_from_point(
    face_styling: FaceStyling,
    image: np.array,
    landmarks: Union[list, None],
):
    """Test la création des landmarks.

    Args:
        face_styling (FaceStyling):  face styling instance.
        image (np.array): image.
        landmarks (Union[list, None]):  face landmarks array.

    Raises:
        AssertionError: La récupération du x d'une coordonnées n'a pas fonctionnée.
    """
    left_x = face_styling.get_coordinate_from_point(
        landmarks, LEFT_POINT, "x", image.shape[1]
    )
    if left_x != 265:
        raise AssertionError(
            "La récupération du x d'une coordonnées n'a pas fonctionnée."
        )


def test_get_coordinates_from_points(
    face_styling: FaceStyling,
    landmarks: Union[list, None],
):
    """Test la création des landmarks.

    Args:
        face_styling (FaceStyling):  face styling instance.
        landmarks (Union[list, None]):  face landmarks array.

    Raises:
        AssertionError: La récupération de plusieurs variables d'une coordonnées n'a pas fonctionnée.
    """
    left_tilt_points = face_styling.get_coordinates_from_points(
        landmarks, LEFT_TILT_POINTS, ["z", "y"], scale=False
    )
    if len(left_tilt_points) != 4:
        raise AssertionError(
            "La récupération de plusieurs variables d'une coordonnées n'a pas fonctionnée."
        )
